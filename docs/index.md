---
id: index
title: Getting Started
sidebar_label: Quickstart
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import NavigationCards from '@site/src/components/NavigationCards';
import LuminaFlow from '@site/src/components/LuminaFlow';
import QuickStartBox from '@site/src/components/QuickStartBox';

<LuminaFlow copyCommand={false} agentPrompt={false} />

<QuickStartBox source="docs-index" />

**Lumina** is an open-source library that gives you a single, unified interface to call 100+ LLMs (OpenAI, Anthropic, Vertex AI, Bedrock, and more) using the OpenAI format.

- Call any provider using the same `completion()` interface, with no API to re-learn for each one
- Consistent output format regardless of which provider or model you use
- Built-in retry / fallback logic across multiple deployments via the [Router](./routing.md)
- Self-hosted [LLM Gateway (Proxy)](/docs/simple_proxy) with virtual keys, cost tracking, and an admin UI

[![PyPI](https://img.shields.io/pypi/v/lumina.svg)](https://pypi.org/project/lumina/)
[![GitHub Stars](https://img.shields.io/github/stars/Soventra/lumina?style=social)](https://github.com/Soventra/lumina)

---

## Installation

```shell
uv add lumina
```

### A leaner SDK installation

For applications that use the Python SDK directly, `lumina-core` provides the shared SDK with fewer mandatory dependencies and without the bundled dashboard or gateway CLI entry points. Python imports remain unchanged: continue using `lumina`

Install `lumina-core` in a fresh environment instead of installing `lumina`. Add AWS and Python Hugging Face tokenizer packages when your application needs them. The two distributions cannot be installed together because they share the same Python files

See [Lumina Core](https://docs.lumina.ai/docs/lumina_core) for installation, package selection, and optional dependencies. Existing `lumina` installations retain their current dependency defaults

To deploy the full AI Gateway (Proxy) with the Admin UI, follow the [Quickstart](./proxy/docker_quick_start.md); it runs as a container and needs no Python setup. To run it from the CLI instead, see the [Gateway Quickstart](./learn/gateway_quickstart.md).

---

## Quick Start

Make your first LLM call using the provider of your choice:

<Tabs>
<TabItem value="openai" label="OpenAI">

```python
from lumina import completion
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"

response = completion(
  model="openai/{{openai_large}}",
  messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)
```

</TabItem>
<TabItem value="anthropic" label="Anthropic">

```python
from lumina import completion
import os

os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

response = completion(
  model="anthropic/{{anthropic}}",
  messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)
```

</TabItem>
<TabItem value="vertex" label="Vertex AI">

```python
from lumina import completion
import os

# auth: run 'gcloud auth application-default login'
os.environ["VERTEXAI_PROJECT"] = "your-project-id"
os.environ["VERTEXAI_LOCATION"] = "us-central1"

response = completion(
  model="vertex_ai/{{gemini_pro}}",
  messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)
```

</TabItem>
<TabItem value="bedrock" label="Bedrock">

```python
from lumina import completion
import os

os.environ["AWS_ACCESS_KEY_ID"] = "your-key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your-secret"
os.environ["AWS_REGION_NAME"] = "us-east-1"

response = completion(
  model="bedrock/us.anthropic.{{anthropic}}",
  messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)
```

</TabItem>
<TabItem value="ollama" label="Ollama">

```python
from lumina import completion

response = completion(
  model="ollama/llama3",
  messages=[{"role": "user", "content": "Hello, how are you?"}],
  api_base="http://localhost:11434"
)
print(response.choices[0].message.content)
```

</TabItem>
<TabItem value="azure" label="Azure OpenAI">

```python
from lumina import completion
import os

os.environ["AZURE_API_KEY"] = "your-key"
os.environ["AZURE_API_BASE"] = "https://your-resource.openai.azure.com"
os.environ["AZURE_API_VERSION"] = "2024-02-01"

response = completion(
  model="azure/your-deployment-name",
  messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)
```

</TabItem>
</Tabs>

Every response follows the OpenAI Chat Completions format, regardless of provider. ✅

### Response Format

Non-streaming responses return a `ModelResponse` object:

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1677858242,
  "model": "{{openai_large}}",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! I'm doing well, thanks for asking."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 12,
    "total_tokens": 25
  }
}
```

Streaming responses (`stream=True`) yield `ModelResponseStream` chunks:

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion.chunk",
  "created": 1677858242,
  "model": "{{openai_large}}",
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant",
        "content": "Hello"
      },
      "finish_reason": null
    }
  ]
}
```

[Full output format reference →](/docs/completion/output)

:::tip[Open in Colab]
<a target="_blank" href="https://colab.research.google.com/github/Soventra/lumina/blob/main/cookbook/Lumina_Getting_Started.ipynb">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
:::

---

## New to Lumina?

**Want to get started fast?** Head to [Tutorials](/docs/tutorials) for step-by-step walkthroughs of AI coding tools, agent SDKs, proxy setup, and more.

**Need to understand a specific feature?** Check [Guides](/docs/guides) for streaming, function calling, prompt caching, and other how-tos.

---

## Choose Your Path

<NavigationCards
columns={2}
items={[
{
title: "Python SDK",
description: "Integrate Lumina directly into your Python application. Drop-in replacement for the OpenAI client.",
listDescription: [
"completion(), embedding(), image_generation() and more",
"Router with retry, fallback, and load balancing",
"OpenAI-compatible exceptions across all providers",
"Observability callbacks (Langfuse, MLflow, Helicone…)",
],
to: "#lumina-python-sdk",
},
{
title: "Proxy Server (LLM Gateway)",
description: "Self-hosted gateway for platform teams managing LLM access across an organization.",
listDescription: [
"Virtual keys with per-key/team/user budgets",
"Centralized logging, guardrails, and caching",
"Admin UI for monitoring and management",
"Drop-in replacement for any OpenAI-compatible client",
],
to: "#lumina-proxy-server-llm-gateway",
},
]}
/>

---

## Lumina Python SDK

### Streaming

Add `stream=True` to receive chunks as they are generated:

```python
from lumina import completion
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"

for chunk in completion(
  model="openai/{{openai_large}}",
  messages=[{"role": "user", "content": "Write a short poem"}],
  stream=True,
):
    print(chunk.choices[0].delta.content or "", end="")
```

### Exception Handling

Lumina maps every provider's errors to the OpenAI exception types, so your existing error handling keeps working:

```python
import lumina

try:
    lumina.completion(
      model="anthropic/{{anthropic}}",
      messages=[{"role": "user", "content": "Hey!"}]
    )
except lumina.AuthenticationError as e:
    print(f"Bad API key: {e}")
except lumina.RateLimitError as e:
    print(f"Rate limited: {e}")
except lumina.APIError as e:
    print(f"API error: {e}")
```

### Logging & Observability

Send input/output to Langfuse, MLflow, Helicone, Lunary, and more with a single line:

```python
import lumina

lumina.success_callback = ["langfuse", "mlflow", "helicone"]

response = lumina.completion(
  model="{{openai_large}}",
  messages=[{"role": "user", "content": "Hi!"}]
)
```

[See all observability integrations →](/docs/observability/opentelemetry_v2)

### Track Costs & Usage

Use a callback to capture cost per response:

```python
import lumina

def track_cost(kwargs, completion_response, start_time, end_time):
    print("Cost:", kwargs.get("response_cost", 0))

lumina.success_callback = [track_cost]

lumina.completion(
  model="{{openai_large}}",
  messages=[{"role": "user", "content": "Hello!"}],
  stream=True
)
```

[Custom callback docs →](/docs/observability/custom_callback)

---

## Lumina Proxy Server (LLM Gateway)

The proxy is a self-hosted OpenAI-compatible gateway. Any client that works with OpenAI works with the proxy, with no code changes.

![Lumina Proxy Dashboard](https://github.com/Soventra/lumina/assets/29436595/47c97d5e-b9be-4839-b28c-43d7f4f10033)

#### Step 1: Start the proxy

<Tabs>
<TabItem value="cli" label="Lumina CLI">

```shell
lumina --model huggingface/bigcode/starcoder
# Proxy running on http://0.0.0.0:4000
```

</TabItem>
<TabItem value="docker" label="Docker">

```yaml title="lumina_config.yaml"
model_list:
  - model_name: {{openai_small}}
    lumina_params:
      model: azure/your-deployment
      api_base: os.environ/AZURE_API_BASE
      api_key: os.environ/AZURE_API_KEY
      api_version: "2023-07-01-preview"
```

```shell
docker run \
  -v $(pwd)/lumina_config.yaml:/app/config.yaml \
  -e AZURE_API_KEY=your-key \
  -e AZURE_API_BASE=https://your-resource.openai.azure.com/ \
  -p 4000:4000 \
  docker.lumina.ai/soventra/lumina:latest \
  --config /app/config.yaml --detailed_debug
```

</TabItem>
</Tabs>

#### Step 2: Call it with the OpenAI client

```python
import openai

client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")

response = client.chat.completions.create(
  model="{{openai_small}}",
  messages=[{"role": "user", "content": "Write a short poem"}]
)
print(response.choices[0].message.content)
```

[Full proxy quickstart →](/docs/proxy/docker_quick_start)

:::tip[Debugging tool]
Use **`/utils/transform_request`** to inspect exactly what Lumina sends to any provider. It helps when debugging prompt formatting, header issues, and provider-specific parameters.
:::

[Interactive API explorer (Swagger) →](https://docs.lumina.ai/api-reference/)

---

## Agent & MCP Gateway

Lumina is a unified gateway for **LLMs, agents, and MCP**, so you don't need a separate agent or MCP gateway. One endpoint for 100+ models, A2A agents, and MCP tools.

<NavigationCards
columns={3}
items={[
{
title: "A2A Agents",
description: "Add and invoke A2A agents via the Lumina gateway.",
to: "/docs/a2a",
},
{
title: "MCP Gateway",
description: "Central MCP endpoint with per-key access control.",
to: "/docs/mcp",
},
{
title: "Enterprise Quickstart",
      description: "Quickstart guide for trial customers: LLM, MCP, and Agent gateway.",
to: "/docs/learn/enterprise_quickstart",
},
]}
/>

---

## What to Explore Next

<NavigationCards
columns={3}
items={[
{
title: "Routing & Load Balancing",
description: "Load balance across deployments and set automatic fallbacks.",
to: "/docs/proxy/load_balancing",
},
{
title: "Virtual Keys",
description: "Manage access, budgets, and rate limits per team or user.",
to: "/docs/proxy/virtual_keys",
},
{
title: "Spend Tracking",
description: "Track costs per key, team, and user across all providers.",
to: "/docs/proxy/cost_tracking",
},
{
title: "Guardrails",
description: "Add content filtering, PII masking, and safety checks.",
to: "/docs/proxy/guardrails/quick_start",
},
{
title: "Observability",
description: "Integrate with Langfuse, MLflow, Helicone, and more.",
to: "/docs/observability/opentelemetry_v2",
},
{
title: "Enterprise",
description: "SSO/SAML, audit logs, and advanced security for production.",
to: "/docs/enterprise",
},
]}
/>
