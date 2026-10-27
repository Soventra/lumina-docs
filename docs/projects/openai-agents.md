import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# OpenAI Agents SDK

Use OpenAI Agents SDK with any LLM provider through Lumina Proxy.

The [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) is a lightweight framework for building multi-agent workflows. It includes an official Lumina extension that lets you use any of the 100+ supported providers.

## Quick Start

### 1. Install Dependencies

```bash
uv add "openai-agents[lumina]"
```

### 2. Add Model to Config

```yaml title="config.yaml"
model_list:
  - model_name: {{openai_large}}
    lumina_params:
      model: "openai/{{openai_large}}"
      api_key: "os.environ/OPENAI_API_KEY"

  - model_name: claude-sonnet
    lumina_params:
      model: "anthropic/{{anthropic}}"
      api_key: "os.environ/ANTHROPIC_API_KEY"

  - model_name: {{gemini_pro}}
    lumina_params:
      model: "gemini/{{gemini_pro}}"
      api_key: "os.environ/GEMINI_API_KEY"
```

### 3. Start Lumina Proxy

```bash
lumina --config config.yaml
```

### 4. Use with Proxy

<Tabs>
<TabItem value="proxy" label="Via Proxy">

```python
from agents import Agent, Runner
from agents.extensions.models.lumina_model import LuminaModel

# Point to Lumina proxy
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=LuminaModel(
        model="claude-sonnet",  # Model from config.yaml
        api_key="sk-<your-lumina-api-key>",      # Lumina API key
        base_url="http://localhost:4000"
    )
)

result = await Runner.run(agent, "What is Lumina?")
print(result.final_output)
```

</TabItem>
<TabItem value="direct" label="Direct (No Proxy)">

```python
from agents import Agent, Runner
from agents.extensions.models.lumina_model import LuminaModel

# Use any provider directly
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=LuminaModel(
        model="anthropic/{{anthropic}}",
        api_key="your-anthropic-key"
    )
)

result = await Runner.run(agent, "What is Lumina?")
print(result.final_output)
```

</TabItem>
</Tabs>

## Track Usage

Enable usage tracking to monitor token consumption:

```python
from agents import Agent, ModelSettings
from agents.extensions.models.lumina_model import LuminaModel

agent = Agent(
    name="Assistant",
    model=LuminaModel(model="claude-sonnet", api_key="sk-<your-lumina-api-key>"),
    model_settings=ModelSettings(include_usage=True)
)

result = await Runner.run(agent, "Hello")
print(result.context_wrapper.usage)  # Token counts
```

## Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `LUMINA_BASE_URL` | `http://localhost:4000` | Lumina proxy URL |
| `LUMINA_API_KEY` | `sk-<your-lumina-api-key>` | Your Lumina API key |

## Related Resources

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Lumina Extension Docs](https://openai.github.io/openai-agents-python/models/lumina/)
- [Lumina Proxy Quick Start](../proxy/quick_start)
