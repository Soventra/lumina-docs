# OpenClaw + Lumina Integration

[OpenClaw](https://openclaw.ai) is a self-hosted AI assistant that connects chat apps (WhatsApp, Telegram, Discord, and more) to LLM providers. By routing OpenClaw through Lumina Proxy, you get access to 100+ providers, cost tracking, spend limits, and automatic failover, all from a single gateway.

## What you'll set up

```
Chat apps → OpenClaw Gateway → Lumina Proxy → LLM Providers (OpenAI, Anthropic, etc.)
```

## Prerequisites

| Requirement | How to get it |
|---|---|
| **Node.js 22+** | `node --version` — install from [nodejs.org](https://nodejs.org) if needed |
| **Python {{python_min_version}}+** | `python --version` |
| **At least one LLM API key** | OpenAI, Anthropic, Gemini, etc. |

## Step 1: Install Lumina Proxy

```bash
uv tool install 'lumina[proxy]'
```

## Step 2: Create a Lumina config file

Create a config file  `lumina_config.yaml` with the models you want to use. Here's an example with OpenAI:

```yaml title="lumina_config.yaml"
model_list:
  - model_name: {{openai_large}}
    lumina_params:
      model: openai/{{openai_large}}
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: sk-your-secret-key  # pick any value — this is YOUR proxy password
```

:::tip[Multi-provider example]
You can add as many models as you want from different providers:

```yaml title="lumina_config.yaml"
model_list:
  - model_name: {{openai_large}}
    lumina_params:
      model: openai/{{openai_large}}
      api_key: os.environ/OPENAI_API_KEY

  - model_name: claude-sonnet
    lumina_params:
      model: anthropic/{{anthropic}}
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gemini-flash
    lumina_params:
      model: gemini/{{gemini_flash}}
      api_key: os.environ/GEMINI_API_KEY

general_settings:
  master_key: sk-your-secret-key
```

See [Lumina proxy config docs](https://docs.lumina.ai/docs/proxy/configs) for all options.
:::

## Step 3: Start the proxy

Make sure your API key(s) are available as environment variables (via `export`, `.env` file, or however you manage secrets), then start the proxy:

```bash
lumina --config lumina_config.yaml --port 4000
```

## Step 4: Install OpenClaw

```bash
# macOS / Linux
curl -fsSL https://openclaw.ai/install.sh | bash
```

:::note[Windows]
On Windows, use PowerShell: `iwr -useb https://openclaw.ai/install.ps1 | iex`

WSL2 is recommended over native Windows.
:::

## Step 5: Connect OpenClaw to Lumina

Run the onboarding wizard:

```bash
openclaw onboard --install-daemon
```

When prompted:

1. Choose **QuickStart** or **Manual** as the onboarding mode (both work; Manual gives you more options for gateway settings)
2. Select **Lumina** as the model/auth provider
3. Enter your Lumina `master_key` from Step 2 and set the base URL to your proxy address (e.g., `http://localhost:4000`)
4. When asked for the default model, choose **Enter model manually** and type the model name from your `lumina_config.yaml` (e.g., `lumina/{{openai_large}}`)

You can also set or change the model after onboarding:

```bash
openclaw models set lumina/{{openai_large}}
```

For scripted / CI environments, you can skip the prompts entirely:

```bash
openclaw onboard --non-interactive --accept-risk \
  --auth-choice lumina-api-key \
  --lumina-api-key "sk-your-secret-key" \
  --custom-base-url "http://localhost:4000" \
  --install-daemon --skip-channels --skip-skills
```

## Step 6: Verify

Check the gateway is healthy:

```bash
openclaw health
```

Then send a test message:

```bash
openclaw dashboard                                           # web UI
openclaw tui                                                 # terminal UI
openclaw agent --agent main -m "Hello, what model are you?"  # one-shot CLI
```

If you get a response from your model, the integration is working.

Check which model is active:

```bash
openclaw models status
```

## Config reference

After onboarding, OpenClaw stores the Lumina provider config in `~/.openclaw/openclaw.json`. The relevant sections are something like this:

```json5 title="~/.openclaw/openclaw.json (excerpt)"
{
  "models": {
    "providers": {
      "lumina": {
        "baseUrl": "http://localhost:4000",
        "apiKey": "sk-your-secret-key",
        "api": "openai-completions",
        "models": [
          {
            "id": "{{openai_large}}",
            "name": "GPT-5.6 Terra via Lumina"
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "lumina/{{openai_large}}" }
    }
  }
}
```

You can edit this file directly to add more models or change the `baseUrl`. OpenClaw hot-reloads changes automatically.

## Troubleshooting

**Connection refused / proxy not reachable**

Make sure the Lumina proxy is running and that the `baseUrl` in your OpenClaw config matches:

```bash
curl http://localhost:4000/health -H "Authorization: Bearer sk-your-secret-key"
```

**Wrong model or "Invalid model name"**

The model name in OpenClaw must match a `model_name` from your `lumina_config.yaml`. Switch the active model with:

```bash
openclaw models set lumina/{{openai_large}}
```

**Gateway pairing issues after reinstall**

If the CLI can't connect to the gateway after a reinstall, stop the service and reinstall it:

```bash
openclaw gateway stop
openclaw gateway install
```

## References

- [OpenClaw docs](https://docs.openclaw.ai)
- [OpenClaw Lumina provider docs](https://docs.openclaw.ai/providers/lumina)
- [OpenClaw model providers](https://docs.openclaw.ai/concepts/model-providers)
- [Lumina proxy configuration](https://docs.lumina.ai/docs/proxy/configs)
