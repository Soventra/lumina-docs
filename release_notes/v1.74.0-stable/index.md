---
title: "Lumina v1.74.0-stable"
description: "Adds namespaced MCP servers on the MCP Gateway, team and key logging in the UI, Azure Content Safety guardrails and GitHub Copilot as a provider."
slug: "v1-74-0-stable"
date: 2025-07-05T10:00:00
authors:
  - name: Krrish Dholakia
    title: CEO, Lumina
    url: https://www.linkedin.com/in/krish-d/
    image_url: https://pbs.twimg.com/profile_images/1298587542745358340/DZv3Oj-h_400x400.jpg
  - name: Ishaan Jaffer
    title: CTO, Lumina
    url: https://www.linkedin.com/in/reffajnaahsi/
    image_url: https://pbs.twimg.com/profile_images/1613813310264340481/lz54oEiB_400x400.jpg

hide_table_of_contents: false
---

import Image from '@theme/IdealImage';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Deploy this version

<Tabs>
<TabItem value="docker" label="Docker">

``` showLineNumbers title="docker run lumina"
docker run \
-e STORE_MODEL_IN_DB=True \
-p 4000:4000 \
docker.lumina.ai/soventra/lumina:v1.74.0-stable
```
</TabItem>

<TabItem value="pip" label="Pip">

``` showLineNumbers title="pip install lumina"
pip install lumina==1.74.0.post2
```

</TabItem>
</Tabs>

---

## Key Highlights 

- **MCP Gateway Namespace Servers** - Clients connecting to Lumina can now specify which MCP servers to use. 
- **Key/Team Based Logging on UI** - Proxy Admins can configure team or key-based logging settings directly in the UI. 
- **Azure Content Safety Guardrails** - Added support for prompt injection and text moderation with Azure Content Safety Guardrails. 
- **VertexAI Deepseek Models** - Support for calling VertexAI Deepseek models with Lumina's/chat/completions or /responses API.
- **Github Copilot API** - You can now use Github Copilot as an LLM API provider.


### MCP Gateway: Namespaced MCP Servers

This release brings support for namespacing MCP Servers on Lumina MCP Gateway.  This means you can specify the `x-mcp-servers` header to specify which servers to list tools from. 
 
This is useful when you want to point MCP clients to specific MCP Servers on Lumina. 


#### Usage

<Tabs>
<TabItem value="openai" label="OpenAI API">

```bash title="cURL Example with Server Segregation" showLineNumbers
curl --location 'https://api.openai.com/v1/responses' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $OPENAI_API_KEY" \
--data '{
    "model": "gpt-4o",
    "tools": [
        {
            "type": "mcp",
            "server_label": "lumina",
            "server_url": "<your-lumina-proxy-base-url>/mcp",
            "require_approval": "never",
            "headers": {
                "x-lumina-api-key": "Bearer YOUR_LUMINA_API_KEY",
                "x-mcp-servers": "Zapier_Gmail"
            }
        }
    ],
    "input": "Run available tools",
    "tool_choice": "required"
}'
```

In this example, the request will only have access to tools from the "Zapier_Gmail" MCP server.

</TabItem>

<TabItem value="lumina" label="Lumina Proxy">

```bash title="cURL Example with Server Segregation" showLineNumbers
curl --location '<your-lumina-proxy-base-url>/v1/responses' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $LUMINA_API_KEY" \
--data '{
    "model": "gpt-4o",
    "tools": [
        {
            "type": "mcp",
            "server_label": "lumina",
            "server_url": "<your-lumina-proxy-base-url>/mcp",
            "require_approval": "never",
            "headers": {
                "x-lumina-api-key": "Bearer YOUR_LUMINA_API_KEY",
                "x-mcp-servers": "Zapier_Gmail,Server2"
            }
        }
    ],
    "input": "Run available tools",
    "tool_choice": "required"
}'
```

This configuration restricts the request to only use tools from the specified MCP servers.

</TabItem>

<TabItem value="cursor" label="Cursor IDE">

```json title="Cursor MCP Configuration with Server Segregation" showLineNumbers
{
  "mcpServers": {
    "Lumina": {
      "url": "<your-lumina-proxy-base-url>/mcp",
      "headers": {
        "x-lumina-api-key": "Bearer sk-<your-lumina-api-key>",
        "x-mcp-servers": "Zapier_Gmail,Server2"
      }
    }
  }
}
```

This configuration in Cursor IDE settings will limit tool access to only the specified MCP server.

</TabItem>
</Tabs>

### Team / Key Based Logging on UI

<Image 
  img={require('../../img/release_notes/team_key_logging.png')}
  style={{width: '100%', display: 'block', margin: '2rem auto'}}
/>

<br />

This release brings support for Proxy Admins to configure Team/Key Based Logging Settings on the UI. This allows routing LLM request/response logs to different Langfuse/Arize projects based on the team or key.

For developers using Lumina, their logs are automatically routed to their specific Arize/Langfuse projects. On this release, we support the following integrations for key/team based logging:

- `langfuse`
- `arize`
- `langsmith`

### Azure Content Safety Guardrails

<Image 
  img={require('../../img/azure_content_safety_guardrails.jpg')}
  style={{width: '100%', display: 'block', margin: '2rem auto'}}
/>

<br />


Lumina now supports **Azure Content Safety Guardrails** for Prompt Injection and Text Moderation. This is **great for internal chat-ui** use cases, as you can now create guardrails with detection for Azure’s Harm Categories, specify custom severity thresholds and run them across 100+ LLMs for just that use-case (or across all your calls). 

[Get Started](../../docs/proxy/guardrails/azure_content_guardrail)


### Python SDK: 2.3 Second Faster Import Times

This release brings significant performance improvements to the Python SDK with 2.3 seconds faster import times. We've refactored the initialization process to reduce startup overhead, making Lumina more efficient for applications that need quick initialization. This is a major improvement for applications that need to initialize Lumina quickly.


---

## New Models / Updated Models

#### Pricing / Context Window Updates

| Provider    | Model                                  | Context Window | Input ($/1M tokens) | Output ($/1M tokens) | Type |
| ----------- | -------------------------------------- | -------------- | ------------------- | -------------------- | ---- |
| Watsonx | `watsonx/mistralai/mistral-large` | 131k | $3.00 | $10.00 | New |
| Azure AI | `azure_ai/cohere-rerank-v3.5` | 4k | $2.00/1k queries | - | New (Rerank) |


#### Features
- **[🆕 GitHub Copilot](../../docs/providers/github_copilot)** - Use GitHub Copilot API with Lumina - [PR](https://github.com/Soventra/lumina/pull/12325), [Get Started](../../docs/providers/github_copilot)
- **[🆕 VertexAI DeepSeek](../../docs/providers/vertex)** - Add support for VertexAI DeepSeek models - [PR](https://github.com/Soventra/lumina/pull/12312), [Get Started](../../docs/providers/vertex_partner#vertexai-deepseek)
- **[Azure AI](../../docs/providers/azure_ai)**
  - Add azure_ai cohere rerank v3.5 - [PR](https://github.com/Soventra/lumina/pull/12283), [Get Started](../../docs/providers/azure_ai#rerank-endpoint)
- **[Vertex AI](../../docs/providers/vertex)**
  - Add size parameter support for image generation - [PR](https://github.com/Soventra/lumina/pull/12292), [Get Started](../../docs/providers/vertex_image)
- **[Custom LLM](../../docs/providers/custom_llm_server)**
  - Pass through extra_ properties on "custom" llm provider - [PR](https://github.com/Soventra/lumina/pull/12185)

#### Bugs
- **[Mistral](../../docs/providers/mistral)**
  - Fix transform_response handling for empty string content - [PR](https://github.com/Soventra/lumina/pull/12202)
  - Turn Mistral to use llm_http_handler - [PR](https://github.com/Soventra/lumina/pull/12245)
- **[Gemini](../../docs/providers/gemini)**
  - Fix tool call sequence - [PR](https://github.com/Soventra/lumina/pull/11999)
  - Fix custom api_base path preservation - [PR](https://github.com/Soventra/lumina/pull/12215)
- **[Anthropic](../../docs/providers/anthropic)**
  - Fix user_id validation logic - [PR](https://github.com/Soventra/lumina/pull/11432)
- **[Bedrock](../../docs/providers/bedrock)**
  - Support optional args for bedrock - [PR](https://github.com/Soventra/lumina/pull/12287)
- **[Ollama](../../docs/providers/ollama)**
  - Fix default parameters for ollama-chat - [PR](https://github.com/Soventra/lumina/pull/12201)
- **[VLLM](../../docs/providers/vllm)**
  - Add 'audio_url' message type support - [PR](https://github.com/Soventra/lumina/pull/12270)

---

## LLM API Endpoints

#### Features

- **[/batches](../../docs/batches)**
  - Support batch retrieve with target model Query Param - [PR](https://github.com/Soventra/lumina/pull/12228)
  - Anthropic completion bridge improvements - [PR](https://github.com/Soventra/lumina/pull/12228)
- **[/responses](../../docs/response_api)**
  - Azure responses api bridge improvements - [PR](https://github.com/Soventra/lumina/pull/12224)
  - Fix responses api error handling - [PR](https://github.com/Soventra/lumina/pull/12225)
- **[/mcp (MCP Gateway)](../../docs/mcp)**
  - Add MCP url masking on frontend - [PR](https://github.com/Soventra/lumina/pull/12247)
  - Add MCP servers header to scope - [PR](https://github.com/Soventra/lumina/pull/12266)
  - Lumina mcp tool prefix - [PR](https://github.com/Soventra/lumina/pull/12289)
  - Segregate MCP tools on connections using headers - [PR](https://github.com/Soventra/lumina/pull/12296)
  - Added changes to mcp url wrapping - [PR](https://github.com/Soventra/lumina/pull/12207)


#### Bugs
- **[/v1/messages](../../docs/anthropic_unified)**
  - Remove hardcoded model name on streaming - [PR](https://github.com/Soventra/lumina/pull/12131)
  - Support lowest latency routing - [PR](https://github.com/Soventra/lumina/pull/12180)
  - Non-anthropic models token usage returned - [PR](https://github.com/Soventra/lumina/pull/12184)
- **[/chat/completions](/docs/anthropic_unified)**
  - Support Cursor IDE tool_choice format `{"type": "auto"}` - [PR](https://github.com/Soventra/lumina/pull/12168)
- **[/generateContent](/docs/generateContent)**
  - Allow passing lumina_params - [PR](https://github.com/Soventra/lumina/pull/12177)
  - Only pass supported params when using OpenAI models - [PR](https://github.com/Soventra/lumina/pull/12297)
  - Fix using gemini-cli with Vertex Anthropic Models - [PR](https://github.com/Soventra/lumina/pull/12246)
- **Streaming**
  - Fix Error code: 307 for LlamaAPI Streaming Chat - [PR](https://github.com/Soventra/lumina/pull/11946)
  - Store finish reason even if is_finished - [PR](https://github.com/Soventra/lumina/pull/12250)

---

## Spend Tracking / Budget Improvements

#### Bugs
  - Fix allow strings in calculate cost - [PR](https://github.com/Soventra/lumina/pull/12200)
  - VertexAI Anthropic streaming cost tracking with prompt caching fixes - [PR](https://github.com/Soventra/lumina/pull/12188)

---

## Management Endpoints / UI

#### Bugs
- **Team Management**
  - Prevent team model reset on model add - [PR](https://github.com/Soventra/lumina/pull/12144)
  - Return team-only models on /v2/model/info - [PR](https://github.com/Soventra/lumina/pull/12144)
  - Render team member budget correctly - [PR](https://github.com/Soventra/lumina/pull/12144)
- **UI Rendering**
  - Fix rendering ui on non-root images - [PR](https://github.com/Soventra/lumina/pull/12226)
  - Correctly display 'Internal Viewer' user role - [PR](https://github.com/Soventra/lumina/pull/12284)
- **Configuration**
  - Handle empty config.yaml - [PR](https://github.com/Soventra/lumina/pull/12189)
  - Fix gemini /models - replace models/ as expected - [PR](https://github.com/Soventra/lumina/pull/12189)

#### Features
- **Team Management**
  - Allow adding team specific logging callbacks - [PR](https://github.com/Soventra/lumina/pull/12261)
  - Add Arize Team Based Logging - [PR](https://github.com/Soventra/lumina/pull/12264)
  - Allow Viewing/Editing Team Based Callbacks - [PR](https://github.com/Soventra/lumina/pull/12265)
- **UI Improvements**
  - Comma separated spend and budget display - [PR](https://github.com/Soventra/lumina/pull/12317)
  - Add logos to callback list - [PR](https://github.com/Soventra/lumina/pull/12244)
- **CLI**
  - Add lumina-proxy cli login for starting to use lumina proxy - [PR](https://github.com/Soventra/lumina/pull/12216)
- **Email Templates**
  - Customizable Email template - Subject and Signature - [PR](https://github.com/Soventra/lumina/pull/12218)

---

## Logging / Guardrail Integrations

#### Features
- Guardrails 
  - All guardrails are now supported on the UI - [PR](https://github.com/Soventra/lumina/pull/12349)
- **[Azure Content Safety](/docs/proxy/guardrails/azure_content_guardrail)**
  - Add Azure Content Safety Guardrails to Lumina proxy - [PR](https://github.com/Soventra/lumina/pull/12268)
  - Add azure content safety guardrails to the UI - [PR](https://github.com/Soventra/lumina/pull/12309)
- **[DeepEval](../../docs/observability/deepeval_integration)**
  - Fix DeepEval logging format for failure events - [PR](https://github.com/Soventra/lumina/pull/12303)
- **[Arize](/docs/observability/arize_integration)**
  - Add Arize Team Based Logging - [PR](https://github.com/Soventra/lumina/pull/12264)
- **[Langfuse](../../docs/proxy/logging#langfuse)**
  - Langfuse prompt_version support - [PR](https://github.com/Soventra/lumina/pull/12301)
- **[Sentry Integration](../../docs/observability/sentry)**
  - Add sentry scrubbing - [PR](https://github.com/Soventra/lumina/pull/12210)
- **[AWS SQS Logging](../../docs/proxy/logging#aws-sqs)**
  - New AWS SQS Logging Integration - [PR](https://github.com/Soventra/lumina/pull/12176)
- **[S3 Logger](../../docs/proxy/logging#s3-buckets)**
  - Add failure logging support - [PR](https://github.com/Soventra/lumina/pull/12299)
- **[Prometheus Metrics](../../docs/proxy/prometheus)**
  - Add better error validation for prometheus metrics and labels - [PR](https://github.com/Soventra/lumina/pull/12182)

#### Bugs
- **Security**
  - Ensure only LLM API route fails get logged on Langfuse - [PR](https://github.com/Soventra/lumina/pull/12308)
- **OpenMeter**
  - Integration error handling fix - [PR](https://github.com/Soventra/lumina/pull/12147)
- **Message Redaction**
  - Ensure message redaction works for responses API logging - [PR](https://github.com/Soventra/lumina/pull/12291)
- **Bedrock Guardrails**
  - Fix bedrock guardrails post_call for streaming responses - [PR](https://github.com/Soventra/lumina/pull/12252)
---

## Performance / Loadbalancing / Reliability improvements

#### Features
- **Python SDK**
  - 2 second faster import times - [PR](https://github.com/Soventra/lumina/pull/12135)
  - Reduce python sdk import time by .3s - [PR](https://github.com/Soventra/lumina/pull/12140)
- **Error Handling**
  - Add error handling for MCP tools not found or invalid server - [PR](https://github.com/Soventra/lumina/pull/12223)
- **SSL/TLS**
  - Fix SSL certificate error - [PR](https://github.com/Soventra/lumina/pull/12327)
  - Fix custom ca bundle support in aiohttp transport - [PR](https://github.com/Soventra/lumina/pull/12281)


---

## General Proxy Improvements

- **Startup**
  - Add new banner on startup - [PR](https://github.com/Soventra/lumina/pull/12328)
- **Dependencies**
  - Update pydantic version - [PR](https://github.com/Soventra/lumina/pull/12213)


---

## New Contributors
* @wildcard made their first contribution in https://github.com/Soventra/lumina/pull/12157
* @colesmcintosh made their first contribution in https://github.com/Soventra/lumina/pull/12168
* @seyeong-han made their first contribution in https://github.com/Soventra/lumina/pull/11946
* @dinggh made their first contribution in https://github.com/Soventra/lumina/pull/12162
* @raz-alon made their first contribution in https://github.com/Soventra/lumina/pull/11432
* @tofarr made their first contribution in https://github.com/Soventra/lumina/pull/12200
* @szafranek made their first contribution in https://github.com/Soventra/lumina/pull/12179
* @SamBoyd made their first contribution in https://github.com/Soventra/lumina/pull/12147
* @lizzij made their first contribution in https://github.com/Soventra/lumina/pull/12219
* @cipri-tom made their first contribution in https://github.com/Soventra/lumina/pull/12201
* @zsimjee made their first contribution in https://github.com/Soventra/lumina/pull/12185
* @jroberts2600 made their first contribution in https://github.com/Soventra/lumina/pull/12175
* @njbrake made their first contribution in https://github.com/Soventra/lumina/pull/12202
* @NANDINI-star made their first contribution in https://github.com/Soventra/lumina/pull/12244
* @utsumi-fj made their first contribution in https://github.com/Soventra/lumina/pull/12230
* @dcieslak19973 made their first contribution in https://github.com/Soventra/lumina/pull/12283
* @hanouticelina made their first contribution in https://github.com/Soventra/lumina/pull/12286
* @lowjiansheng made their first contribution in https://github.com/Soventra/lumina/pull/11999
* @JoostvDoorn made their first contribution in https://github.com/Soventra/lumina/pull/12281
* @takashiishida made their first contribution in https://github.com/Soventra/lumina/pull/12239

## **[Git Diff](https://github.com/Soventra/lumina/compare/v1.73.6-stable...v1.74.0-stable)**

