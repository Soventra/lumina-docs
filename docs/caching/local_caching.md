# Lumina - Local Caching

## Caching `completion()` and `embedding()` calls when switched on

Lumina implements exact match caching and supports the following Caching:
* In-Memory Caching [Default]
* Redis Caching Local
* Redis Caching Hosted

## Quick Start Usage - Completion
Caching - cache
Keys in the cache are `model`, the following example will lead to a cache hit
```python
import lumina
from lumina import completion
from lumina.caching.caching import Cache
lumina.cache = Cache()

# Make completion calls
response1 = completion(
    model="{{openai_small}}", 
    messages=[{"role": "user", "content": "Tell me a joke."}],
    caching=True
)
response2 = completion(
    model="{{openai_small}}", 
    messages=[{"role": "user", "content": "Tell me a joke."}],
    caching=True
)

# response1 == response2, response 1 is cached
```

## Custom Key-Value Pairs 
Add custom key-value pairs to your cache. 

```python 
from lumina.caching.caching import Cache
cache = Cache()

cache.add_cache(cache_key="test-key", result="1234")

cache.get_cache(cache_key="test-key")
```

## Caching with Streaming 
Lumina can cache your streamed responses for you

### Usage
```python
import lumina
from lumina import completion
from lumina.caching.caching import Cache
lumina.cache = Cache()

# Make completion calls
response1 = completion(
    model="{{openai_small}}", 
    messages=[{"role": "user", "content": "Tell me a joke."}], 
    stream=True,
    caching=True)
for chunk in response1:
    print(chunk)
response2 = completion(
    model="{{openai_small}}", 
    messages=[{"role": "user", "content": "Tell me a joke."}], 
    stream=True,
    caching=True)
for chunk in response2:
    print(chunk)
```

## Usage - Embedding()
1. Caching - cache
Keys in the cache are `model`, the following example will lead to a cache hit
```python
import time
import lumina
from lumina import embedding
from lumina.caching.caching import Cache
lumina.cache = Cache()

start_time = time.time()
embedding1 = embedding(model="text-embedding-ada-002", input=["hello from lumina"*5], caching=True)
end_time = time.time()
print(f"Embedding 1 response time: {end_time - start_time} seconds")

start_time = time.time()
embedding2 = embedding(model="text-embedding-ada-002", input=["hello from lumina"*5], caching=True)
end_time = time.time()
print(f"Embedding 2 response time: {end_time - start_time} seconds")
```