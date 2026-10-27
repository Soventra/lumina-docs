import Image from '@theme/IdealImage';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Custom Prompt Management

Connect Lumina to your prompt management system with custom hooks.

## Overview


<Image 
  img={require('../../img/custom_prompt_management.png')}
  style={{width: '100%', display: 'block', margin: '2rem auto'}}
/>


## How it works

## Quick Start

### 1. Create Your Custom Prompt Manager

Create a class that inherits from `CustomPromptManagement` to handle prompt retrieval and formatting:

**Example Implementation**

Create a new file called `custom_prompt.py` and add this code. The key method here is `get_chat_completion_prompt` you can implement custom logic to retrieve and format prompts based on the `prompt_id` and `prompt_variables`.

```python
from typing import List, Tuple, Optional
from lumina.integrations.custom_prompt_management import CustomPromptManagement
from lumina.types.llms.openai import AllMessageValues
from lumina.types.prompts.init_prompts import PromptSpec
from lumina.types.utils import StandardCallbackDynamicParams

class MyCustomPromptManagement(CustomPromptManagement):
    def get_chat_completion_prompt(
        self,
        model: str,
        messages: List[AllMessageValues],
        non_default_params: dict,
        prompt_id: str,
        prompt_variables: Optional[dict],
        dynamic_callback_params: StandardCallbackDynamicParams,
        prompt_spec: Optional[PromptSpec] = None,
        prompt_label: Optional[str] = None,
        prompt_version: Optional[int] = None,
        ignore_prompt_manager_model: Optional[bool] = False,
        ignore_prompt_manager_optional_params: Optional[bool] = False,
    ) -> Tuple[str, List[AllMessageValues], dict]:
        """
        Retrieve and format prompts based on prompt_id.
        
        Returns:
            - model: The model to use
            - messages: The formatted messages
            - non_default_params: Optional parameters like temperature
        """
        # Example matching the diagram: Add system message for prompt_id "1234"
        if prompt_id == "1234":
            # Prepend system message while preserving existing messages
            new_messages = [
                {"role": "system", "content": "Be a good Bot!"},
            ] + messages
            return model, new_messages, non_default_params
        
        # Default: Return original messages if no prompt_id match
        return model, messages, non_default_params

prompt_management = MyCustomPromptManagement()
```

### 2. Configure Your Prompt Manager in Lumina `config.yaml`

```yaml
model_list:
  - model_name: {{openai_large}}
    lumina_params:
      model: openai/{{openai_large}}
      api_key: os.environ/OPENAI_API_KEY

lumina_settings:
  callbacks: custom_prompt.prompt_management  # sets lumina.callbacks = [prompt_management]
```

### 3. Start Lumina Gateway

<Tabs>
<TabItem value="docker" label="Docker Run">

Mount your `custom_logger.py` on the Lumina Docker container.

```shell
docker run -d \
  -p 4000:4000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  --name my-app \
  -v $(pwd)/my_config.yaml:/app/config.yaml \
  -v $(pwd)/custom_logger.py:/app/custom_logger.py \
  my-app:latest \
  --config /app/config.yaml \
  --port 4000 \
  --detailed_debug \
```

</TabItem>

<TabItem value="py" label="lumina pip">

```shell
lumina --config config.yaml --detailed_debug
```

</TabItem>
</Tabs>

### 4. Test Your Custom Prompt Manager

When you pass `prompt_id="1234"`, the custom prompt manager will add a system message "Be a good Bot!" to your conversation:

<Tabs>
<TabItem value="openai" label="OpenAI Python v1.0.0+">

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-<your-lumina-api-key>",
    base_url="http://0.0.0.0:4000"
)

response = client.chat.completions.create(
    model="{{openai_large}}",
    messages=[{"role": "user", "content": "hi"}],
    extra_body={
        "prompt_id": "1234"
    }
)

print(response.choices[0].message.content)
```
</TabItem>

<TabItem value="langchain" label="Langchain">

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

chat = ChatOpenAI(
    model="{{openai_large}}",
    openai_api_key="sk-<your-api-key>",
    openai_api_base="http://0.0.0.0:4000",
    extra_body={
        "prompt_id": "1234"
    }
)

messages = []
response = chat(messages)

print(response.content)
```
</TabItem>

<TabItem value="curl" label="Curl">

```shell
curl -X POST http://0.0.0.0:4000/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $LUMINA_API_KEY" \
-d '{
    "model": "{{openai_large}}",
    "messages": [{"role": "user", "content": "hi"}],
    "prompt_id": "1234"
}'
```
</TabItem>
</Tabs>

### Using the Lumina SDK Directly

If you call `lumina.completion()` from a Python script (without going through the proxy), register your custom prompt manager before making the request:

```python

import lumina
from custom_prompt import prompt_management

lumina.callbacks = [prompt_management]

response = lumina.completion(
    model="{{openai_large}}",
    messages=[{"role": "user", "content": "hi"}],
    prompt_id="1234",
    prompt_variables={"user_message": "hi"},
)
```

> **Note:** `lumina.callbacks = [prompt_management]` (or equivalently `lumina.logging_callback_manager.add_lumina_callback(prompt_management)`) is required in SDK scripts. The proxy reads `callbacks` from `config.yaml` automatically, but standalone scripts do not.

The request will be transformed from:
```json
{
    "model": "{{openai_large}}",
    "messages": [{"role": "user", "content": "hi"}],
    "prompt_id": "1234"
}
```

To:
```json
{
    "model": "{{openai_large}}",
    "messages": [
        {"role": "system", "content": "Be a good Bot!"},
        {"role": "user", "content": "hi"}
    ]
}
```


