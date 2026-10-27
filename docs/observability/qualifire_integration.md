import Image from '@theme/IdealImage';

# Qualifire

[Qualifire](https://qualifire.ai/) provides real-time Agentic evaluations, guardrails and observability for production AI applications.

**Key Features:**

- **Evaluation** - Systematically assess AI behavior to detect hallucinations, jailbreaks, policy breaches, and other vulnerabilities
- **Guardrails** - Real-time interventions to prevent risks like brand damage, data leaks, and compliance breaches
- **Observability** - Complete tracing and logging for RAG pipelines, chatbots, and AI agents
- **Prompt Management** - Centralized prompt management with versioning and no-code studio

:::tip

Looking for Qualifire Guardrails? Check out the [Qualifire Guardrails Integration](../proxy/guardrails/qualifire.md) for real-time content moderation, prompt injection detection, PII checks, and more.

:::

## Pre-Requisites

1. Create an account on [Qualifire](https://app.qualifire.ai/)
2. Get your API key and webhook URL from the Qualifire dashboard

```bash
uv add lumina
```

## Quick Start

Use just 2 lines of code to instantly log your responses **across all providers** with Qualifire.

```python
lumina.callbacks = ["qualifire_eval"]
```

```python
import lumina
import os

# Set Qualifire credentials
os.environ["QUALIFIRE_API_KEY"] = "your-qualifire-api-key"
os.environ["QUALIFIRE_WEBHOOK_URL"] = "https://your-qualifire-webhook-url"

# LLM API Keys
os.environ['OPENAI_API_KEY'] = "your-openai-api-key"

# Set qualifire_eval as a callback & Lumina will send the data to Qualifire
lumina.callbacks = ["qualifire_eval"]

# OpenAI call
response = lumina.completion(
  model="{{openai_large}}",
  messages=[
    {"role": "user", "content": "Hi - i'm openai"}
  ]
)
```

## Using with Lumina Proxy

1. Setup config.yaml

```yaml
model_list:
  - model_name: {{openai_large}}
    lumina_params:
      model: openai/{{openai_large}}
      api_key: os.environ/OPENAI_API_KEY

lumina_settings:
  callbacks: ["qualifire_eval"]

general_settings:
  master_key: "sk-<your-lumina-master-key>"

environment_variables:
  QUALIFIRE_API_KEY: "your-qualifire-api-key"
  QUALIFIRE_WEBHOOK_URL: "https://app.qualifire.ai/api/v1/webhooks/evaluations"
```

2. Start the proxy

```bash
lumina --config config.yaml
```

3. Test it!

```bash
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H "Authorization: Bearer $LUMINA_API_KEY" \
-d '{ "model": "{{openai_large}}", "messages": [{"role": "user", "content": "Hi - i'm openai"}]}'
```

## Environment Variables

| Variable                | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| `QUALIFIRE_API_KEY`     | Your Qualifire API key for authentication              |
| `QUALIFIRE_WEBHOOK_URL` | The Qualifire webhook endpoint URL from your dashboard |

## What Gets Logged?

The [Lumina Standard Logging Payload](https://docs.lumina.ai/docs/proxy/logging_spec) is sent to your Qualifire endpoint on each successful LLM API call.

This includes:

- Request messages and parameters
- Response content and metadata
- Token usage statistics
- Latency metrics
- Model information
- Cost data

Once data is in Qualifire, you can:

- Run evaluations to detect hallucinations, toxicity, and policy violations
- Set up guardrails to block or modify responses in real-time
- View traces across your entire AI pipeline
- Track performance and quality metrics over time
