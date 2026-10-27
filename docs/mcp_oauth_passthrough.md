# MCP OAuth Passthrough

Some MCP servers run their own OAuth issuer and expect the client (Claude Code, Cursor, ChatGPT, etc.) to authenticate directly against it. For those servers Lumina can let the client's own upstream token flow through instead of minting, storing, or refreshing anything itself.

Two `auth_type` values cover this. They differ in one thing: whether Lumina still authenticates the caller at its own edge.

| Mode | Lumina admission | Credential forwarded upstream | Spend / rate limits / audit | Use when |
|------|-------------------|-------------------------------|-----------------------------|----------|
| `true_passthrough` | None; anonymous at the Lumina layer | The client's `Authorization`, verbatim | Not recorded | Lumina should add zero auth and the upstream is the sole gate |
| `oauth_delegate` | Required (Lumina key / SSO / JWT) | A distinct upstream bearer the caller sends alongside admission | Recorded, keyed on the admission identity | You want Lumina to keep gating and observing the route while the upstream owns tool authorization |

Both modes return the upstream's protected-resource metadata verbatim during discovery, so the client always authorizes against the real upstream issuer.

Both forward the token exactly as the caller sent it. Lumina does not decode it, does not check its audience or scopes, and does not exchange it; the upstream MCP server is the only party that validates it. If the caller's token was minted for a different resource, neither mode can make it work, and you want [`oauth2_token_exchange`](#audience-locked-tokens-passthrough-or-token-exchange) instead.

Both also take an orthogonal `dcr_bridge` flag that changes where an OAuth-only client discovers its authorization server. Turn it on for clients that cannot register with the upstream IdP themselves or cannot send two separate credentials, such as OpenCode, Claude Code, Cursor, and Claude Desktop. See [Gateway-hosted sign-in (DCR bridge)](#gateway-hosted-sign-in-dcr-bridge).

## Audience-locked tokens: passthrough or token exchange {#audience-locked-tokens-passthrough-or-token-exchange}

An OAuth access token carries an audience (`aud`, or the resource it was requested for). A well-behaved upstream MCP server rejects any token whose audience names something else, for example a token an agent obtained for a SaaS API and then presented to the MCP server. Because `true_passthrough` and `oauth_delegate` forward the token verbatim, that rejection shows up as the upstream's own `401` relayed back to the client. This is the correct confused-deputy-safe outcome: the gateway did not launder a token minted for one resource into access to another, and it is not a Lumina bug to file.

Pick the mode from the token you actually hold:

| The caller's token was minted for | Use | What Lumina does with it |
|-----------------------------------|-----|---------------------------|
| The upstream MCP server itself (the client ran OAuth against that server's issuer) | `true_passthrough` or `oauth_delegate` | Forwards it verbatim; the upstream validates audience and scopes |
| A different resource (your IdP, an internal API, a SaaS API), and your IdP supports RFC 8693 or Entra On-Behalf-Of | `oauth2_token_exchange` | Sends it to the IdP as the `subject_token`, receives a token whose audience is the MCP server (`audience: ...` in the server config), caches it, and forwards only the exchanged token. See [MCP OBO Auth](./mcp_obo_auth.md) |
| A Lumina virtual key, SSO session, or IdP JWT that only proves identity to the gateway | Neither passthrough mode | Admission credentials are never forwarded upstream. Configure a server-side credential (`oauth2` client credentials, a static `authentication_token`, or token exchange) instead |

The practical test: if you would have to ask your IdP to widen a token's audience so the upstream accepts it, stop and use token exchange. Widening audiences turns one bearer into a key for several resources, and the passthrough modes exist precisely so that the gateway never does that on the caller's behalf.

## true_passthrough

Lumina acts as a transparent proxy: no admission check, nothing minted or stored, and the client's `Authorization` forwarded unchanged. Reach for it when the upstream is the source of truth for access and you do not want Lumina gating the route twice.

### Setup

```yaml title="config.yaml" showLineNumbers
mcp_servers:
  notion_passthrough:
    url: "https://mcp.notion.com/mcp"
    auth_type: true_passthrough
```

That is the entire configuration. No client credentials or token endpoints, because Lumina never participates in the token exchange.

### How It Works

- The client sends its MCP request with no Lumina API key.
- With no upstream token yet, Lumina relays the upstream's own `401` and `WWW-Authenticate`.
- The client runs OAuth directly against the upstream issuer.
- The client retries with `Authorization: Bearer <upstream-token>`, and Lumina forwards it untouched.

```mermaid
sequenceDiagram
    participant Client
    participant Lumina as Lumina Proxy
    participant MCP as Upstream MCP Server
    participant Auth as Upstream OAuth Server

    Client->>Lumina: MCP request (no Lumina key)
    Lumina-->>Client: 401 + WWW-Authenticate (upstream challenge, relayed)

    Note over Client,Auth: Client runs OAuth directly with upstream
    Client->>Auth: Authorize + token exchange
    Auth-->>Client: access_token

    Client->>Lumina: MCP request + Bearer access_token
    Lumina->>MCP: Forward request + Bearer access_token (verbatim)
    MCP-->>Lumina: MCP response
    Lumina-->>Client: MCP response
```

### Fail-Closed Behavior

The transparent path fires only when every target resolves to `true_passthrough`. It falls back to normal Lumina admission when:

- The server's `auth_type` is anything else.
- The request targets multiple servers (`x-mcp-servers: a,b`) and any one is not `true_passthrough`.
- The target server cannot be resolved from the URL path or the `x-mcp-servers` header.

### Security Trade-offs

- The MCP route becomes an unauthenticated ingress at the Lumina layer.
- Spend tracking, per-key rate limits, and any guardrail depending on `user_api_key_auth.user_id` do not run.
- Lumina cannot tell who the caller is, so per-user auditing must come from the upstream server's logs.
- `available_on_public_internet: false` adds no authentication here; it mainly controls IP-based discovery ([see guide](./mcp_public_internet.md)).
- Only enable it on servers whose upstream OAuth issuer you trust to enforce access control.

### Config Reference

| Field | Required | Description |
|-------|----------|-------------|
| `auth_type` | Yes | Must be `true_passthrough`. |
| `url` | Yes | The upstream MCP server URL. |
| `allowed_tools` | No | Server-level tool allowlist. With no caller identity there are no per-key or per-team tool permissions, so this list is the only tool restriction and it applies to every caller identically. |

```yaml title="config.yaml" showLineNumbers
mcp_servers:
  notion_passthrough:
    url: "https://mcp.notion.com/mcp"
    auth_type: true_passthrough
    allowed_tools:
      - search
      - fetch
```

## oauth_delegate

Lumina still admits the caller (Lumina API key, SSO, or JWT), then forwards a separate upstream bearer the caller supplies. Lumina mints nothing and never forwards the admission credential upstream. Use it when the upstream owns tool-level authorization but you still want Lumina gating the route and keeping spend, rate-limit, and audit attribution.

### Setup

```yaml title="config.yaml" showLineNumbers
mcp_servers:
  notion_delegate:
    url: "https://mcp.notion.com/mcp"
    auth_type: oauth_delegate
```

No client credentials, for the same reason as `true_passthrough`. What changes is the request: the caller sends two credentials.

### How It Works

- The caller admits with a Lumina credential in `x-lumina-api-key`.
- The upstream token rides in `Authorization` (or `x-mcp-<alias>-authorization` for aggregate requests).
- Lumina validates admission, then forwards only the upstream bearer, never the admission credential.
- With no upstream token yet, Lumina returns a `401` pointing at the gateway's `oauth-protected-resource` well-known, which proxies the upstream metadata verbatim.

```mermaid
sequenceDiagram
    participant Client
    participant Lumina as Lumina Proxy
    participant MCP as Upstream MCP Server
    participant Auth as Upstream OAuth Server

    Client->>Lumina: MCP request + x-lumina-api-key (no upstream token)
    Note over Lumina: Admit caller (key / SSO / JWT)
    Lumina-->>Client: 401 + WWW-Authenticate (gateway, proxies upstream metadata)

    Note over Client,Auth: Client runs OAuth directly with upstream
    Client->>Auth: Authorize + token exchange
    Auth-->>Client: access_token

    Client->>Lumina: MCP request + x-lumina-api-key + Authorization: Bearer access_token
    Note over Lumina: Admit caller, strip admission credential, record spend / rate limit / audit
    Lumina->>MCP: Forward request + Bearer access_token (upstream token only)
    MCP-->>Lumina: MCP response
    Lumina-->>Client: MCP response
```

:::warning[Keep the two credentials in separate headers]

If a caller sends a single credential in `Authorization` with no `x-lumina-api-key`, Lumina treats it as the admission credential (virtual key, IdP JWT, or SSO session token) and never forwards it upstream. That is the leak defense keeping a Lumina or IdP token from reaching a third-party MCP server.

:::

### Security Trade-offs

- Admission always runs, so there is no anonymous ingress.
- Spend, rate limits, and audit resolve against the admission identity.
- Lumina forwards the upstream token without inspecting it, so the upstream still owns tool-level authorization and token validation.

### Config Reference

| Field | Required | Description |
|-------|----------|-------------|
| `auth_type` | Yes | Must be `oauth_delegate`. |
| `url` | Yes | The upstream MCP server URL. |

At request time: admission in `x-lumina-api-key`, upstream token in `Authorization: Bearer <upstream-token>` (or `x-mcp-<alias>-authorization` for a specific server in an aggregate request).

Because admission runs, the full Lumina permission model applies on top of whatever the upstream enforces: [per-key and per-team tool permissions](./mcp_control.md#per-entity-tool-level-permissions), the server-level `allowed_tools` list, per-key rate limits, and spend logging of every tool call under the admitted identity.

## Multi-server aggregate requests {#multi-server-aggregate-requests}

A request to the aggregate `/mcp` endpoint (or one carrying `x-mcp-servers: a,b`) fans out to several upstreams, but the request can only carry one `Authorization` header. If two of those upstreams both forward the caller's token, sending that one header to both would replay a single bearer across unrelated resources (the cross-resource replay RFC 9700 warns about). Lumina therefore applies two rules to `true_passthrough` and `oauth_delegate` servers inside an aggregate scope.

Bind one upstream token to one server with `x-mcp-{alias}-authorization`. The alias is lowercased and any character outside `a-z0-9_` becomes `_`, so a server aliased `Jira Cloud` is addressed as `x-mcp-jira_cloud-authorization`. The value is forwarded verbatim, so include the scheme (`Bearer <token>`). Per-server headers are never withheld, on any operation, because each one names exactly one recipient.

The request-wide `Authorization` is withheld from a client-forwarded server during a listing fan-out (`tools/list`, and the prompt and resource listings) whenever another server in the same scope would also consume it. That server is then listed with no upstream credential, so a server that requires one returns its `401` and the aggregate absorbs it (see below). Explicitly addressed operations such as `tools/call` on a named tool, a single-server route like `/{server_name}/mcp`, or an aggregate scope where only one server forwards the caller's token are unaffected: the client named the one recipient, so the request-wide header is forwarded to it.

In practice this is why a single bearer that is valid for several upstreams can execute tools through the aggregate endpoint yet not appear in the aggregate `tools/list`: the tool call names one server, the listing does not. The fix is to send the token per server rather than request-wide.

```bash title="Aggregate tools/list with per-server tokens" showLineNumbers
curl -X POST "https://lumina.example.com/mcp" \
  -H "Content-Type: application/json" \
  -H "x-lumina-api-key: Bearer $LUMINA_API_KEY" \
  -H "x-mcp-servers: jira,confluence" \
  -H "x-mcp-jira-authorization: Bearer <token-for-jira>" \
  -H "x-mcp-confluence-authorization: Bearer <token-for-confluence>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Sending the same token value on two per-server headers is your decision, made explicitly per server, and Lumina honors it. What it refuses to do is make that decision for you by fanning out an unaddressed `Authorization`.

For `true_passthrough` there is an additional constraint: the transparent admission path fires only when every server in the scope is `true_passthrough`. Mixing a `true_passthrough` server into an aggregate with any other mode falls back to normal Lumina admission, so the caller needs a Lumina credential for that request.

## Previewing tools in the Admin UI {#previewing-tools-in-the-admin-ui}

Lumina holds no upstream token for these servers, so the create and edit forms cannot list tools on their own. Both forms show an "Authorize & Fetch Tools (browser-only)" button for `true_passthrough` and `oauth_delegate`. It runs the upstream OAuth flow in the admin's browser and keeps the resulting token in that browser session only, forwarding it per server for the tool preview and for configuring `allowed_tools`. The token is not written to the server row, to the per-user credential store, or to any cache; closing the tab discards it.

The optional OAuth Client ID and Client Secret next to that button are different: they are saved with the server as declared configuration. Set them when the upstream issuer does not support dynamic client registration and every admin should authorize through one pre-registered app.

## Intentional limits {#intentional-limits}

The following are consequences of forwarding a token verbatim without inspecting it, and they are by design rather than defects.

On the multi-server aggregate there is no per-server "needs re-authentication" signal. A single-server route relays the upstream's `401` and `WWW-Authenticate` truthfully, but the aggregate absorbs one server's auth failure into an empty listing for that server so the remaining servers still list. Use the single-server route, or the per-server header, when you need to see which upstream rejected the token.

Sender-constrained tokens (DPoP, RFC 9449, or mTLS-bound tokens, RFC 8705) cannot be relayed. The binding proves the request came from the TLS client or the key holder that obtained the token, and a layer-7 proxy is neither. The upstream will reject them; obtain a plain bearer for the MCP server or use token exchange.

Revoked tokens are not detected at connect time. Lumina keeps no state about a forwarded token and does not introspect it, so a token revoked at the issuer is forwarded and rejected by the upstream on the request that uses it. The client sees the upstream's `401` at that point, exactly as it would talking to the upstream directly.

## Gateway-hosted sign-in (DCR bridge) {#gateway-hosted-sign-in-dcr-bridge}

OAuth-only MCP clients (OpenCode, Claude Code, Cursor, Claude Desktop) connect by running a single Dynamic Client Registration (RFC 7591) plus PKCE flow against whatever authorization server the discovery metadata advertises. They:

- Hold no client credential pre-provisioned with the upstream IdP.
- Cannot send a separate Lumina credential alongside an upstream token.

So neither the plain `true_passthrough` request nor the two-header `oauth_delegate` request fits them. The `dcr_bridge` flag closes that gap:

- **On:** Lumina advertises itself as the authorization server during discovery and hosts `/{server_name}/register`, `/{server_name}/authorize`, and `/{server_name}/token`. The client registers and signs in through the gateway while Lumina runs the upstream OAuth behind those endpoints.
- **Off:** Lumina relays the upstream server's own OAuth metadata verbatim. Suits clients already registered with the upstream IdP, or able to run DCR directly against it.

Where to set it:

- Valid only on `true_passthrough` and `oauth_delegate`; rejected on any other `auth_type` at create, update, and config load.
- In the Admin UI it is the "Gateway-hosted sign-in (DCR bridge)" switch on the MCP server form, defaulted on for those two modes.
- In config it is a boolean field.

### true_passthrough with the bridge

```yaml title="config.yaml" showLineNumbers
mcp_servers:
  miro:
    url: "https://mcp.miro.com/"
    transport: http
    auth_type: true_passthrough
    dcr_bridge: true
```

The transparent option for OAuth-only clients:

- The client discovers the gateway as its authorization server and registers through `POST /{server_name}/register`.
- It runs PKCE against `GET /{server_name}/authorize` and `POST /{server_name}/token`.
- Where the upstream supports DCR, Lumina relays the client's registration to it.
- Where the server has no stored `client_id`, Lumina mints an ephemeral client for the flow and persists nothing.
- No Lumina sign-in is involved, and no caller identity or spend is recorded.

### oauth_delegate with the bridge

```yaml title="config.yaml" showLineNumbers
mcp_servers:
  miro:
    url: "https://mcp.miro.com/"
    transport: http
    auth_type: oauth_delegate
    dcr_bridge: true
```

This combination keeps Lumina in the observability path for OAuth-only clients, so spend, rate limits, audit, and per-tool-call attribution all resolve. Reach for it when you want to see in Lumina which server a caller used and which tools it invoked.

An OAuth-only client cannot present a Lumina key inline, so identity comes from a Lumina browser session instead:

- At the authorize step Lumina looks for a Lumina UI session cookie.
- With no cookie, it redirects to Lumina login (`/sso/key/generate`) first.
- After sign-in the user re-initiates the connection.
- Lumina seals that identity plus the upstream token into a gateway-bound credential.
- The client stores that credential and replays it on every later request; admission, spend, and audit resolve against it.

:::warning[Two prerequisites]

- **The gateway needs a working browser sign-in** (SSO or username/password). Without one there is no identity to bind and the authorize step cannot proceed. A missing gateway sign-in is the usual reason an `oauth_delegate` bridge connection stalls at the login page.
- **The client's OAuth flow must run in an interactive browser session.** OpenCode, Claude Code, Cursor, and Claude Desktop all do.

For fully scripted, non-interactive delegation, leave `dcr_bridge` off and use the two-header `oauth_delegate` request instead.

:::

```mermaid
sequenceDiagram
    participant Client as OAuth-only client
    participant Browser
    participant Lumina as Lumina Proxy
    participant MCP as Upstream MCP Server
    participant Auth as Upstream OAuth Server

    Client->>Lumina: MCP request (no credential)
    Lumina-->>Client: 401 + WWW-Authenticate (gateway is the authorization server)
    Client->>Lumina: POST /{server}/register (DCR)
    Client->>Browser: open /{server}/authorize
    Browser->>Lumina: GET /{server}/authorize
    Note over Lumina: no Lumina session cookie
    Lumina-->>Browser: redirect to Lumina login
    Browser->>Lumina: sign in (SSO / username-password)
    Browser->>Lumina: GET /{server}/authorize (with session)
    Lumina->>Auth: authorize upstream, capture code at /callback
    Auth-->>Lumina: upstream authorization code
    Lumina-->>Browser: gateway code, redirect back to client
    Client->>Lumina: POST /{server}/token
    Note over Lumina: seal Lumina identity + upstream token into one gateway-bound credential
    Lumina-->>Client: gateway-bound credential
    Client->>Lumina: MCP request + gateway-bound credential
    Note over Lumina: admit, record spend / rate limit / audit / tool calls
    Lumina->>MCP: forward request + upstream token (identity credential stripped)
    MCP-->>Lumina: MCP response
    Lumina-->>Client: MCP response
```

### Choosing the flag

| Situation | `dcr_bridge` |
|-----------|--------------|
| An OAuth-only client (OpenCode, Claude Code, Cursor, Claude Desktop, ChatGPT) that holds no upstream `client_id` and cannot send two credentials | `true` |
| A client already registered with the upstream IdP, or one that runs DCR directly against the upstream | `false` |
| A scripted, non-interactive caller that can send `x-lumina-api-key` plus an upstream `Authorization` bearer | `false`, with `auth_type: oauth_delegate` (two-header form) |

### Connecting a client

- Point the client at `https://<gateway-host>/<server_name>/mcp` and let it discover OAuth from there.
- Do not configure a `client_id` or secret on the client; the gateway handles registration and the token exchange.
- On a `true_passthrough` bridge server the browser flow authorizes only with the upstream.
- On an `oauth_delegate` bridge server it signs in to Lumina first, then authorizes with the upstream.

Follow each client's own MCP documentation for exact field names, which change over time.

Claude Code registers and runs the browser flow on first use:

```bash
claude mcp add --transport http miro https://<gateway-host>/miro/mcp
```

Cursor reads remote MCP servers from `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "miro": {
      "url": "https://<gateway-host>/miro/mcp"
    }
  }
}
```

OpenCode reads them from `opencode.json`:

```json
{
  "mcp": {
    "miro": {
      "type": "remote",
      "url": "https://<gateway-host>/miro/mcp",
      "enabled": true
    }
  }
}
```

### Config Reference

| Field | Required | Description |
|-------|----------|-------------|
| `auth_type` | Yes | Must be `true_passthrough` or `oauth_delegate`; `dcr_bridge` is rejected on any other value. |
| `url` | Yes | The upstream MCP server URL. |
| `dcr_bridge` | Yes | `true` so the gateway hosts sign-in for OAuth-only clients. Off relays the upstream's own OAuth metadata instead. |

## Delegate Auth to Upstream (PKCE Passthrough) {#delegate-auth-to-upstream-pkce-passthrough}

:::warning[Deprecated]

`delegate_auth_to_upstream` is the original flag-based form of client-forwarded OAuth and is deprecated. It no longer bypasses Lumina admission: on current versions Lumina still requires its own API key, SSO, or JWT on every request that carries a bearer, and the proxy logs a deprecation warning when a server is loaded with `auth_type: oauth2` and `delegate_auth_to_upstream: true`. New servers should use `auth_type: oauth_delegate` (admission required, upstream token forwarded) or `auth_type: true_passthrough` (no admission). Existing configs should migrate to one of those two. The section below describes what the legacy flag still does.

:::

For OAuth2 MCP servers where the client authenticates directly against the upstream server's own OAuth issuer, the legacy flag lets a credential-free client reach the upstream's OAuth challenge through Lumina so it can start PKCE. Once the client holds an upstream token it must also present a Lumina credential, exactly as with `oauth_delegate`.

### Setup

```yaml title="config.yaml" showLineNumbers
mcp_servers:
  notion_mcp:
    url: "https://mcp.notion.com/mcp"
    auth_type: oauth2
    oauth2_flow: authorization_code
    delegate_auth_to_upstream: true
```

Delegated servers are interactive, so they take `oauth2_flow: authorization_code`. The flag is honored **only** when `auth_type: oauth2`; setting it on any other auth type is silently ignored.

:::warning[Internal-only (`available_on_public_internet: false`) and the anonymous discovery step]

`available_on_public_internet: false` does not make the credential-free cold start authenticated. An anonymous caller with no `Authorization` header can still reach the upstream OAuth2 `/authorize` challenge for a matching `auth_type: oauth2` server with `delegate_auth_to_upstream: true` (not `oauth2_flow: client_credentials`). The internal-only flag mainly controls IP-based discovery and related behavior ([see guide](./mcp_public_internet.md)). Tool calls are not affected: any request carrying a bearer goes through Lumina admission.

:::

### How It Works

1. The client sends an MCP request to Lumina with no `Authorization` header and no `x-lumina-api-key`.
2. Because every target server is `auth_type: oauth2` with `delegate_auth_to_upstream: true`, Lumina admits this credential-free request anonymously so the upstream's own `401` + `WWW-Authenticate` flows back to the client.
3. The client completes PKCE directly with the upstream OAuth issuer.
4. The client retries with `Authorization: Bearer <upstream-token>`. Lumina runs its own admission on this request. With no Lumina credential the request fails with `401`; the client has to send a Lumina key in `x-lumina-api-key` alongside the upstream bearer, which is the `oauth_delegate` request shape.
5. Once admitted, Lumina forwards the upstream bearer untouched and never forwards the Lumina credential.

```mermaid
sequenceDiagram
    participant Client
    participant Lumina as Lumina Proxy
    participant MCP as Upstream MCP Server
    participant Auth as Upstream OAuth Server

    Client->>Lumina: MCP request (no credentials at all)
    Lumina->>MCP: Forward request (no Authorization)
    MCP-->>Lumina: 401 + WWW-Authenticate
    Lumina-->>Client: 401 + WWW-Authenticate (passthrough)

    Note over Client,Auth: Client runs PKCE directly with upstream
    Client->>Auth: Authorize + token exchange (PKCE)
    Auth-->>Client: access_token

    Client->>Lumina: MCP request + Bearer access_token (no Lumina key)
    Lumina-->>Client: 401 (Lumina admission required)

    Client->>Lumina: MCP request + x-lumina-api-key + Bearer access_token
    Note over Lumina: Admit caller, strip admission credential
    Lumina->>MCP: Forward request + Bearer access_token
    MCP-->>Lumina: MCP response
    Lumina-->>Client: MCP response
```

### Fail-Closed Behavior

The anonymous cold start fires only when the request carries no bearer and **every** target opts in. It runs normal Lumina auth when:

- The request carries an `Authorization` header (any bearer, including an upstream token).
- The server's `auth_type` is anything other than `oauth2`.
- `delegate_auth_to_upstream` is not explicitly `true`.
- The server's effective `oauth2_flow` is `client_credentials`.
- The request targets multiple servers (`x-mcp-servers: a,b`) and any one is not delegated.
- The target server cannot be resolved from the URL path or `x-mcp-servers` header.

### Security Trade-offs

- Only the credential-free discovery step is anonymous. Tool calls run under a Lumina identity, so spend tracking, per-key rate limits, and guardrails apply as they do for `oauth_delegate`.
- Lumina forwards the upstream token without inspecting it, so the upstream still owns tool-level authorization and token validation.
- Because the flag is deprecated and behaves like `oauth_delegate` once a bearer is present, migrate to `auth_type: oauth_delegate` rather than relying on it.

### Config Reference

| Field | Required | Description |
|-------|----------|-------------|
| `auth_type` | Yes | Must be `oauth2`. The flag is ignored otherwise. |
| `oauth2_flow` | Yes | Set to `authorization_code`; delegation lets the client's interactive PKCE flow start against the upstream server. |
| `delegate_auth_to_upstream` | Yes | Set to `true` to opt this server into the legacy delegate behavior. Deprecated in favor of `auth_type: oauth_delegate`. |
