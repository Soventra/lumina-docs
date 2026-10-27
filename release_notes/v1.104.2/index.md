---
title: "Lumina v1.104.2 adds Decisions API routes for OpenAI and System One"
description: "Adds the Decisions API on /v1/decisions and /v1/systemone, with decision models from OpenAI, Perplexity, TypeSafe, OpenRouter, Cloudflare and Strands."
slug: "v1-104-2"
date: 2026-10-08T08:39:07
authors:
  - name: Krrish Dholakia
    title: CEO, Lumina
    url: https://www.linkedin.com/in/krish-d/
    image_url: https://pbs.twimg.com/profile_images/1298587542745358340/DZv3Oj-h_400x400.jpg
  - name: Ishaan Jaff
    title: CTO, Lumina
    url: https://www.linkedin.com/in/reffajnaahsi/
    image_url: https://pbs.twimg.com/profile_images/1613813310264340481/lz54oEiB_400x400.jpg
  - name: Yuneng Jiang
    title: Senior Full Stack Engineer, Lumina
    url: https://www.linkedin.com/in/yuneng-david-jiang-455676139/
    image_url: https://avatars.githubusercontent.com/u/171294688?v=4
hide_table_of_contents: false
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Deploy this version

<Tabs>
<TabItem value="docker" label="Docker">

```bash
docker run \
-e LUMINA_MASTER_KEY=sk-<paste-a-long-random-key> \
-e DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<dbname> \
-e STORE_MODEL_IN_DB=True \
-p 4000:4000 \
docker.lumina.ai/soventra/lumina:1.104.2
```

</TabItem>
<TabItem value="pip" label="Pip">

```bash
pip install lumina==1.104.2
```

</TabItem>
</Tabs>

This release is published as [`ghcr.io/soventra/lumina:v1.104.2`](https://github.com/Soventra/lumina/pkgs/container/lumina). See the [GitHub release](https://github.com/Soventra/lumina/releases/tag/v1.104.2) and the full [releases page](https://github.com/Soventra/lumina/releases)

`v1.104.2` is a patch release on top of [`v1.104.1`](/release_notes/v1.104.1/v1-104-1). It adds the Decisions API routes and providers. There are no new database migrations or breaking changes: the Decisions routes are new on this line. The `v1.104.2` tag points at [`fc3920b`](https://github.com/Soventra/lumina/commit/fc3920bf403124ad075bc04990f999f7e0612e12)

## Decisions API

The proxy now serves decision models, which answer typed questions (yes/no predicates, choices and scores) about an input. Requests go through the usual keys, budgets, spend tracking and guardrails. See the [Decisions docs](../../docs/decisions)

- **Two request formats**
    - `POST /v1/decisions` and `POST /decisions` take OpenAI's Decisions API format: `input` plus a `questions` list, answered as an `answers` list with OpenAI-style `usage`
    - `POST /v1/systemone` and `POST /systemone` take the System One format: `state` plus a named `questions` map, answered as an `answers` map keyed by question name
    - Both routes go through one shared format inside the proxy, so any Decisions model can be called on either route
- **Providers**: `openai/` (`gpt-6-luna`), `perplexity/`, `typesafe/`, `openrouter/`, `cloudflare/clef` and `cloudflare/clef-flash`, and self-hosted `strands_decider/` (requires `api_base`)
- **OpenAI**: images, multi-message input, `safety_identifier`, names and refusals pass through on `/v1/decisions`. The provider reads `lumina.api_key`, `lumina.openai_key`, `lumina.api_base`, `OPENAI_BASE_URL` and `OPENAI_API_BASE` in the same order as other OpenAI calls
- **Validation before any upstream call**: a missing `state`, a malformed question, more than 128 questions, a single-option question or a body that is not JSON returns 400. Image input sent to a provider that only accepts text returns a clear 400
- **Spend tracking**: per-token pricing from the cost map, with cached and cache-write input tokens billed at their own rates
- **Health checks**: `/health` probes `mode: evaluation` deployments with a one-question Decisions call, and `health_check_params` can override its `state` and `questions`
- **Guardrails**: OpenAI-format responses include `guardrail_information` when the caller sets `include_guardrail_response`
- **Pass-through**: an existing `pass_through_endpoints` entry at `/v1/decisions` keeps answering that path, while `/decisions` serves the native route

#### New Model Support (6 new models)

| Provider | Model | Context Window | Input ($/1M tokens) | Output ($/1M tokens) |
| --- | --- | --- | --- | --- |
| Perplexity | `perplexity/pplx-decider-v1-27b` | 262K | $0.04 | $0.00 |
| Cloudflare | `cloudflare/clef` | 65K | $0.24 | $0.00 |
| Cloudflare | `cloudflare/clef-flash` | 65K | $0.09 | $0.00 |
| Cloudflare | `cloudflare/@cf/cloudflare/clef` | 65K | $0.24 | $0.00 |
| Cloudflare | `cloudflare/@cf/cloudflare/clef-flash` | 65K | $0.09 | $0.00 |
| Strands Decider | `strands_decider/strands-decider-2B-hobson-v19` | - | $0.00 (self-hosted) | $0.00 |

The existing `gpt-6-luna` entry now lists `/v1/decisions` among its supported endpoints

### What's Changed

- Add a unified `/v1/decisions` endpoint for System One-compatible providers - [PR #44236](https://github.com/Soventra/lumina/pull/44236)
- Serve the System One format at `/v1/systemone` and OpenAI's format at `/v1/decisions` - [PR #45184](https://github.com/Soventra/lumina/pull/45184)
- Add OpenAI as a Decisions provider behind a shared decisions format - [PR #45214](https://github.com/Soventra/lumina/pull/45214)

All three are backported in [PR #45190](https://github.com/Soventra/lumina/pull/45190)

## Full Changelog

https://github.com/Soventra/lumina/compare/v1.104.1...v1.104.2
