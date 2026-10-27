# Scrub Logged Data

Redact messages / mask PII before sending data to logging integrations (langfuse/etc.).

See our [**Presidio PII Masking**](https://github.com/Soventra/lumina/blob/a176feeacc5fdf504747978d82056eb84679c4be/lumina/proxy/hooks/presidio_pii_masking.py#L286) for reference.

1. Setup a custom callback 

```python
from lumina.integrations.custom_logger import CustomLogger

class MyCustomHandler(CustomLogger):
    async def async_logging_hook(
        self, kwargs: dict, result: Any, call_type: str
    ) -> Tuple[dict, Any]:
        """
        For masking logged request/response. Return a modified version of the request/result. 
        
        Called before `async_log_success_event`.
        """
        if (
            call_type == "completion" or call_type == "acompletion"
        ):  # /chat/completions requests
            messages: Optional[List] = kwargs.get("messages", None)

            kwargs["messages"] = [{"role": "user", "content": "MASK_THIS_ASYNC_VALUE"}]

        return kwargs, result

    def logging_hook(
        self, kwargs: dict, result: Any, call_type: str
    ) -> Tuple[dict, Any]:
        """
        For masking logged request/response. Return a modified version of the request/result.

        Called before `log_success_event`.
        """
        if (
            call_type == "completion" or call_type == "acompletion"
        ):  # /chat/completions requests
            messages: Optional[List] = kwargs.get("messages", None)

            kwargs["messages"] = [{"role": "user", "content": "MASK_THIS_SYNC_VALUE"}]

        return kwargs, result


customHandler = MyCustomHandler()
```


2. Connect custom handler to Lumina

```python
import lumina

lumina.callbacks = [customHandler]
```

3. Test it!

```python
# uv add langfuse 

import os
import lumina
from lumina import completion 

os.environ["LANGFUSE_PUBLIC_KEY"] = ""
os.environ["LANGFUSE_SECRET_KEY"] = ""
# Optional, defaults to https://cloud.langfuse.com
os.environ["LANGFUSE_HOST"] # optional
# LLM API Keys
os.environ['OPENAI_API_KEY']=""

lumina.callbacks = [customHandler]
lumina.success_callback = ["langfuse"]



## sync 
response = completion(model="{{openai_small}}", messages=[{ "role": "user", "content": "Hi - i'm openai"}],
                              stream=True)
for chunk in response: 
    continue


## async
import asyncio 

async def completion():
    response = await acompletion(model="{{openai_small}}", messages=[{ "role": "user", "content": "Hi - i'm openai"}],
                              stream=True)
    async for chunk in response: 
        continue
asyncio.run(completion())
```