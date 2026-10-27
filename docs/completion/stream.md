---
sidebar_label: "Streaming"
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Streaming + Async

| Feature | Lumina SDK | Lumina Proxy |
|---------|-------------|---------------|
| Streaming | ✅ [start here](#streaming-responses) | ✅ [start here](../proxy/user_keys#streaming) |
| Async | ✅ [start here](#async-completion) | ✅ [start here](../proxy/user_keys#streaming) |
| Async Streaming | ✅ [start here](#async-streaming) | ✅ [start here](../proxy/user_keys#streaming) |

## Streaming Responses
Lumina supports streaming the model response back by passing `stream=True` as an argument to the completion function
### Usage
```python
from lumina import completion
messages = [{"role": "user", "content": "Hey, how's it going?"}]
response = completion(model="{{openai_small}}", messages=messages, stream=True)
for part in response:
    print(part.choices[0].delta.content or "")
```

### Helper function

Lumina also exposes a helper function to rebuild the complete streaming response from the list of chunks. 

```python
from lumina import completion
messages = [{"role": "user", "content": "Hey, how's it going?"}]
response = completion(model="{{openai_small}}", messages=messages, stream=True)

for chunk in response: 
    chunks.append(chunk)

print(lumina.stream_chunk_builder(chunks, messages=messages))
```

## Async Completion
Asynchronous Completion with Lumina. Lumina provides an asynchronous version of the completion function called `acompletion`
### Usage
```python
from lumina import acompletion
import asyncio

async def test_get_response():
    user_message = "Hello, how are you?"
    messages = [{"content": user_message, "role": "user"}]
    response = await acompletion(model="{{openai_small}}", messages=messages)
    return response

response = asyncio.run(test_get_response())
print(response)

```

## Async Streaming
We've implemented an `__anext__()` function in the streaming object returned. This enables async iteration over the streaming object. 

### Usage
Here's an example of using it with openai.
```python
from lumina import acompletion
import asyncio, os, traceback

async def completion_call():
    try:
        print("test acompletion + streaming")
        response = await acompletion(
            model="{{openai_small}}", 
            messages=[{"content": "Hello, how are you?", "role": "user"}], 
            stream=True
        )
        print(f"response: {response}")
        async for chunk in response:
            print(chunk)
    except:
        print(f"error occurred: {traceback.format_exc()}")
        pass

asyncio.run(completion_call())
```

## Error Handling - Infinite Loops

Sometimes a model might enter an infinite loop, and keep repeating the same chunks - [e.g. issue](https://github.com/Soventra/lumina/issues/5158)

Break out of it with: 

```python
lumina.REPEATED_STREAMING_CHUNK_LIMIT = 100 # # catch if model starts looping the same chunk while streaming. Uses high default to prevent false positives.
```

Lumina provides error handling for this, by checking if a chunk is repeated 'n' times (Default is 100). If it exceeds that limit, it will raise a `lumina.InternalServerError`, to allow retry logic to happen. 

<Tabs>
<TabItem value="sdk" label="SDK">

```python
import lumina 
import os 

lumina.set_verbose = False
loop_amount = lumina.REPEATED_STREAMING_CHUNK_LIMIT + 1
chunks = [
    lumina.ModelResponse(**{
    "id": "chatcmpl-123",
    "object": "chat.completion.chunk",
    "created": 1694268190,
    "model": "{{openai_small}}",
    "system_fingerprint": "fp_44709d6fcb",
    "choices": [
        {"index": 0, "delta": {"content": "How are you?"}, "finish_reason": "stop"}
    ],
}, stream=True)
] * loop_amount
completion_stream = lumina.ModelResponseListIterator(model_responses=chunks)

response = lumina.CustomStreamWrapper(
    completion_stream=completion_stream,
    model="{{openai_small}}",
    custom_llm_provider="cached_response",
    logging_obj=lumina.Logging(
        model="{{openai_small}}",
        messages=[{"role": "user", "content": "Hey"}],
        stream=True,
        call_type="completion",
        start_time=time.time(),
        lumina_call_id="12345",
        function_id="1245",
    ),
)

for chunk in response:
    continue # expect to raise InternalServerError 
```

</TabItem>
<TabItem value="proxy" label="PROXY">

Define this on your config.yaml on the proxy. 

```yaml
lumina_settings:
    REPEATED_STREAMING_CHUNK_LIMIT: 100 # this overrides the lumina default
```

The proxy uses the lumina SDK. To validate this works, try the 'SDK' code snippet. 

</TabItem>
</Tabs>