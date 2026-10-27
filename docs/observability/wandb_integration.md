import Image from '@theme/IdealImage';

# Weights & Biases


:::tip

This is community maintained, Please make an issue if you run into a bug
https://github.com/Soventra/lumina

:::


Weights & Biases helps AI developers build better models faster https://wandb.ai

<Image img={require('../../img/wandb.png')} />

:::info
We want to learn how we can make the callbacks better! Meet the Lumina [founders](https://calendly.com/d/4mp-gd3-k5k/berriai-1-1-onboarding-lumina-hosted-version) or
join our [discord](https://discord.gg/wuPM9dRgDw)
::: 

## Pre-Requisites
Ensure you have run `uv add wandb` for this integration
```shell
uv add wandb lumina
```

## Quick Start
Use just 2 lines of code, to instantly log your responses **across all providers** with Weights & Biases

```python
lumina.success_callback = ["wandb"]
```
```python
# uv add wandb 
import lumina
import os

os.environ["WANDB_API_KEY"] = ""
# LLM API Keys
os.environ['OPENAI_API_KEY']=""

# set wandb as a callback, lumina will send the data to Weights & Biases
lumina.success_callback = ["wandb"] 
 
# openai call
response = lumina.completion(
  model="{{openai_small}}",
  messages=[
    {"role": "user", "content": "Hi - i'm openai"}
  ]
)
```

## Support & Talk to Founders

- [Schedule Demo](https://calendly.com/d/4mp-gd3-k5k/berriai-1-1-onboarding-lumina-hosted-version)
- [Community Discord](https://discord.gg/wuPM9dRgDw)
- Our emails ishaan@berri.ai / krrish@berri.ai