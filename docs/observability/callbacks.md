# Callbacks

## Use Callbacks to send Output Data to Posthog, Sentry etc

Lumina provides `input_callbacks`, `success_callbacks` and `failure_callbacks`, making it easy for you to send data to a particular provider depending on the status of your responses.

:::tip
**New to Lumina Callbacks?**

- For proxy/server logging and observability, see the [Proxy Logging Guide](https://docs.lumina.ai/docs/proxy/logging).
- To write your own callback logic, see the [Custom Callbacks Guide](https://docs.lumina.ai/docs/observability/custom_callback).
:::


### Supported Callback Integrations

- [Lunary](https://lunary.ai/docs)
- [Langfuse](https://langfuse.com/docs)
- [LangSmith](https://www.langchain.com/langsmith)
- [Helicone](https://docs.helicone.ai/introduction)
- [Traceloop](https://traceloop.com/docs)
- [Athina](https://docs.athina.ai/)
- [Sentry](https://docs.sentry.io/platforms/python/)
- [PostHog](https://posthog.com/docs/libraries/python)
- [Slack](https://slack.dev/bolt-python/concepts)
- [Arize](https://docs.arize.com/)
- [PromptLayer](https://docs.promptlayer.com/)

This is **not** an extensive list. Please check the dropdown for all logging integrations.

### Related Cookbooks
Try out our cookbooks for code snippets and interactive demos:

- [Langfuse Callback Example (Colab)](https://colab.research.google.com/github/Soventra/lumina/blob/main/cookbook/logging_observability/Lumina_Langfuse.ipynb)
- [Lunary Callback Example (Colab)](https://colab.research.google.com/github/Soventra/lumina/blob/main/cookbook/logging_observability/Lumina_Lunary.ipynb)
- [Arize Callback Example (Colab)](https://colab.research.google.com/github/Soventra/lumina/blob/main/cookbook/logging_observability/Lumina_Arize.ipynb)
- [Proxy + Langfuse Callback Example (Colab)](https://colab.research.google.com/github/Soventra/lumina/blob/main/cookbook/logging_observability/Lumina_Proxy_Langfuse.ipynb)
- [PromptLayer Callback Example (Colab)](https://colab.research.google.com/github/Soventra/lumina/blob/main/cookbook/Lumina_PromptLayer.ipynb)

### Quick Start

```python
from lumina import completion

# set callbacks
lumina.input_callback=["sentry"] # for sentry breadcrumbing - logs the input being sent to the api
lumina.success_callback=["posthog", "helicone", "langfuse", "lunary", "athina"]
lumina.failure_callback=["sentry", "lunary", "langfuse"]

## set env variables
os.environ['LUNARY_PUBLIC_KEY'] = ""
os.environ['SENTRY_DSN'], os.environ['SENTRY_API_TRACE_RATE']= ""
os.environ['POSTHOG_API_KEY'], os.environ['POSTHOG_API_URL'] = "api-key", "api-url"
os.environ["HELICONE_API_KEY"] = ""
os.environ["TRACELOOP_API_KEY"] = ""
os.environ["LUNARY_PUBLIC_KEY"] = ""
os.environ["ATHINA_API_KEY"] = ""
os.environ["LANGFUSE_PUBLIC_KEY"] = ""
os.environ["LANGFUSE_SECRET_KEY"] = ""
os.environ["LANGFUSE_HOST"] = ""

response = completion(model="{{openai_small}}", messages=messages)
```
