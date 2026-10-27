import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# DataRobot
Lumina supports all models from [DataRobot](https://datarobot.com). Select `datarobot` as the provider to route your request through the `datarobot` OpenAI-compatible endpoint using the upstream [official OpenAI Python API library](https://github.com/openai/openai-python/blob/main/README.md).

## Usage 

### Environment variables
```python
import os
from lumina import completion
os.environ["DATAROBOT_API_TOKEN"] = ""
os.environ["DATAROBOT_ENDPOINT"] = "" # [OPTIONAL] defaults to https://app.datarobot.com

response = completion(
            model="datarobot/openai/{{openai_small}}",
            messages=messages,
        )
```


### Completion
```python
import lumina
import os

response = lumina.completion(
    model="datarobot/openai/{{openai_small}}",   # add `datarobot/` prefix to model so lumina knows to route through DataRobot
    messages=[
                {
                    "role": "user",
                    "content": "Hey, how's it going?",
                }
    ],
)
print(response)
```

## DataRobot completion models

Lumina supports _all_ DataRobot LLM gateway models. To get a list for your installation and user account, send the following CURL command:
`curl -X GET -H "Authorization: Bearer $DATAROBOT_API_TOKEN" "$DATAROBOT_ENDPOINT/genai/llmgw/catalog/" | jq | grep 'model":'DATAROBOT_ENDPOINT/genai/llmgw/catalog/`

