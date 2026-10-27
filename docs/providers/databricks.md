import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Databricks

Lumina supports all models on Databricks

:::tip

**We support ALL Databricks models, just set `model=databricks/<any-model-on-databricks>` as a prefix when sending lumina requests**

:::

## Authentication

Lumina supports multiple authentication methods for Databricks, listed in order of preference:

### OAuth M2M (Recommended for Production)

OAuth Machine-to-Machine authentication using Service Principal credentials is the **recommended method for production** deployments per Databricks Partner requirements.

```python
import os
from lumina import completion

# Set OAuth credentials (Service Principal)
os.environ["DATABRICKS_CLIENT_ID"] = "your-service-principal-application-id"
os.environ["DATABRICKS_CLIENT_SECRET"] = "your-service-principal-secret"
os.environ["DATABRICKS_API_BASE"] = "https://adb-xxx.azuredatabricks.net/serving-endpoints"

response = completion(
    model="databricks/databricks-dbrx-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

### Personal Access Token (PAT)

PAT authentication is supported for development and testing scenarios.

```python
import os
from lumina import completion

os.environ["DATABRICKS_API_KEY"] = "dapi..."  # Your Personal Access Token
os.environ["DATABRICKS_API_BASE"] = "https://adb-xxx.azuredatabricks.net/serving-endpoints"

response = completion(
    model="databricks/databricks-dbrx-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

### Databricks SDK Authentication (Automatic)

If no credentials are provided, Lumina will use the Databricks SDK for automatic authentication. This supports OAuth, Azure AD, and other unified auth methods configured in your environment.

```python
from lumina import completion

# No environment variables needed - uses Databricks SDK unified auth
# Requires: uv add databricks-sdk
response = completion(
    model="databricks/databricks-dbrx-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

## Custom User-Agent for Partner Attribution

If you're building a product on top of Lumina that integrates with Databricks, you can pass your own partner identifier for proper attribution in Databricks telemetry.

The partner name will be prefixed to the Lumina user agent:

```python
# Via parameter
response = completion(
    model="databricks/databricks-dbrx-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    user_agent="mycompany/1.0.0",
)
# Resulting User-Agent: mycompany_lumina/1.79.1

# Via environment variable
os.environ["DATABRICKS_USER_AGENT"] = "mycompany/1.0.0"
# Resulting User-Agent: mycompany_lumina/1.79.1
```

| Input | Resulting User-Agent |
|-------|---------------------|
| (none) | `lumina/1.79.1` |
| `mycompany/1.0.0` | `mycompany_lumina/1.79.1` |
| `partner_product/2.5.0` | `partner_product_lumina/1.79.1` |
| `acme` | `acme_lumina/1.79.1` |

**Note:** The version from your custom user agent is ignored; Lumina's version is always used.

## Security

Lumina automatically redacts sensitive information (tokens, secrets, API keys) from all debug logs to prevent credential leakage. This includes:

- Authorization headers
- API keys and tokens
- Client secrets
- Personal access tokens (PATs)

## Usage

<Tabs>
<TabItem value="sdk" label="SDK">

### ENV VAR
```python
import os 
os.environ["DATABRICKS_API_KEY"] = ""
os.environ["DATABRICKS_API_BASE"] = ""
```

### Example Call

```python
from lumina import completion
import os
## set ENV variables
os.environ["DATABRICKS_API_KEY"] = "databricks key"
os.environ["DATABRICKS_API_BASE"] = "databricks base url" # e.g.: https://adb-3064715882934586.6.azuredatabricks.net/serving-endpoints

# Databricks dbrx-instruct call
response = completion(
    model="databricks/databricks-dbrx-instruct", 
    messages = [{ "content": "Hello, how are you?","role": "user"}]
)
```

</TabItem>
<TabItem value="proxy" label="PROXY">

1. Add models to your config.yaml

  ```yaml
  model_list:
    - model_name: dbrx-instruct
      lumina_params:
        model: databricks/databricks-dbrx-instruct
        api_key: os.environ/DATABRICKS_API_KEY
        api_base: os.environ/DATABRICKS_API_BASE
        user_agent: "mycompany/1.0.0"  # Optional: for partner attribution
  ```



2. Start the proxy 

  ```bash
  $ lumina --config /path/to/config.yaml --debug
  ```

3. Send Request to Lumina Proxy Server

  <Tabs>

  <TabItem value="openai" label="OpenAI Python v1.0.0+">

  ```python
  import openai
  client = openai.OpenAI(
      api_key="sk-<your-lumina-api-key>",             # pass lumina proxy key, if you're using virtual keys
      base_url="http://0.0.0.0:4000" # lumina-proxy-base url
  )

  response = client.chat.completions.create(
      model="dbrx-instruct",
      messages = [
        {
            "role": "system",
            "content": "Be a good human!"
        },
        {
            "role": "user",
            "content": "What do you know about earth?"
        }
    ]
  )

  print(response)
  ```

  </TabItem>

  <TabItem value="curl" label="curl">

  ```shell
  curl --location 'http://0.0.0.0:4000/chat/completions' \
      --header "Authorization: Bearer $LUMINA_API_KEY" \
      --header 'Content-Type: application/json' \
      --data '{
      "model": "dbrx-instruct",
      "messages": [
        {
            "role": "system",
            "content": "Be a good human!"
        },
        {
            "role": "user",
            "content": "What do you know about earth?"
        }
        ],
  }'
  ```
  </TabItem>

  </Tabs>


</TabItem>

</Tabs>

## Passing additional params - max_tokens, temperature 
See all lumina.completion supported params [here](../completion/input.md#translated-openai-params)

```python
# !uv add lumina
from lumina import completion
import os
## set ENV variables
os.environ["DATABRICKS_API_KEY"] = "databricks key"
os.environ["DATABRICKS_API_BASE"] = "databricks api base"

# databricks dbrx call
response = completion(
    model="databricks/databricks-dbrx-instruct", 
    messages = [{ "content": "Hello, how are you?","role": "user"}],
    max_tokens=20,
    temperature=0.5
)
```

**proxy**

```yaml
  model_list:
    - model_name: llama-3
      lumina_params:
        model: databricks/databricks-meta-llama-3-70b-instruct
        api_key: os.environ/DATABRICKS_API_KEY
        max_tokens: 20
        temperature: 0.5
```


## Usage - Thinking / `reasoning_content`

Lumina translates OpenAI's `reasoning_effort` to Anthropic's `thinking` parameter. [Code](https://github.com/Soventra/lumina/blob/23051d89dd3611a81617d84277059cd88b2df511/lumina/llms/anthropic/chat/transformation.py#L298)

| reasoning_effort | thinking |
| ---------------- | -------- |
| "low"            | "budget_tokens": 1024 |
| "medium"         | "budget_tokens": 2048 |
| "high"           | "budget_tokens": 4096 |


Known Limitations:
- Support for passing thinking blocks back to Claude [Issue](https://github.com/Soventra/lumina/issues/9790)
 

<Tabs>
<TabItem value="sdk" label="SDK">

```python
from lumina import completion
import os

# set ENV variables (can also be passed in to .completion() - e.g. `api_base`, `api_key`)
os.environ["DATABRICKS_API_KEY"] = "databricks key"
os.environ["DATABRICKS_API_BASE"] = "databricks base url"

resp = completion(
    model="databricks/databricks-claude-sonnet-5",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    reasoning_effort="low",
)

```

</TabItem>

<TabItem value="proxy" label="PROXY">

1. Setup config.yaml

```yaml
- model_name: {{anthropic}}
  lumina_params:
    model: databricks/databricks-claude-sonnet-5
    api_key: os.environ/DATABRICKS_API_KEY
    api_base: os.environ/DATABRICKS_API_BASE
```

2. Start proxy

```bash
lumina --config /path/to/config.yaml
```

3. Test it! 

```bash
curl http://0.0.0.0:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR-LUMINA-KEY>" \
  -d '{
    "model": "{{anthropic}}",
    "messages": [{"role": "user", "content": "What is the capital of France?"}],
    "reasoning_effort": "low"
  }'
```

</TabItem>
</Tabs>


**Expected Response**

```python
ModelResponse(
    id='chatcmpl-c542d76d-f675-4e87-8e5f-05855f5d0f5e',
    created=1740470510,
    model='{{anthropic}}',
    object='chat.completion',
    system_fingerprint=None,
    choices=[
        Choices(
            finish_reason='stop',
            index=0,
            message=Message(
                content="The capital of France is Paris.",
                role='assistant',
                tool_calls=None,
                function_call=None,
                provider_specific_fields={
                    'citations': None,
                    'thinking_blocks': [
                        {
                            'type': 'thinking',
                            'thinking': 'The capital of France is Paris. This is a very straightforward factual question.',
                            'signature': 'EuYBCkQYAiJAy6...'
                        }
                    ]
                }
            ),
            thinking_blocks=[
                {
                    'type': 'thinking',
                    'thinking': 'The capital of France is Paris. This is a very straightforward factual question.',
                    'signature': 'EuYBCkQYAiJAy6AGB...'
                }
            ],
            reasoning_content='The capital of France is Paris. This is a very straightforward factual question.'
        )
    ],
    usage=Usage(
        completion_tokens=68,
        prompt_tokens=42,
        total_tokens=110,
        completion_tokens_details=None,
        prompt_tokens_details=PromptTokensDetailsWrapper(
            audio_tokens=None,
            cached_tokens=0,
            text_tokens=None,
            image_tokens=None
        ),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0
    )
)
```

### Citations

Anthropic models served through Databricks can return citation metadata. Lumina
exposes these via `response.choices[0].message.provider_specific_fields["citations"]`.

### Pass `thinking` to Anthropic models

You can also pass the `thinking` parameter to Anthropic models.


You can also pass the `thinking` parameter to Anthropic models.

<Tabs>
<TabItem value="sdk" label="SDK">

```python
from lumina import completion
import os

# set ENV variables (can also be passed in to .completion() - e.g. `api_base`, `api_key`)
os.environ["DATABRICKS_API_KEY"] = "databricks key"
os.environ["DATABRICKS_API_BASE"] = "databricks base url"

response = lumina.completion(
  model="databricks/databricks-claude-3-7-sonnet",
  messages=[{"role": "user", "content": "What is the capital of France?"}],
  thinking={"type": "enabled", "budget_tokens": 1024},
)
```

</TabItem>
<TabItem value="proxy" label="PROXY">

```bash
curl http://0.0.0.0:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $LUMINA_KEY" \
  -d '{
    "model": "databricks/databricks-claude-3-7-sonnet",
    "messages": [{"role": "user", "content": "What is the capital of France?"}],
    "thinking": {"type": "enabled", "budget_tokens": 1024}
  }'
```

</TabItem>
</Tabs>





## Supported Databricks Chat Completion Models 

:::tip

**We support ALL Databricks models, just set `model=databricks/<any-model-on-databricks>` as a prefix when sending lumina requests**

:::


| Model Name                 | Command                                                          |
|----------------------------|------------------------------------------------------------------|
| databricks/databricks-claude-3-7-sonnet    | `completion(model='databricks/databricks/databricks-claude-3-7-sonnet', messages=messages)`   | 
| databricks-meta-llama-3-1-70b-instruct    | `completion(model='databricks/databricks-meta-llama-3-1-70b-instruct', messages=messages)`   | 
| databricks-meta-llama-3-1-405b-instruct    | `completion(model='databricks/databricks-meta-llama-3-1-405b-instruct', messages=messages)`   | 
| databricks-dbrx-instruct    | `completion(model='databricks/databricks-dbrx-instruct', messages=messages)`   | 
| databricks-meta-llama-3-70b-instruct    | `completion(model='databricks/databricks-meta-llama-3-70b-instruct', messages=messages)`   | 
| databricks-llama-2-70b-chat    | `completion(model='databricks/databricks-llama-2-70b-chat', messages=messages)`   | 
| databricks-mixtral-8x7b-instruct    | `completion(model='databricks/databricks-mixtral-8x7b-instruct', messages=messages)`   | 
| databricks-mpt-30b-instruct    | `completion(model='databricks/databricks-mpt-30b-instruct', messages=messages)`   | 
| databricks-mpt-7b-instruct    | `completion(model='databricks/databricks-mpt-7b-instruct', messages=messages)`   | 


## Decisions (ai_decide)

Databricks serves OpenJev as the [`ai_decide` AI Function](https://docs.databricks.com/aws/en/sql/language-manual/functions/ai_decide), which answers decision questions at `POST /api/2.0/ai-functions/ai-decide` on your workspace. The function is in Beta, so a workspace admin must turn on the `ai_decide` preview first. Lumina exposes it on the [unified decision routes](/docs/decisions), `/v1/systemone` for System One bodies and `/v1/decisions` for the OpenAI Decisions format, and as an Auto Router classifier. Add it to `model_list`:

```yaml title="config.yaml"
model_list:
  - model_name: databricks-decider
    lumina_params:
      model: databricks/ai_decide
      api_base: os.environ/DATABRICKS_API_BASE
      api_key: os.environ/DATABRICKS_API_KEY
```

`DATABRICKS_API_BASE` is `https://<workspace-host>`. The `/serving-endpoints` URL the chat deployments above use also works, since Lumina removes that suffix before it adds the AI Function path. Lumina sends no `model` field to the AI Function, since it picks the model itself. Any other `databricks/<endpoint>` name on the decision routes still goes to that serving endpoint's `/invocations` route.

```bash
curl http://localhost:4000/v1/systemone \
  -H "Authorization: Bearer $LUMINA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "databricks-decider",
    "state": "My invoice has two identical charges for the same month",
    "questions": {
      "is_billing": {"type": "noul", "instructions": "Is this a billing problem?"},
      "intent": {
        "type": "choice",
        "instructions": "What does the customer want?",
        "criteria": {"refund": "Money back", "explanation": "Understand the charge", "cancel": "Close the account"}
      },
      "urgency": {"type": "score", "instructions": "How urgent is this?", "criteria": ["low", "medium", "high"]}
    }
  }'
```

Lumina unwraps the `response` envelope Databricks returns, so the answers come back in the same shape as the other decision providers, and `metadata` is kept. A `noul` answer's `probability` is returned as `noul`, the System One field name. The AI Function reports no token usage and no model name, so `usage` is zero, spend logs record the call as `databricks/ai_decide` at zero cost, and `/v1/systemone` returns `model: null`. Databricks bills AI Functions on your workspace and publishes no per-token price. `/health` probes the deployment with a System One request, so no `model_info.mode` is needed. An OpenAI-format body sent to `/v1/decisions` reaches Databricks as the same System One request, and the answers come back in the OpenAI format.

To route Auto Router traffic with the same AI Function, set `opensource_classifier_config.provider: databricks` and `model: ai_decide` as described in the [OSS classifier guide](/docs/auto_router/decision_classifiers#databricks-ai-decide).

## Embedding Models

### Passing Databricks specific params - 'instruction'

For embedding models, databricks lets you pass in an additional param 'instruction'. [Full Spec](https://github.com/Soventra/lumina/blob/43353c28b341df0d9992b45c6ce464222ebd7984/lumina/llms/databricks.py#L164)


```python
# !uv add lumina
from lumina import embedding
import os
## set ENV variables
os.environ["DATABRICKS_API_KEY"] = "databricks key"
os.environ["DATABRICKS_API_BASE"] = "databricks url"

# Databricks bge-large-en call
response = lumina.embedding(
      model="databricks/databricks-bge-large-en",
      input=["good morning from lumina"],
      instruction="Represent this sentence for searching relevant passages:",
  )
```

**proxy**

```yaml
  model_list:
    - model_name: bge-large
      lumina_params:
        model: databricks/databricks-bge-large-en
        api_key: os.environ/DATABRICKS_API_KEY
        api_base: os.environ/DATABRICKS_API_BASE
        instruction: "Represent this sentence for searching relevant passages:"
```

## Supported Databricks Embedding Models 

:::tip

**We support ALL Databricks models, just set `model=databricks/<any-model-on-databricks>` as a prefix when sending lumina requests**

:::


| Model Name                 | Command                                                          |
|----------------------------|------------------------------------------------------------------|
| databricks-bge-large-en    | `embedding(model='databricks/databricks-bge-large-en', messages=messages)`   |
| databricks-gte-large-en    | `embedding(model='databricks/databricks-gte-large-en', messages=messages)`   |
