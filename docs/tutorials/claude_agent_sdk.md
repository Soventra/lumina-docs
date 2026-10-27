import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Claude Agent SDK with Lumina

Use Anthropic's Claude Agent SDK with any LLM provider through Lumina Proxy.

The Claude Agent SDK provides a high-level interface for building AI agents. By pointing it to Lumina, you can use the same agent code with OpenAI, Bedrock, Azure, Vertex AI, or any other provider.

## Quick Start

### 1. Install Dependencies

```bash
uv add claude-agent-sdk
```

### 2. Start Lumina Proxy

```yaml title="config.yaml" showLineNumbers
model_list:
  - model_name: bedrock-claude-sonnet-5
    lumina_params:
      model: "bedrock/us.anthropic.{{anthropic}}"
      aws_region_name: "us-east-1"

  - model_name: bedrock-claude-opus-5
    lumina_params:
      model: "bedrock/us.anthropic.{{anthropic_large}}"
      aws_region_name: "us-east-1"

  - model_name: bedrock-nova-premier
    lumina_params:
      model: "bedrock/amazon.nova-premier-v1:0"
      aws_region_name: "us-east-1"
```

```bash
lumina --config config.yaml
```

### 3. Point Agent SDK to Lumina

| Environment Variable | Value | Description |
|---------------------|-------|-------------|
| `ANTHROPIC_BASE_URL` | `http://localhost:4000` | Lumina proxy URL |
| `ANTHROPIC_API_KEY` | `sk-<your-api-key>` | Your Lumina API key (not Anthropic key) |

```python title="agent.py" showLineNumbers
import os
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

# Point to Lumina proxy (not Anthropic)
os.environ["ANTHROPIC_BASE_URL"] = "http://localhost:4000"
os.environ["ANTHROPIC_API_KEY"] = "sk-<your-api-key>"  # Your Lumina key

# Configure agent with any model from your config
options = ClaudeAgentOptions(
    system_prompt="You are a helpful AI assistant.",
    model="bedrock-claude-sonnet-5",  # Use any model from config.yaml
    max_turns=20,
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("What is Lumina?")
    
    async for msg in client.receive_response():
        if hasattr(msg, 'content'):
            for content_block in msg.content:
                if hasattr(content_block, 'text'):
                    print(content_block.text, end='', flush=True)
```



## Why Use Lumina with Agent SDK?

| Feature | Benefit |
|---------|---------|
| **Multi-Provider** | Use the same agent code with OpenAI, Bedrock, Azure, Vertex AI, etc. |
| **Cost Tracking** | Track spending across all agent conversations |
| **Rate Limiting** | Set budgets and limits on agent usage |
| **Load Balancing** | Distribute requests across multiple API keys or regions |
| **Fallbacks** | Automatically retry with different models if one fails |

## Complete Example

See our [cookbook example](https://github.com/Soventra/lumina/tree/main/cookbook/anthropic_agent_sdk) for a complete interactive CLI agent that:
- Streams responses in real-time
- Switches between models dynamically
- Fetches available models from the proxy

```bash
# Clone and run the example
git clone https://github.com/Soventra/lumina.git
cd lumina/cookbook/anthropic_agent_sdk
uv add -r requirements.txt
python main.py
```

## Related Resources

- [Claude Agent SDK Documentation](https://github.com/anthropics/anthropic-agent-sdk)
- [Lumina Proxy Quick Start](../proxy/quick_start)
- [Complete Cookbook Example](https://github.com/Soventra/lumina/tree/main/cookbook/anthropic_agent_sdk)
