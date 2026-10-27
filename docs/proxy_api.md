# Lumina Keys (community key, discontinued)

The free community `sk-lumina-...` keys and the hosted proxy behind them are no longer available. The Lumina SDK has no special handling for these keys, so setting `OPENAI_API_KEY` (or any other provider key) to an `sk-lumina-...` value sends it straight to that provider, which rejects it with an authentication error

To get one key for many providers, run your own [Lumina Proxy](./proxy/quick_start.md) with your provider credentials, then call it from the SDK through the [`lumina_proxy/` provider](./providers/lumina_proxy.md) using a key issued by your proxy

```python
import os
from lumina import completion

os.environ["LUMINA_PROXY_API_BASE"] = "http://0.0.0.0:4000"  # your proxy
os.environ["LUMINA_PROXY_API_KEY"] = os.environ["LUMINA_API_KEY"]

messages = [{"content": "Hello, how are you?", "role": "user"}]

response = completion(model="lumina_proxy/{{openai_small}}", messages=messages)
```

The `lumina_proxy/` prefix works the same way in tools built on the Lumina SDK, as long as `LUMINA_PROXY_API_BASE` points at your proxy. For every model and provider you can call, see the [provider list](./providers/) or [models.lumina.ai](https://models.lumina.ai/)
