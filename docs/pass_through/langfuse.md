# Langfuse SDK

Pass-through endpoints for Langfuse - call langfuse endpoints with Lumina Virtual Key.

Just replace `https://us.cloud.langfuse.com` with `LUMINA_PROXY_BASE_URL/langfuse`

#### **Example Usage**
```python
from langfuse import Langfuse

langfuse = Langfuse(
    host="http://localhost:4000/langfuse", # your lumina proxy endpoint
    public_key="anything",        # no key required since this is a pass through
    secret_key="LUMINA_VIRTUAL_KEY",        # no key required since this is a pass through
)

print("sending langfuse trace request")
span = langfuse.start_observation(name="test-trace-lumina-proxy-passthrough")
span.end()  # the root observation's name/input/output become the trace's
print("flushing langfuse request")
langfuse.flush()

print("flushed langfuse request")
```

Supports **ALL** Langfuse Endpoints.

[**See All Langfuse Endpoints**](https://api.reference.langfuse.com/)

## Quick Start

Let's log a trace to Langfuse.

1. Add Langfuse Public/Secret keys to environment

```bash
export LANGFUSE_PUBLIC_KEY=""
export LANGFUSE_SECRET_KEY=""
```

2. Start Lumina Proxy 

```bash
lumina

# RUNNING on http://0.0.0.0:4000
```

3. Test it! 

Let's log a trace to Langfuse! 

```python
from langfuse import Langfuse

langfuse = Langfuse(
    host="http://localhost:4000/langfuse", # your lumina proxy endpoint
    public_key="anything",        # no key required since this is a pass through
    secret_key="anything",        # no key required since this is a pass through
)

print("sending langfuse trace request")
span = langfuse.start_observation(name="test-trace-lumina-proxy-passthrough")
span.end()  # the root observation's name/input/output become the trace's
print("flushing langfuse request")
langfuse.flush()

print("flushed langfuse request")
```


## Advanced - Use with Virtual Keys 

Pre-requisites
- [Setup proxy with DB](../proxy/virtual_keys.md#setup)

Use this, to avoid giving developers the raw Google AI Studio key, but still letting them use Google AI Studio endpoints.

### Usage

1. Setup environment

```bash
export DATABASE_URL=""
export LUMINA_MASTER_KEY=""
export LANGFUSE_PUBLIC_KEY=""
export LANGFUSE_SECRET_KEY=""
```

```bash
lumina

# RUNNING on http://0.0.0.0:4000
```

2. Generate virtual key 

```bash
curl -X POST 'http://0.0.0.0:4000/key/generate' \
-H "Authorization: Bearer $LUMINA_API_KEY" \
-H 'Content-Type: application/json' \
-d '{}'
```

Expected Response 

```bash
{
    ...
    "key": "sk-<virtual-key>"
}
```

3. Test it! 


```python
from langfuse import Langfuse

langfuse = Langfuse(
    host="http://localhost:4000/langfuse", # your lumina proxy endpoint
    public_key="anything",        # no key required since this is a pass through
    secret_key="sk-<your-lumina-api-key>",        # no key required since this is a pass through
)

print("sending langfuse trace request")
span = langfuse.start_observation(name="test-trace-lumina-proxy-passthrough")
span.end()  # the root observation's name/input/output become the trace's
print("flushing langfuse request")
langfuse.flush()

print("flushed langfuse request")
```

## [Advanced - Log to separate langfuse projects (by key/team)](../proxy/team_logging.md)