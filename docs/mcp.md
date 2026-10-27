import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Image from '@theme/IdealImage';

# MCP Overview

Lumina Proxy provides an MCP Gateway that allows you to use a fixed endpoint for all MCP tools and control MCP access by Key, Team. 

<Image 
  img={require('../img/mcp_2.png')}
  style={{width: '100%', display: 'block', margin: '2rem auto'}}
/>
<p style={{textAlign: 'left', color: '#666'}}>Lumina MCP Architecture: Use MCP tools with all Lumina supported models</p>

## Overview
| Feature | Description |
|---------|-------------|
| MCP Operations | • List Tools<br/>• Call Tools <br/>• Prompts <br/>• Resources |
| Direct REST API | [`/mcp-rest/tools/list` and `/mcp-rest/tools/call`](./mcp_rest_api.md) — call tools with curl without an LLM |
| Supported MCP Transports | • Streamable HTTP<br/>• SSE<br/>• Standard Input/Output (stdio) |
| Lumina Permission Management | • By Key<br/>• By Team<br/>• By Organization |

:::warning[MCP protocol update]
The gateway negotiates the protocol version during `initialize`. See [tested versions and capability limits](./mcp_config_reference#protocol-version).<br/>
Lumina namespaces multiple MCP servers by prefixing each tool name with its MCP server name, so newly created servers now must use names that comply with SEP-986; noncompliant names cannot be added anymore. Existing servers that still violate SEP-986 only emit warnings today, but future MCP-side rollouts may block those names entirely, so we recommend updating any legacy server names proactively before MCP enforcement makes them unusable.
:::

For a single decision reference covering which endpoint, transport, and auth pattern to use, see the [MCP Configuration Reference](./mcp_config_reference)

## Adding your MCP

### Prerequisites

To store MCP servers in the database, you need to enable database storage:

**Environment Variable:**
```bash
export STORE_MODEL_IN_DB=True
```

**OR in config.yaml:**
```yaml
general_settings:
  store_model_in_db: true
```

#### Fine-grained Database Storage Control

By default, when `store_model_in_db` is `true`, all object types (models, MCPs, guardrails, vector stores, etc.) are stored in the database. If you want to store only specific object types, use the `supported_db_objects` setting.

**Example: Store only MCP servers in the database**

```yaml title="config.yaml" showLineNumbers
general_settings:
  store_model_in_db: true
  supported_db_objects: ["mcp"]  # Only store MCP servers in DB

model_list:
  - model_name: {{openai_large}}
    lumina_params:
      model: openai/{{openai_large}}
      api_key: sk-xxxxxxx
```

**See all available object types:** [Config Settings - supported_db_objects](./proxy/config_settings.md#general_settings---reference)

If `supported_db_objects` is not set, all object types are loaded from the database (default behavior).

For diagnosing connectivity problems after setup, start with the [five-minute triage](./mcp_troubleshoot.md#locate-the-error-source) and the [symptom matrix](./mcp_troubleshoot.md#symptom-matrix) in the MCP Troubleshooting Guide.

<Tabs>
<TabItem value="ui" label="Lumina UI">

On the Lumina UI, Navigate to "MCP Servers" and click "Add New MCP Server".

On this form, you should enter your MCP Server URL and the transport you want to use.

Lumina supports the following MCP transports:
- Streamable HTTP
- SSE (Server-Sent Events)
- Standard Input/Output (stdio)

<Image 
  img={require('../img/add_mcp.png')}
  dark={require('../img/add_mcp_dark.png')}
  alt="Add New MCP Server form with a Streamable HTTP server"
  style={{width: '80%', display: 'block', margin: '0'}}
/>

<br/>
<br/>

### Add HTTP MCP Server

This video walks through adding and using an HTTP MCP server on Lumina UI and using it in Cursor IDE.

<iframe width="840" height="500" src="https://www.loom.com/embed/e2aebce78e8d46beafeb4bacdde31f14" frameBorder="0" allowFullScreen></iframe>

<br/>
<br/>

### Add SSE MCP Server

This video walks through adding and using an SSE MCP server on Lumina UI and using it in Cursor IDE.

<iframe width="840" height="500" src="https://www.loom.com/embed/07e04e27f5e74475b9cf8ef8247d2c3e" frameBorder="0" allowFullScreen></iframe>

<br/>
<br/>

### Add STDIO MCP Server

:::warning stdio is off by default

stdio MCP servers are disabled unless the proxy is started with `LUMINA_ENABLE_MCP_STDIO=true` in its environment. While it is off, the stdio transport is greyed out in the UI, creating or updating a stdio server returns an error, and existing stdio servers stay listed but never start: their tools are left out of tool listings, direct tool calls return `403`, and their health check reports them as unhealthy

The flag is read from the proxy's process environment only. Setting it under `environment_variables` in config.yaml or in the database has no effect

:::

**Upgrading with existing stdio servers?** Add `LUMINA_ENABLE_MCP_STDIO=true` to the proxy's environment and restart it. Until you do, the proxy logs a warning naming each stdio server it will not start

For stdio MCP servers, select "Standard Input/Output (stdio)" as the transport type and provide the stdio configuration in JSON format:

<Image 
  img={require('../img/add_stdio_mcp.png')}
  dark={require('../img/add_stdio_mcp_dark.png')}
  alt="Stdio configuration for an MCP server"
  style={{width: '80%', display: 'block', margin: '0'}}
/>

<br/>
<br/>

### OAuth Configuration & Overrides

Lumina attempts [OAuth 2.0 Authorization Server Discovery](https://datatracker.ietf.org/doc/html/rfc8414) by default. When you create an MCP server in the UI and set `Authentication: OAuth`, Lumina will locate the provider metadata, dynamically register a client, and perform PKCE-based authorization without you providing any additional details.

**Customize the OAuth flow when needed:**

<Image 
  img={require('../img/mcp_oauth.png')}
  dark={require('../img/mcp_oauth_dark.png')}
  alt="OAuth authentication settings for an MCP server"
  style={{width: '80%', display: 'block', margin: '0'}}
/>

- **Provide explicit client credentials** – If the MCP provider does not offer dynamic client registration or you prefer to manage the client yourself, fill in `client_id`, `client_secret`, and the desired `scopes`.
- **Override discovery URLs** – In some environments, Lumina might not be able to reach the provider's metadata endpoints. Use the optional `authorization_url`, `token_url`, and `registration_url` fields to point Lumina directly to the correct endpoints.

<br/>

### AWS SigV4 Authentication

For MCP servers hosted on [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html), select **AWS SigV4** as the authentication type. Lumina will sign every outgoing MCP request with your AWS credentials using [Signature Version 4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html).

<Image
  img={require('../img/mcp_aws_sigv4_ui.png')}
  dark={require('../img/mcp_aws_sigv4_ui_dark.png')}
  alt="AWS SigV4 authentication settings for an MCP server"
  style={{width: '80%', display: 'block', margin: '0'}}
/>

Fill in your AWS region, service name (defaults to `bedrock-agentcore`), and optionally your AWS access key and secret. If credentials are omitted, Lumina falls back to the boto3 credential chain (IAM roles, environment variables, etc.).

[**See full SigV4 setup guide**](./mcp_aws_sigv4.md)

<br/>

### Static Headers

Sometimes your MCP server needs specific headers on every request. Maybe it's an API key, maybe it's a custom header the server expects. Instead of configuring auth, you can just set them directly.

<Image 
  img={require('../img/static_headers.png')}
  dark={require('../img/static_headers_dark.png')}
  alt="Static headers in the MCP server permission settings"
  style={{width: '80%', display: 'block', margin: '0'}}
/>

These headers get sent with every request to the server. That's it.


**When to use this:**
- Your server needs custom headers that don't fit the standard auth patterns
- You want full control over exactly what headers are sent
- You're debugging and need to quickly add headers without changing auth configuration

### Server Variables

Store credentials on the server and reference them in static headers or authentication with `${VAR_NAME}` (e.g. `${DB_PROTOCOL}://${CORP_USERNAME}:${CORP_PASSWORD}@${DB_HOSTNAME}`). Scope each variable as **Instance** (shared) or **Per-user** (each user supplies their own).

<iframe width="840" height="500" src="https://www.loom.com/embed/12878e2be19140069170c3a270b50d1c" frameBorder="0" allowFullScreen></iframe>

**When to use this:**
- Each user needs to connect with their own static credentials
- You want to reuse certain shared details (e.g., DB url) across users

</TabItem>

<TabItem value="config" label="config.yaml">

Add your MCP servers directly in your `config.yaml` file:

```yaml title="config.yaml" showLineNumbers
model_list:
  - model_name: {{openai_large}}
    lumina_params:
      model: openai/{{openai_large}}
      api_key: sk-xxxxxxx

lumina_settings:
  # MCP Aliases - Map aliases to server names for easier tool access
  mcp_aliases:
    "github": "github_mcp_server"
    "zapier": "zapier_mcp_server"
    "deepwiki": "deepwiki_mcp_server"

mcp_servers:
  # HTTP Streamable Server
  deepwiki_mcp:
    url: "https://mcp.deepwiki.com/mcp"
  # SSE Server
  zapier_mcp:
    url: "https://actions.zapier.com/mcp/sk-akxxxxx/sse"
  
  # Standard Input/Output (stdio) Server - CircleCI Example
  # Requires LUMINA_ENABLE_MCP_STDIO=true in the proxy's environment
  circleci_mcp:
    transport: "stdio"
    command: "npx"
    args: ["-y", "@circleci/mcp-server-circleci"]
    env:
      CIRCLECI_TOKEN: "your-circleci-token"
      CIRCLECI_BASE_URL: "https://circleci.com"
  
  # Full configuration with all optional fields
  my_http_server:
    url: "https://my-mcp-server.com/mcp"
    transport: "http"
    description: "My custom MCP server"
    auth_type: "api_key"
    auth_value: "abc123"
```

**Configuration Options:**
- **Server Name**: Use any descriptive name for your MCP server (e.g., `zapier_mcp`, `deepwiki_mcp`, `circleci_mcp`)
- **server_id**: Optional stable id for the server. See [Pinning `server_id`](#pinning-server_id)
- **Alias**: This name will be prefilled with the server name with "_" replacing spaces, else edit it to be the prefix in tool names
- **URL**: The endpoint URL for your MCP server (required for HTTP/SSE transports)
- **Transport**: Defaults to `http` in `config.yaml`. Management API request models default to `sse`; set it explicitly when adding or updating a server. See [transport defaults](./mcp_config_reference#transport-matrix)
  - `sse` - SSE (Server-Sent Events) transport
  - `http` - Streamable HTTP transport
  - `stdio` - Standard Input/Output transport
- **Command**: The command to execute for stdio transport (required for stdio)
- **allow_all_keys**: Set to `true` to make the server available to every Lumina API key, even if the key/team doesn't list the server in its MCP permissions.
- **Args**: Array of arguments to pass to the command (optional for stdio)
- **Env**: Environment variables to set for the stdio process (optional for stdio)
- **Description**: Optional description for the server
- **Auth Type**: Optional authentication type. Supported values:

  See [MCP Non-OAuth Authentication](./mcp_authentication.md) for a choice guide, exact credential inputs, and upstream request examples.

  | Value | Header sent (managed SSE/HTTP transport) |
  |-------|-------------|
  | `none` | No auth header added |
  | `api_key` | `X-API-Key: <auth_value>` |
  | `bearer_token` | `Authorization: Bearer <auth_value>` |
  | `basic` | `Authorization: Basic <base64(auth_value)>`; enter `auth_value` as raw `username:password` |
  | `authorization` | `Authorization: <auth_value>` (verbatim, no prefix) |
  | `token` | `Authorization: token <auth_value>` (GitHub-style) |
  | `oauth2` | `Authorization: Bearer <resolved_token>` — PKCE or M2M `client_credentials`. See [MCP OAuth](./mcp_oauth.md) |
  | `oauth2_token_exchange` | `Authorization: Bearer <exchanged_token>` — RFC 8693 On-Behalf-Of. See [MCP OBO Auth](./mcp_obo_auth.md) |
  | `oauth2_id_jag` | `Authorization: Bearer <access_token>` — Identity Assertion Authorization Grant (two legs). See [MCP ID-JAG Auth](./mcp_id_jag.md) |
  | `true_passthrough` | The client's upstream `Authorization`, forwarded verbatim. See [MCP OAuth Passthrough](./mcp_oauth_passthrough.md) |
  | `oauth_delegate` | A distinct client-supplied upstream bearer, after Lumina admission. See [MCP OAuth Passthrough](./mcp_oauth_passthrough.md) |
  | `aws_sigv4` | Per-request AWS SigV4 signature. See [MCP AWS SigV4](./mcp_aws_sigv4.md) |

  The header shown above is the default. Set `upstream_token_header` on the server to send the resolved token somewhere other than `Authorization`, which is what an MCP server behind an API gateway usually needs. See [MCP OAuth](./mcp_oauth.md#sending-the-token-on-a-different-header)

  Note: the header table above describes the managed SSE/HTTP transport path. The OpenAPI-tool path emits `Authorization: ApiKey <value>` instead of `X-API-Key` for `auth_type: api_key`; the deprecated `x-mcp-auth` broadcast header also uses the `ApiKey` form.

- **Extra Headers**: Optional list of additional header names that should be forwarded from client to the MCP server
- **Static Headers**: Optional map of header key/value pairs to include every request to the MCP server.

For `auth_type: oauth2`, `oauth2_flow` is required: use `client_credentials` for a service identity or `authorization_code` for per-user sign-in. Missing or invalid flows prevent proxy startup. See [MCP OAuth](./mcp_oauth#config-reference)

Examples for each auth type:

```yaml title="MCP auth examples (config.yaml)" showLineNumbers
mcp_servers:
  api_key_example:
    url: "https://my-mcp-server.com/mcp"
    auth_type: "api_key"
    auth_value: "abc123"        # headers={"X-API-Key": "abc123"}

  # OAuth 2.0 client credentials (machine-to-machine)
  oauth2_example:
    url: "https://my-mcp-server.com/mcp"
    transport: "http"
    auth_type: "oauth2"
    oauth2_flow: "client_credentials"
    token_url: "https://my-mcp-server.com/oauth/token"
    client_id: os.environ/OAUTH_CLIENT_ID
    client_secret: os.environ/OAUTH_CLIENT_SECRET
    scopes: ["tool.read", "tool.write"] # optional override

  bearer_example:
    url: "https://my-mcp-server.com/mcp"
    auth_type: "bearer_token"
    auth_value: "abc123"        # headers={"Authorization": "Bearer abc123"}

  basic_example:
    url: "https://my-mcp-server.com/mcp"
    auth_type: "basic"
    auth_value: "user:pass"  # headers={"Authorization": "Basic dXNlcjpwYXNz"}

  custom_auth_example:
    url: "https://my-mcp-server.com/mcp"
    auth_type: "authorization"
    auth_value: "Token example123"  # headers={"Authorization": "Token example123"}

  # AWS SigV4 for Bedrock AgentCore MCP servers
  agentcore_mcp:
    url: "https://bedrock-agentcore.us-east-1.amazonaws.com/runtimes/<url-encoded-ARN>/invocations"
    transport: "http"
    auth_type: "aws_sigv4"
    aws_role_name: os.environ/AWS_ROLE_ARN          # optional — IAM role to assume
    aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID  # optional — falls back to IAM role
    aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
    aws_region_name: us-east-1
    aws_service_name: bedrock-agentcore

  # Example with extra headers forwarding
  github_mcp:
    url: "https://api.githubcopilot.com/mcp"
    auth_type: "bearer_token"
    auth_value: "ghp_example_token"
    extra_headers: ["custom_key", "x-custom-header"]  # These headers will be forwarded from client

  # Example with static headers
  my_mcp_server:
    url: "https://my-mcp-server.com/mcp"
    static_headers: # These headers will be requested to the MCP server
      X-API-Key: "abc123"
      X-Custom-Header: "some-value"
```

### Pinning `server_id`

Lumina derives a config server's id from its name and connection settings. If you change those settings, the id changes and existing key or team permissions stop matching.

Set `server_id` to keep the same id when the server changes:

```yaml
mcp_servers:
  internal_docs:
    server_id: "internal-docs"
    url: "https://docs.internal.example/mcp"
    transport: "http"
```

If the server already has permissions, use its current id from `GET /v1/mcp/server` or the Admin UI, then set that exact value as `server_id`:

```bash
curl -s http://localhost:4000/v1/mcp/server \
  -H "Authorization: Bearer $LUMINA_API_KEY"
```

`server_id` must be a non-empty string. Config entries cannot reuse an id or another entry's name or alias. Clashes with a database-backed server only log a warning: if the id matches, the database server wins and the config one is unreachable, and if it matches that server's name or alias, permissions naming it reach the config server instead.

If `LUMINA_USE_SHORT_MCP_TOOL_PREFIX` is enabled, changing the id also changes the server's tool prefix. Servers added through the UI or `/v1/mcp/server` already have stable ids.

### MCP Walkthroughs

- **Strands (STDIO)** – [watch tutorial](https://screen.studio/share/ruv4D73F)

> Add it from the UI

```json title="strands-mcp" showLineNumbers
{
  "mcpServers": {
    "strands-agents": {
      "command": "uvx",
      "args": ["strands-agents-mcp-server"],
      "env": {
        "FASTMCP_LOG_LEVEL": "INFO"
      },
      "disabled": false,
      "autoApprove": ["search_docs", "fetch_doc"]
    }
  }
}
```

> config.yml

```yaml title="config.yml – strands MCP" showLineNumbers
mcp_servers:
  strands_mcp:
    transport: "stdio"
    command: "uvx"
    args: ["strands-agents-mcp-server"]
    env:
      FASTMCP_LOG_LEVEL: "INFO"
```


### MCP Aliases

You can define aliases for your MCP servers in the `lumina_settings` section. This allows you to:

1. **Map friendly names to server names**: Use shorter, more memorable aliases
2. **Override server aliases**: If a server doesn't have an alias defined, the system will use the first matching alias from `mcp_aliases`
3. **Ensure uniqueness**: Only the first alias for each server is used, preventing conflicts

**Example:**
```yaml
lumina_settings:
  mcp_aliases:
    "github": "github_mcp_server"      # Maps "github" alias to "github_mcp_server"
    "zapier": "zapier_mcp_server"      # Maps "zapier" alias to "zapier_mcp_server"
    "docs": "deepwiki_mcp_server"      # Maps "docs" alias to "deepwiki_mcp_server"
    "github_alt": "github_mcp_server"  # This will be ignored since "github" already maps to this server
```

**Benefits:**
- **Simplified tool access**: Use `github_create_issue` instead of `github_mcp_server_create_issue`
- **Consistent naming**: Standardize alias patterns across your organization
- **Easy migration**: Change server names without breaking existing tool references

</TabItem>
</Tabs>


## Converting OpenAPI Specs to MCP Servers

Lumina can convert OpenAPI specifications into MCP servers, exposing any REST API as MCP tools without writing custom server code.

See the **[MCP from OpenAPI Specs guide](./mcp_openapi.md)** for full setup, usage examples, and how to override tool names and descriptions.

## MCP OAuth

Lumina supports OAuth 2.0 for MCP servers -- both interactive (PKCE) flows for user-facing clients and machine-to-machine (M2M) `client_credentials` for backend services.

See the **[MCP OAuth guide](./mcp_oauth.md)** for setup instructions, sequence diagrams, and a test server.

<details>
<summary>Detailed OAuth reference (click to expand)</summary>

Lumina v 1.77.6 added support for OAuth 2.0 Client Credentials for MCP servers.

You can configure this either in `config.yaml` or directly from the Lumina UI (MCP Servers → Authentication → OAuth). Every `auth_type: oauth2` server must declare its flow via `oauth2_flow`: `authorization_code` for interactive browser sign-in (shown below) or `client_credentials` for machine-to-machine tokens.

```yaml
mcp_servers:
  github_mcp:
    url: "https://api.githubcopilot.com/mcp"
    auth_type: oauth2
    oauth2_flow: authorization_code
    client_id: os.environ/GITHUB_OAUTH_CLIENT_ID
    client_secret: os.environ/GITHUB_OAUTH_CLIENT_SECRET
```

[**See Claude Code Tutorial**](/docs/tutorials/claude_responses_api)

### How It Works

```mermaid
sequenceDiagram
    participant Browser as User-Agent (Browser)
    participant Client as Client
    participant Lumina as Lumina Proxy
    participant MCP as MCP Server (Resource Server)
    participant Auth as Authorization Server

    Note over Client,Lumina: Step 1 – Resource discovery
    Client->>Lumina: GET /.well-known/oauth-protected-resource/{mcp_server_name}/mcp
    Lumina->>Client: Return resource metadata

    Note over Client,Lumina: Step 2 – Authorization server discovery
    Client->>Lumina: GET /.well-known/oauth-authorization-server/{mcp_server_name}
    Lumina->>Client: Return authorization server metadata

    Note over Client,Auth: Step 3 – Dynamic client registration
    Client->>Lumina: POST /{mcp_server_name}/register
    Lumina->>Auth: Forward registration request
    Auth->>Lumina: Issue client credentials
    Lumina->>Client: Return client credentials

    Note over Client,Browser: Step 4 – User authorization (PKCE)
    Client->>Browser: Open authorization URL + code_challenge + resource
    Browser->>Auth: Authorization request
    Note over Auth: User authorizes
    Auth->>Browser: Redirect with authorization code
    Browser->>Lumina: Callback to Lumina with code
    Lumina->>Browser: Redirect back with authorization code
    Browser->>Client: Callback with authorization code

    Note over Client,Auth: Step 5 – Token exchange
    Client->>Lumina: Token request + code_verifier + resource
    Lumina->>Auth: Forward token request
    Auth->>Lumina: Access (and refresh) token
    Lumina->>Client: Return tokens

    Note over Client,MCP: Step 6 – Authenticated MCP call
    Client->>Lumina: MCP request with access token + Lumina API key
    Lumina->>MCP: MCP request with Bearer token
    MCP-->>Lumina: MCP response
    Lumina-->>Client: Return MCP response
```

**Participants**

- **Client** – The MCP-capable AI agent (e.g., Claude Code, Cursor, or another IDE/agent) that initiates OAuth discovery, authorization, and tool invocations on behalf of the user.
- **Lumina Proxy** – Mediates all OAuth discovery, registration, token exchange, and MCP traffic while protecting stored credentials.
- **Authorization Server** – Issues OAuth 2.0 tokens via dynamic client registration, PKCE authorization, and token endpoints.
- **MCP Server (Resource Server)** – The protected MCP endpoint that receives Lumina’s authenticated JSON-RPC requests.
- **User-Agent (Browser)** – Temporarily involved so the end user can grant consent during the authorization step.

**Flow Steps**

1. **Resource Discovery**: The client fetches MCP resource metadata from Lumina’s `.well-known/oauth-protected-resource` endpoint to understand scopes and capabilities.
2. **Authorization Server Discovery**: The client retrieves the OAuth server metadata (token endpoint, authorization endpoint, supported PKCE methods) through Lumina’s `.well-known/oauth-authorization-server` endpoint.
3. **Dynamic Client Registration**: The client registers through Lumina, which forwards the request to the authorization server (RFC 7591). If the provider doesn’t support dynamic registration, you can pre-store `client_id`/`client_secret` in Lumina (e.g., GitHub MCP) and the flow proceeds the same way.
4. **User Authorization**: The client launches a browser session (with code challenge and resource hints). The user approves access, the authorization server sends the code through Lumina back to the client.
5. **Token Exchange**: The client calls Lumina with the authorization code, code verifier, and resource. Lumina exchanges them with the authorization server and returns the issued access/refresh tokens.
6. **MCP Invocation**: With a valid token, the client sends the MCP JSON-RPC request (plus Lumina API key) to Lumina, which forwards it to the MCP server and relays the tool response.

See the official [MCP Authorization Flow](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#authorization-flow-steps) for additional reference.

</details>


## Forwarding Custom Headers to MCP Servers

Lumina supports forwarding additional custom headers from MCP clients to backend MCP servers using the `extra_headers` configuration parameter. This allows you to pass custom authentication tokens, API keys, or other headers that your MCP server requires.

**Configuration**


<Tabs>
<TabItem value="config" label="config.yaml">
Configure `extra_headers` in your MCP server configuration to specify which header names should be forwarded:

```yaml title="config.yaml with extra_headers" showLineNumbers
mcp_servers:
  github_mcp:
    url: "https://api.githubcopilot.com/mcp"
    auth_type: "bearer_token"
    auth_value: "ghp_default_token"
    extra_headers: ["custom_key", "x-custom-header", "Authorization"]
    description: "GitHub MCP server with custom header forwarding"
```
</TabItem>
<TabItem value="clientside" label="Dynamically on Client Side">

Use this when giving users access to a [group of MCP servers](/docs/mcp#control-mcp-access-for-end-users).

**Format:** `x-mcp-{server_alias}-{header_name}: value`

This allows you to use different authentication for different MCP servers.


**Examples:**
- `x-mcp-github-authorization: Bearer ghp_xxxxxxxxx` - GitHub MCP server with Bearer token
- `x-mcp-zapier-x-api-key: sk-xxxxxxxxx` - Zapier MCP server with API key
- `x-mcp-deepwiki-authorization: Basic base64_encoded_creds` - DeepWiki MCP server with Basic auth

If every server in an access group takes the same credential, send it once as `x-mcp-{access_group}-{header_name}` and Lumina forwards it to each server whose `access_groups` contains that group. A server-specific `x-mcp-{server_alias}-{header_name}` header still wins for that server, and servers outside the group never receive the group credential. When a server belongs to several groups and those groups carry different credentials, Lumina forwards none of them.

```python title="Python Client with Server-Specific Auth" showLineNumbers
from fastmcp import Client
import asyncio

# Standard MCP configuration with multiple servers
config = {
    "mcpServers": {
        "mcp_group": {
            "url": "http://localhost:4000/mcp/",
            "headers": {
                "x-mcp-servers": "dev_group", # assume this gives access to github, zapier and deepwiki
                "x-lumina-api-key": "Bearer sk-<your-lumina-api-key>",
                "x-mcp-github-authorization": "Bearer gho_token", 
                "x-mcp-zapier-x-api-key": "sk-xxxxxxxxx",
                "x-mcp-deepwiki-authorization": "Basic base64_encoded_creds",
                "custom_key": "value"
            }
        }
    }
}

# Create a client that connects to all servers
client = Client(config)


async def main():
    async with client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        # call mcp 
        await client.call_tool(
            name="github_mcp-search_issues",
            arguments={'query': 'created:>2024-01-01', 'sort': 'created', 'order': 'desc', 'perPage': 30}
        )

if __name__ == "__main__":
    asyncio.run(main())

```



**Benefits:**
- **Server-specific authentication**: Each MCP server can use different auth methods
- **Better security**: No need to share the same auth token across all servers
- **Flexible header names**: Support for different auth header types (authorization, x-api-key, etc.)
- **Clean separation**: Each server's auth is clearly identified



</TabItem>
</Tabs>


#### Client Usage

When connecting from MCP clients, include the custom headers that match the `extra_headers` configuration:

<Tabs>
<TabItem value="fastmcp" label="Python FastMCP">

```python title="FastMCP Client with Custom Headers" showLineNumbers
from fastmcp import Client
import asyncio

# MCP client configuration with custom headers
config = {
    "mcpServers": {
        "github": {
            "url": "http://localhost:4000/github_mcp/mcp",
            "headers": {
                "x-lumina-api-key": "Bearer sk-<your-lumina-api-key>",
                "Authorization": "Bearer gho_token", 
                "custom_key": "custom_value",
                "x-custom-header": "additional_data"
            }
        }
    }
}

# Create a client that connects to the server
client = Client(config)

async def main():
    async with client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Call a tool if available
        if tools:
            result = await client.call_tool(tools[0].name, {})
            print(f"Tool result: {result}")

# Run the client
asyncio.run(main())
```

</TabItem>

<TabItem value="cursor" label="Cursor IDE">

```json title="Cursor MCP Configuration with Custom Headers" showLineNumbers
{
  "mcpServers": {
    "GitHub": {
      "url": "http://localhost:4000/github_mcp/mcp",
      "headers": {
        "x-lumina-api-key": "Bearer sk-<your-lumina-api-key>",
        "Authorization": "Bearer $GITHUB_TOKEN",
        "custom_key": "custom_value",
        "x-custom-header": "additional_data"
      }
    }
  }
}
```

</TabItem>

<TabItem value="http" label="HTTP Client">

```bash title="cURL with Custom Headers" showLineNumbers
curl --location 'http://localhost:4000/github_mcp/mcp' \
--header 'Content-Type: application/json' \
--header "x-lumina-api-key: Bearer $LUMINA_API_KEY" \
--header 'Authorization: Bearer gho_token' \
--header 'custom_key: custom_value' \
--header 'x-custom-header: additional_data' \
--data '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
}'
```

</TabItem>
</Tabs>

#### How It Works

1. **Configuration**: Define `extra_headers` in your MCP server config with the header names you want to forward
2. **Client Headers**: Include the corresponding headers in your MCP client requests
3. **Header Forwarding**: Lumina automatically forwards matching headers to the backend MCP server
4. **Authentication**: The backend MCP server receives both the configured auth headers and the custom headers


### Passing Request Headers to STDIO env Vars

If your stdio MCP server needs per-request credentials, you can map HTTP headers from the client request directly into the environment for the launched stdio process. Reference the header name in the env value using the `${X-HEADER_NAME}` syntax. Lumina will read that header from the incoming request and set the env var before starting the command.

```json title="Forward X-GITHUB_PERSONAL_ACCESS_TOKEN header to stdio env" showLineNumbers
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${X-GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

In this example, when a client makes a request with the `X-GITHUB_PERSONAL_ACCESS_TOKEN` header, the proxy forwards that value into the stdio process as the `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable.

## Control MCP Access for End Users

Control which MCP servers end users of your AI application can access (e.g. users of an internal chat UI). Pass the customer ID in the `x-lumina-end-user-id` header to:
- Enforce object permissions (limit which MCP servers they can access)
- Apply customer-specific budgets
- Track spend per customer

**FastMCP Client Example:**

```python title="Track customer spend with x-lumina-end-user-id" showLineNumbers
from fastmcp import Client
import asyncio

# MCP client configuration with customer tracking
config = {
    "mcpServers": {
        "github": {
            "url": "http://localhost:4000/github_mcp/mcp",
            "headers": {
                "x-lumina-api-key": "Bearer sk-<your-lumina-api-key>",
                "x-lumina-end-user-id": "customer_123",  # CUSTOMER ID
                "Authorization": "Bearer gho_token"
            }
        }
    }
}

client = Client(config)

async def main():
    async with client:
        # All MCP calls will be tracked under customer_123
        tools = await client.list_tools()
        result = await client.call_tool(tools[0].name, {})
        print(f"Tool result: {result}")

asyncio.run(main())
```

**Cursor IDE Example:**

```json title="Cursor config with customer tracking" showLineNumbers
{
  "mcpServers": {
    "GitHub": {
      "url": "http://localhost:4000/github_mcp/mcp",
      "headers": {
        "x-lumina-api-key": "Bearer sk-<your-lumina-api-key>",
        "x-lumina-end-user-id": "customer_123"
      }
    }
  }
}
```

**What happens:**
- Customer-specific object permissions are enforced (only allowed MCP servers are accessible)
- Customer budgets are applied
- All tool calls are tracked under `customer_123`

[Learn more about customer management →](./proxy/customers)

## Calling the Proxy's /v1/responses Endpoint

When calling your Lumina Proxy's `/v1/responses` endpoint to use MCP tools, use `server_url: "lumina_proxy"` for all permitted servers, or `lumina_proxy/mcp/<server_alias>` for one server in the tools array. This tells the proxy to use its configured MCP servers.

:::important[Do not use the full proxy URL]
Using `server_url: "https://your-proxy.com/mcp"` is incorrect when the request is already going to the proxy. Use the [documented sentinel forms](./mcp_config_reference#endpoint-matrix) to route to configured MCP servers. Direct MCP clients use the network URL instead.
:::

```bash title="Correct: Using lumina_proxy" showLineNumbers
curl --location 'https://your-proxy.com/v1/responses' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $LUMINA_API_KEY" \
--data '{
    "model": "{{openai_large}}",
    "tools": [
        {
            "type": "mcp",
            "server_label": "lumina",
            "server_url": "lumina_proxy",
            "require_approval": "never"
        }
    ],
    "input": "Run available tools",
    "tool_choice": "required"
}'
```

### Sending Custom Headers to MCP Servers

To pass custom headers (e.g., API keys, auth tokens) to specific MCP servers, use either:

**Option 1: Request headers** – Add `x-mcp-{server_alias}-{header_name}` to your request headers. The proxy forwards these to the matching MCP server.

```bash
# Send Authorization header to the "weather2" MCP server
--header 'x-mcp-weather2-authorization: Bearer your-token'

# Send custom header to the "github" MCP server  
--header 'x-mcp-github-x-api-key: your-api-key'
```

**Option 2: Headers in tool config** – Include a `headers` object in the tool definition. These are merged with request headers.

```json
{
    "type": "mcp",
    "server_label": "lumina",
    "server_url": "lumina_proxy",
    "require_approval": "never",
    "headers": {
        "x-lumina-api-key": "Bearer YOUR_LUMINA_API_KEY",
        "x-mcp-servers": "Zapier_MCP,dev-group",
        "x-mcp-weather2-authorization": "Bearer your-weather-api-token"
    }
}
```

## Using your MCP with client side credentials

Use this if you want to pass a client side authentication token to Lumina to then pass to your MCP to auth to your MCP.


### New Server-Specific Auth Headers (Recommended)

You can specify MCP auth tokens using server-specific headers in the format `x-mcp-{server_alias}-{header_name}`. This allows you to use different authentication for different MCP servers.

**Benefits:**
- **Server-specific authentication**: Each MCP server can use different auth methods
- **Better security**: No need to share the same auth token across all servers
- **Flexible header names**: Support for different auth header types (authorization, x-api-key, etc.)
- **Clean separation**: Each server's auth is clearly identified

### Group-Level Auth Headers

When the servers in an access group share one credential, pass `x-mcp-{access_group}-{header_name}` once instead of repeating it per server. Lumina uses it as the default for every server whose `access_groups` includes that group. A server-specific `x-mcp-{server_alias}-{header_name}` header overrides it for that server, servers outside the group never receive it, and if a server is in several groups that carry different credentials none of them is forwarded. Server aliases and access group names share the `x-mcp-` header namespace, so a server whose alias equals a group name keeps receiving `x-mcp-{alias}-*` as its own credential; avoid naming a server after an access group it does not belong to.

```bash title="cURL Example with Group-Level Auth" showLineNumbers
curl -X POST http://localhost:4000/mcp/dev_group \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-lumina-api-key: Bearer $LUMINA_API_KEY" \
  -H "x-mcp-dev_group-authorization: Bearer SHARED_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### Client authentication {#legacy-auth-header-deprecated}

Replace the deprecated broadcast header with `x-mcp-{server_alias}-{header_name}`. See [legacy compatibility](./mcp_config_reference#deprecated-x-mcp-auth). The client examples below use scoped credentials

<Tabs>
<TabItem value="openai" label="OpenAI API">

#### Connect via OpenAI Responses API with Server-Specific Auth

When calling OpenAI directly, use a publicly reachable Lumina MCP URL and include the gateway key and scoped upstream headers:

```bash title="cURL Example with Server-Specific Auth" showLineNumbers
curl --location 'https://api.openai.com/v1/responses' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $OPENAI_API_KEY" \
--data '{
    "model": "{{openai_large}}",
    "tools": [
        {
            "type": "mcp",
            "server_label": "lumina",
            "server_url": "https://your-lumina-proxy.example.com/mcp",
            "require_approval": "never",
            "headers": {
                "x-lumina-api-key": "Bearer YOUR_LUMINA_API_KEY",
                "x-mcp-github-authorization": "Bearer YOUR_GITHUB_TOKEN",
                "x-mcp-zapier-x-api-key": "YOUR_ZAPIER_API_KEY"
            }
        }
    ],
    "input": "Run available tools",
    "tool_choice": "required"
}'
```

</TabItem>

<TabItem value="lumina" label="Lumina Proxy">

#### Connect via Lumina Proxy Responses API with Server-Specific Auth

Use this when calling Lumina Proxy for LLM API requests to `/v1/responses` endpoint with server-specific authentication:

```bash title="cURL Example with Server-Specific Auth" showLineNumbers
curl --location '<your-lumina-proxy-base-url>/v1/responses' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $LUMINA_API_KEY" \
--data '{
    "model": "{{openai_large}}",
    "tools": [
        {
            "type": "mcp",
            "server_label": "lumina",
            "server_url": "lumina_proxy",
            "require_approval": "never",
            "headers": {
                "x-lumina-api-key": "Bearer YOUR_LUMINA_API_KEY",
                "x-mcp-github-authorization": "Bearer YOUR_GITHUB_TOKEN",
                "x-mcp-zapier-x-api-key": "YOUR_ZAPIER_API_KEY"
            }
        }
    ],
    "input": "Run available tools",
    "tool_choice": "required"
}'
```

</TabItem>

<TabItem value="cursor" label="Cursor IDE">

#### Connect via Cursor IDE with Server-Specific Auth

Use tools directly from Cursor IDE with Lumina MCP and include server-specific authentication:

**Setup Instructions:**

1. **Open Cursor Settings**: Use `⇧+⌘+J` (Mac) or `Ctrl+Shift+J` (Windows/Linux)
2. **Navigate to MCP Tools**: Go to the "MCP Tools" tab and click "New MCP Server"
3. **Add Configuration**: Copy and paste the JSON configuration below, then save with `Cmd+S` or `Ctrl+S`

```json title="Cursor MCP Configuration with Server-Specific Auth" showLineNumbers
{
  "mcpServers": {
    "Lumina": {
      "url": "http://localhost:4000/mcp/",
      "headers": {
        "x-lumina-api-key": "Bearer sk-<your-lumina-api-key>",
        "x-mcp-github-authorization": "Bearer $GITHUB_TOKEN",
        "x-mcp-zapier-x-api-key": "$ZAPIER_API_KEY"
      }
    }
  }
}
```

</TabItem>

<TabItem value="http" label="Streamable HTTP">

#### Connect via Streamable HTTP Transport with Server-Specific Auth

Connect to Lumina MCP using HTTP transport with server-specific authentication:

**Server URL:**
```text showLineNumbers
http://localhost:4000/mcp/
```

**Headers:**
```text showLineNumbers
x-lumina-api-key: Bearer YOUR_LUMINA_API_KEY
x-mcp-github-authorization: Bearer YOUR_GITHUB_TOKEN
x-mcp-zapier-x-api-key: YOUR_ZAPIER_API_KEY
```

</TabItem>

<TabItem value="fastmcp" label="Python FastMCP">

#### Connect via Python FastMCP Client with Server-Specific Auth

Use the Python FastMCP client to connect to your Lumina MCP server with server-specific authentication:

```python title="Python FastMCP Example with Server-Specific Auth" showLineNumbers
import asyncio
import json

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

# Create the transport with your Lumina MCP server URL and server-specific auth headers
server_url = "http://localhost:4000/mcp/"
transport = StreamableHttpTransport(
    server_url,
    headers={
        "x-lumina-api-key": "Bearer YOUR_LUMINA_API_KEY",
        "x-mcp-github-authorization": "Bearer YOUR_GITHUB_TOKEN",
        "x-mcp-zapier-x-api-key": "YOUR_ZAPIER_API_KEY"
    }
)

# Initialize the client with the transport
client = Client(transport=transport)


async def main():
    # Connection is established here
    print("Connecting to Lumina MCP server with server-specific authentication...")
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        print("Fetching available tools...")
        tools = await client.list_tools()

        print(f"Available tools: {json.dumps([t.name for t in tools], indent=2)}")
        
        # Example: Call a tool (replace 'tool_name' with an actual tool name)
        if tools:
            tool_name = tools[0].name
            print(f"Calling tool: {tool_name}")
            
            # Call the tool with appropriate arguments
            result = await client.call_tool(tool_name, arguments={})
            print(f"Tool result: {result}")


# Run the example
if __name__ == "__main__":
    asyncio.run(main())
```

</TabItem>
</Tabs>

### Customize the MCP Auth Header Name

Existing deployments can rename the deprecated broadcast header. See the [central legacy header reference](./mcp_config_reference#deprecated-x-mcp-auth); new setups should use server-specific headers

## Use MCP tools with `/chat/completions`

:::tip[Works with all providers]
This flow is **provider-agnostic**: the same MCP tool definition works for _every_ LLM backend behind Lumina (OpenAI, Azure OpenAI, Anthropic, Amazon Bedrock, Vertex, self-hosted deployments, etc.).
:::

Lumina Proxy also supports MCP-aware tooling on the classic `/v1/chat/completions` endpoint. Provide the MCP tool definition directly in the `tools` array and Lumina will fetch and transform the MCP server's tools into OpenAI-compatible function calls. When `require_approval` is set to `"never"`, the proxy automatically executes the returned tool calls and feeds the results back into the model before returning the assistant response.

```bash title="Chat Completions with MCP Tools" showLineNumbers
curl --location '<your-lumina-proxy-base-url>/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $LUMINA_API_KEY" \
--data '{
  "model": "{{openai_small}}",
  "messages": [
    {"role": "user", "content": "Summarize the latest open PR."}
  ],
  "tools": [
    {
      "type": "mcp",
      "server_url": "lumina_proxy/mcp/github_mcp",
      "server_label": "github_mcp",
      "require_approval": "never"
    }
  ]
}'
```

If you omit `require_approval` or set it to any value other than `"never"`, the MCP tool calls are returned to the client so that you can review and execute them manually, matching the upstream OpenAI behavior.


## Lumina Proxy - Walk through MCP Gateway
Lumina exposes an MCP Gateway for admins to add all their MCP servers to Lumina. The key benefits of using Lumina Proxy with MCP are:

1. Use a fixed endpoint for all MCP tools
2. MCP Permission management by Key, Team, or User

This video demonstrates how you can onboard an MCP server to Lumina Proxy, use it and set access controls.

<iframe width="840" height="500" src="https://www.loom.com/embed/f7aa8d217879430987f3e64291757bfc" frameBorder="0" allowFullScreen></iframe>

## Lumina Python SDK MCP Bridge

Lumina Python SDK acts as a MCP bridge to use MCP tools with all Lumina supported models. Lumina offers the following features for using MCP

- **List** Available MCP Tools: OpenAI clients can view all available MCP tools
  - `lumina.experimental_mcp_client.load_mcp_tools` to list all available MCP tools
- **Call** MCP Tools: OpenAI clients can call MCP tools
  - `lumina.experimental_mcp_client.call_openai_tool` to call an OpenAI tool on an MCP server


### 1. List Available MCP Tools

In this example we'll use `lumina.experimental_mcp_client.load_mcp_tools` to list all available MCP tools on any MCP server. This method can be used in two ways:

- `format="mcp"` - (default) Return MCP tools 
  - Returns: `mcp.types.Tool`
- `format="openai"` - Return MCP tools converted to OpenAI API compatible tools. Allows using with OpenAI endpoints.
  - Returns: `openai.types.chat.ChatCompletionToolParam`

<Tabs>
<TabItem value="sdk" label="Lumina Python SDK">

```python title="MCP Client List Tools" showLineNumbers
# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import lumina
from lumina import experimental_mcp_client


server_params = StdioServerParameters(
    command="python3",
    # Make sure to update to the full absolute path to your mcp_server.py file
    args=["./mcp_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()

        # Get tools
        tools = await experimental_mcp_client.load_mcp_tools(session=session, format="openai")
        print("MCP TOOLS: ", tools)

        messages = [{"role": "user", "content": "what's (3 + 5)"}]
        llm_response = await lumina.acompletion(
            model="{{openai_large}}",
            api_key=os.getenv("OPENAI_API_KEY"),
            messages=messages,
            tools=tools,
        )
        print("LLM RESPONSE: ", json.dumps(llm_response, indent=4, default=str))
```

</TabItem>

<TabItem value="openai" label="OpenAI SDK + Lumina Proxy">

In this example we'll walk through how you can use the OpenAI SDK pointed to the Lumina proxy to call MCP tools. The key difference here is we use the OpenAI SDK to make the LLM API request

```python title="MCP Client List Tools" showLineNumbers
# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from openai import OpenAI
from lumina import experimental_mcp_client

server_params = StdioServerParameters(
    command="python3",
    # Make sure to update to the full absolute path to your mcp_server.py file
    args=["./mcp_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()

        # Get tools using lumina mcp client
        tools = await experimental_mcp_client.load_mcp_tools(session=session, format="openai")
        print("MCP TOOLS: ", tools)

        # Use OpenAI SDK pointed to Lumina proxy
        client = OpenAI(
            api_key="your-api-key",  # Your Lumina proxy API key
            base_url="http://localhost:4000"  # Your Lumina proxy URL
        )

        messages = [{"role": "user", "content": "what's (3 + 5)"}]
        llm_response = client.chat.completions.create(
            model="{{openai_large}}",
            messages=messages,
            tools=tools
        )
        print("LLM RESPONSE: ", llm_response)
```
</TabItem>
</Tabs>


### 2. List and Call MCP Tools

In this example we'll use 
- `lumina.experimental_mcp_client.load_mcp_tools` to list all available MCP tools on any MCP server
- `lumina.experimental_mcp_client.call_openai_tool` to call an OpenAI tool on an MCP server

The first llm response returns a list of OpenAI tools. We take the first tool call from the LLM response and pass it to `lumina.experimental_mcp_client.call_openai_tool` to call the tool on the MCP server.

#### How `lumina.experimental_mcp_client.call_openai_tool` works

- Accepts an OpenAI Tool Call from the LLM response
- Converts the OpenAI Tool Call to an MCP Tool
- Calls the MCP Tool on the MCP server
- Returns the result of the MCP Tool call

<Tabs>
<TabItem value="sdk" label="Lumina Python SDK">

```python title="MCP Client List and Call Tools" showLineNumbers
# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import lumina
from lumina import experimental_mcp_client


server_params = StdioServerParameters(
    command="python3",
    # Make sure to update to the full absolute path to your mcp_server.py file
    args=["./mcp_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()

        # Get tools
        tools = await experimental_mcp_client.load_mcp_tools(session=session, format="openai")
        print("MCP TOOLS: ", tools)

        messages = [{"role": "user", "content": "what's (3 + 5)"}]
        llm_response = await lumina.acompletion(
            model="{{openai_large}}",
            api_key=os.getenv("OPENAI_API_KEY"),
            messages=messages,
            tools=tools,
        )
        print("LLM RESPONSE: ", json.dumps(llm_response, indent=4, default=str))

        openai_tool = llm_response["choices"][0]["message"]["tool_calls"][0]
        # Call the tool using MCP client
        call_result = await experimental_mcp_client.call_openai_tool(
            session=session,
            openai_tool=openai_tool,
        )
        print("MCP TOOL CALL RESULT: ", call_result)

        # send the tool result to the LLM
        messages.append(llm_response["choices"][0]["message"])
        messages.append(
            {
                "role": "tool",
                "content": str(call_result.content[0].text),
                "tool_call_id": openai_tool["id"],
            }
        )
        print("final messages with tool result: ", messages)
        llm_response = await lumina.acompletion(
            model="{{openai_large}}",
            api_key=os.getenv("OPENAI_API_KEY"),
            messages=messages,
            tools=tools,
        )
        print(
            "FINAL LLM RESPONSE: ", json.dumps(llm_response, indent=4, default=str)
        )
```

</TabItem>
<TabItem value="proxy" label="OpenAI SDK + Lumina Proxy">

In this example we'll walk through how you can use the OpenAI SDK pointed to the Lumina proxy to call MCP tools. The key difference here is we use the OpenAI SDK to make the LLM API request

```python title="MCP Client with OpenAI SDK" showLineNumbers
# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from openai import OpenAI
from lumina import experimental_mcp_client

server_params = StdioServerParameters(
    command="python3",
    # Make sure to update to the full absolute path to your mcp_server.py file
    args=["./mcp_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize the connection
        await session.initialize()

        # Get tools using lumina mcp client
        tools = await experimental_mcp_client.load_mcp_tools(session=session, format="openai")
        print("MCP TOOLS: ", tools)

        # Use OpenAI SDK pointed to Lumina proxy
        client = OpenAI(
            api_key="your-api-key",  # Your Lumina proxy API key
            base_url="http://localhost:4000"  # Your Lumina proxy URL
        )

        messages = [{"role": "user", "content": "what's (3 + 5)"}]
        llm_response = client.chat.completions.create(
            model="{{openai_large}}",
            messages=messages,
            tools=tools
        )
        print("LLM RESPONSE: ", llm_response)

        # Get the first tool call
        tool_call = llm_response.choices[0].message.tool_calls[0]
        
        # Call the tool using MCP client
        call_result = await experimental_mcp_client.call_openai_tool(
            session=session,
            openai_tool=tool_call.model_dump(),
        )
        print("MCP TOOL CALL RESULT: ", call_result)

        # Send the tool result back to the LLM
        messages.append(llm_response.choices[0].message.model_dump())
        messages.append({
            "role": "tool",
            "content": str(call_result.content[0].text),
            "tool_call_id": tool_call.id,
        })

        final_response = client.chat.completions.create(
            model="{{openai_large}}",
            messages=messages,
            tools=tools
        )
        print("FINAL RESPONSE: ", final_response)
```

</TabItem>
</Tabs>

## FAQ

**Q: How do I use OAuth2 client_credentials (machine-to-machine) with MCP servers behind Lumina?**

Lumina supports automatic token management for the `client_credentials` grant. Configure `client_id`, `client_secret`, and `token_url` on your MCP server and Lumina will fetch, cache, and refresh tokens automatically. See the [MCP OAuth M2M guide](./mcp_oauth.md#machine-to-machine-m2m-auth) for setup instructions.

**Q: When I fetch an OAuth token from the Lumina UI, where is it stored?**

The UI keeps only transient state in `sessionStorage` so the OAuth redirect flow can finish; the token is not persisted in the server or database.

**Q: I'm seeing MCP connection errors. What should I check?**

Start with the [five-minute triage](./mcp_troubleshoot.md#locate-the-error-source) in the MCP Troubleshooting Guide: one curl isolates the failing layer (Client → Lumina vs. Lumina → MCP), and the [symptom matrix](./mcp_troubleshoot.md#symptom-matrix) maps each status code and symptom to its fix. If you need to escalate, collect the [support bundle](./mcp_troubleshoot.md#support-bundle) first.
