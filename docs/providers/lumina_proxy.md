import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Lumina Proxy (LLM Gateway)


| Property | Details |
|-------|-------|
| Description | Lumina Proxy is an OpenAI-compatible gateway that allows you to interact with multiple LLM providers through a unified API. Simply use the `lumina_proxy/` prefix before the model name to route your requests through the proxy. |
| Provider Route on Lumina | `lumina_proxy/` (add this prefix to the model name, to route any requests to lumina_proxy - e.g. `lumina_proxy/your-model-name`) |
| Setup Lumina Gateway | [Lumina Gateway ↗](../simple_proxy) |
| Supported Endpoints |`/chat/completions`, `/completions`, `/embeddings`, `/audio/speech`, `/audio/transcriptions`, `/images`, `/images/edits`, `/rerank` |



## Required Variables

```python
os.environ["LUMINA_PROXY_API_KEY"] = "" # "sk-<your-lumina-api-key>" your lumina proxy api key 
os.environ["LUMINA_PROXY_API_BASE"] = "" # "http://localhost:4000" your lumina proxy api base
```


## Usage (Non Streaming)
```python
import os 
import lumina
from lumina import completion

os.environ["LUMINA_PROXY_API_KEY"] = ""

# set custom api base to your proxy
# either set .env or lumina.api_base
# os.environ["LUMINA_PROXY_API_BASE"] = ""
lumina.api_base = "your-openai-proxy-url"


messages = [{ "content": "Hello, how are you?","role": "user"}]

# lumina proxy call
response = completion(model="lumina_proxy/your-model-name", messages=messages)
```

## Usage - passing `api_base`, `api_key` per request

If you need to set api_base dynamically, just pass it in completions instead - completions(...,api_base="your-proxy-api-base")

```python
import os 
import lumina
from lumina import completion

os.environ["LUMINA_PROXY_API_KEY"] = ""

messages = [{ "content": "Hello, how are you?","role": "user"}]

# lumina proxy call
response = completion(
    model="lumina_proxy/your-model-name", 
    messages=messages, 
    api_base = "your-lumina-proxy-url",
    api_key = "your-lumina-proxy-api-key"
)
```
## Usage - Streaming

```python
import os 
import lumina
from lumina import completion

os.environ["LUMINA_PROXY_API_KEY"] = ""

messages = [{ "content": "Hello, how are you?","role": "user"}]

# openai call
response = completion(
    model="lumina_proxy/your-model-name", 
    messages=messages,
    api_base = "your-lumina-proxy-url", 
    stream=True
)

for chunk in response:
    print(chunk)
```

## Embeddings

```python
import lumina

response = lumina.embedding(
    model="lumina_proxy/your-embedding-model",
    input="Hello world",
    api_base="your-lumina-proxy-url",
    api_key="your-lumina-proxy-api-key"
)
```

## Image Generation

```python
import lumina

response = lumina.image_generation(
    model="lumina_proxy/dall-e-3",
    prompt="A beautiful sunset over mountains",
    api_base="your-lumina-proxy-url",
    api_key="your-lumina-proxy-api-key"
)
```

## Image Edit

```python
import lumina

with open("your-image.png", "rb") as f:
    response = lumina.image_edit(
        model="lumina_proxy/gpt-image-1",
        prompt="Make this image a watercolor painting",
        image=[f],
        api_base="your-lumina-proxy-url",
        api_key="your-lumina-proxy-api-key",
    )
```

## Audio Transcription

```python
import lumina

response = lumina.transcription(
    model="lumina_proxy/whisper-1",
    file="your-audio-file",
    api_base="your-lumina-proxy-url",
    api_key="your-lumina-proxy-api-key"
)
```

## Text to Speech

```python
import lumina

response = lumina.speech(
    model="lumina_proxy/tts-1",
    input="Hello world",
    api_base="your-lumina-proxy-url",
    api_key="your-lumina-proxy-api-key"
)
``` 

## Rerank

```python
import lumina

import lumina

response = lumina.rerank(
    model="lumina_proxy/rerank-english-v2.0",
    query="What is machine learning?",
    documents=[
        "Machine learning is a field of study in artificial intelligence",
        "Biology is the study of living organisms"
    ],
    api_base="your-lumina-proxy-url",
    api_key="your-lumina-proxy-api-key"
)
```


## Integration with Other Libraries

Lumina Proxy works with Langchain, LlamaIndex, OpenAI JS, Anthropic SDK, Instructor, and more.

[Learn how to use Lumina proxy with these libraries →](../proxy/user_keys)

## Send all SDK requests to Lumina Proxy

:::info

Requires v1.72.1 or higher.

:::

Use this when calling Lumina Proxy from any library / codebase already using the Lumina SDK.

These flags will route all requests through your Lumina proxy, regardless of the model specified.

When enabled, requests will use `LUMINA_PROXY_API_BASE` with `LUMINA_PROXY_API_KEY` as the authentication.

### Option 1: Set Globally in Code

```python
# Set the flag globally for all requests
lumina.use_lumina_proxy = True

response = lumina.completion(
    model="vertex_ai/{{gemini_flash}}",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
```

### Option 2: Control via Environment Variable

```python
# Control proxy usage through environment variable
os.environ["USE_LUMINA_PROXY"] = "True"

response = lumina.completion(
    model="vertex_ai/{{gemini_flash}}",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
```

### Option 3: Set Per Request

```python
# Enable proxy for specific requests only
response = lumina.completion(
    model="vertex_ai/{{gemini_flash}}",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    use_lumina_proxy=True
)
```

## OAuth2/JWT Authentication

If your Lumina Proxy requires OAuth2/JWT authentication (e.g., Azure AD, Keycloak, Okta), the SDK can automatically obtain and refresh tokens for you.

```python
import lumina
from lumina.proxy_auth import AzureADCredential, ProxyAuthHandler

lumina.proxy_auth = ProxyAuthHandler(
    credential=AzureADCredential(),
    scope="api://my-lumina-proxy/.default"
)
lumina.api_base = "https://my-proxy.example.com"

response = lumina.completion(
    model="{{openai_large}}",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

[Learn more about SDK Proxy Authentication (OAuth2/JWT Auto-Refresh) →](../proxy_auth)

## Sending `tags` to Lumina Proxy

Tags allow you to categorize and track your API requests for monitoring, debugging, and analytics purposes. You can send tags as a list of strings to the Lumina Proxy using the `extra_body` parameter.

### Usage

Send tags by including them in the `extra_body` parameter of your completion request:

```python showLineNumbers title="Usage"
import lumina

response = lumina.completion(
    model="{{openai_large}}",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    api_base="http://localhost:4000",
    api_key="sk-<your-lumina-api-key>",
    extra_body={"tags": ["user:ishaan", "department:engineering", "priority:high"]}
)
```

### Async Usage

```python showLineNumbers title="Async Usage"
import lumina

response = await lumina.acompletion(
    model="{{openai_large}}",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    api_base="http://localhost:4000", 
    api_key="sk-<your-lumina-api-key>",
    extra_body={"tags": ["user:ishaan", "department:engineering"]}
)
```

