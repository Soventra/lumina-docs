import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Ramp

Send AI usage and cost data to Ramp for automated spend tracking.

[Ramp](https://ramp.com/) is a finance automation platform that helps businesses manage expenses, corporate cards, and vendor payments. With the Ramp callback integration, your Lumina AI usage, including token counts, model costs, and request metadata, is automatically sent to Ramp for real-time spend visibility.

:::info
We want to learn how we can make the callbacks better! Meet the Lumina [founders](https://calendly.com/d/4mp-gd3-k5k/berriai-1-1-onboarding-lumina-hosted-version) or
join our [discord](https://discord.gg/wuPM9dRgDw)
:::

## Pre-Requisites

1. Log in to [Ramp](https://app.ramp.com/) and search for **"Lumina"** using the search bar. Click the **Lumina** integration result.

> **Note:** Only business owners and admins can access and configure integrations.

2. On the Lumina integration page, click the **Connect** button in the top right.

3. In the Connect Lumina drawer, click **Generate API Key** to create an API key.

> **Important:** Copy the API key immediately, because it won't be shown again. If you lose it, you can revoke the existing key and generate a new one from the integration settings.

```shell
pip install lumina
```

## Quick Start

Set your `RAMP_API_KEY` and add `"ramp"` to your callbacks to start logging LLM usage to Ramp.

<Tabs>
<TabItem value="python" label="SDK">

```python
lumina.callbacks = ["ramp"]
```

```python
import lumina
import os

# Ramp API Key
os.environ["RAMP_API_KEY"] = "your-ramp-api-key"

# LLM API Keys
os.environ['OPENAI_API_KEY'] = ""

# Set ramp as a callback
lumina.callbacks = ["ramp"]

# OpenAI call
response = lumina.completion(
  model="{{openai_small}}",
  messages=[
    {"role": "user", "content": "Hi - I'm testing Ramp integration"}
  ]
)
```

</TabItem>
<TabItem value="proxy" label="Lumina Proxy">

1. Setup config.yaml

```yaml
model_list:
  - model_name: {{openai_small}}
    lumina_params:
      model: openai/{{openai_small}}
      api_key: os.environ/OPENAI_API_KEY

lumina_settings:
  callbacks: ["ramp"]

environment_variables:
  RAMP_API_KEY: os.environ/RAMP_API_KEY
```

2. Start Lumina Proxy

```bash
lumina --config /path/to/config.yaml
```

3. Test it!

```bash
curl -L -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H "Authorization: Bearer $LUMINA_API_KEY" \
-d '{
  "model": "{{openai_small}}",
  "messages": [
    {
      "role": "user",
      "content": "Hey, how are you?"
    }
  ]
}'
```

</TabItem>
</Tabs>

## What Data is Logged?

Lumina sends the [Standard Logging Payload](https://docs.lumina.ai/docs/proxy/logging_spec) to Ramp on successful LLM API calls, which includes:

- **Request details**: Model, messages, parameters
- **Response details**: Completion text, token usage, latency
- **Metadata**: User ID, custom metadata, timestamps
- **Cost tracking**: Response cost based on token usage

## Authentication

Set the `RAMP_API_KEY` environment variable with your Ramp API key.

| Environment Variable | Description |
|---|---|
| `RAMP_API_KEY` | Your Ramp API key (required) |

## Support & Talk to Founders

- [Schedule Demo](https://calendly.com/d/4mp-gd3-k5k/berriai-1-1-onboarding-lumina-hosted-version)
- [Community Discord](https://discord.gg/wuPM9dRgDw)
- Our numbers +1 (770) 8783-106 / ‭+1 (412) 618-6238‬
- Our emails ishaan@berri.ai / krrish@berri.ai
