import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Adding a New Guardrail Integration

You're going to create a class that checks text before it goes to the LLM or after it comes back. If it violates your rules, you block it.

## How It Works

Request with guardrail:

```bash
curl --location 'http://localhost:4000/chat/completions' \
--header "Authorization: Bearer $LUMINA_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "{{openai_large}}",
    "messages": [{"role": "user", "content": "How do I hack a system?"}],
    "guardrails": ["my-guardrail"]
}'
```

Your guardrail checks input, then output. If something's wrong, raise an exception.

## Build Your Guardrail

### Create Your Directory

```bash
mkdir -p lumina/proxy/guardrails/guardrail_hooks/my_guardrail
cd lumina/proxy/guardrails/guardrail_hooks/my_guardrail
```

Two files: `my_guardrail.py` (main class) and `__init__.py` (initialization).

### Write the Main Class

`my_guardrail.py`:

Follow from [Custom Guardrail](/docs/proxy/guardrails/custom_guardrail#1-write-a-customguardrail-class) tutorial.

### Create the Init File

`__init__.py`:

```python
from typing import TYPE_CHECKING

from lumina.types.guardrails import SupportedGuardrailIntegrations

from .my_guardrail import MyGuardrail

if TYPE_CHECKING:
    from lumina.types.guardrails import Guardrail, LuminaParams


def initialize_guardrail(lumina_params: "LuminaParams", guardrail: "Guardrail"):
    import lumina
    
    _my_guardrail_callback = MyGuardrail(
        api_base=lumina_params.api_base,
        api_key=lumina_params.api_key,
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=lumina_params.mode,
        default_on=lumina_params.default_on,
    )
    
    lumina.logging_callback_manager.add_lumina_callback(_my_guardrail_callback)
    return _my_guardrail_callback


guardrail_initializer_registry = {
    SupportedGuardrailIntegrations.MY_GUARDRAIL.value: initialize_guardrail,
}

guardrail_class_registry = {
    SupportedGuardrailIntegrations.MY_GUARDRAIL.value: MyGuardrail,
}
```

### Register Your Guardrail Type

Add to `lumina/types/guardrails.py`:

```python
class SupportedGuardrailIntegrations(str, Enum):
    LAKERA = "lakera_prompt_injection"
    APORIA = "aporia"
    BEDROCK = "bedrock_guardrails"
    PRESIDIO = "presidio"
    ZSCALER_AI_GUARD = "zscaler_ai_guard"
    MY_GUARDRAIL = "my_guardrail"
```

## Usage

### Config File

```yaml
model_list:
  - model_name: {{openai_large}}
    lumina_params:
      model: {{openai_large}}
    api_key: os.environ/OPENAI_API_KEY

guardrails:
    - guardrail_name: my_guardrail
      lumina_params:
        guardrail: my_guardrail
        mode: during_call
        api_key: os.environ/MY_GUARDRAIL_API_KEY
        api_base: https://api.myguardrail.com
```

### Per-Request

```bash
curl --location 'http://localhost:4000/chat/completions' \
--header "Authorization: Bearer $LUMINA_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "{{openai_large}}",
    "messages": [{"role": "user", "content": "Test message"}],
    "guardrails": ["my_guardrail"]
}'
```

## Testing

Add unit tests inside `test_lumina/` folder.



