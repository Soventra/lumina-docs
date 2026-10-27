# lumina.aembedding()

Lumina provides an asynchronous version of the `embedding` function called `aembedding`
### Usage
```python
from lumina import aembedding
import asyncio

async def test_get_response():
    response = await aembedding('text-embedding-ada-002', input=["good morning from lumina"])
    return response

response = asyncio.run(test_get_response())
print(response)
```