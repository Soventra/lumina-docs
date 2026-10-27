---
title: "Lumina v1.102.4 fixes double-counted spend on the chat to Responses bridge"
description: "Fixes spend that was logged twice for large non-streaming chat requests to openai/responses models, so key, team and daily spend match real cost."
slug: "v1-102-4"
date: 2026-10-08T07:49:06
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
docker.lumina.ai/soventra/lumina:1.102.4
```

</TabItem>
<TabItem value="pip" label="Pip">

```bash
pip install lumina==1.102.4
```

</TabItem>
</Tabs>

This release is published as [`ghcr.io/soventra/lumina:v1.102.4`](https://github.com/Soventra/lumina/pkgs/container/lumina). See the [GitHub release](https://github.com/Soventra/lumina/releases/tag/v1.102.4) and the full [releases page](https://github.com/Soventra/lumina/releases)

`v1.102.4` is a patch release on top of [`v1.102.3`](/release_notes/v1.102.3/v1-102-3). It fixes spend that was logged twice for large non-streaming chat requests. There are no new database migrations or breaking changes. The `v1.102.4` tag points at [`0de9a17`](https://github.com/Soventra/lumina/commit/0de9a178571aaaf3c96a56816e9c4734e977a315)

## Spend logged once on the Chat to Responses bridge

Since `v1.102.0`, a large non-streaming `/v1/chat/completions` request to an `openai/responses/*` model was logged twice. The request showed two rows on the logs page, and key, team and daily spend went up by twice the real cost

- One request now queues exactly one success log, and the logged result is the provider's own response
- Streaming requests and the success handler itself are unchanged

### What's Changed

- Log spend once for large non-streaming requests on the chat to Responses bridge - [PR #44508](https://github.com/Soventra/lumina/pull/44508), backported in [PR #45215](https://github.com/Soventra/lumina/pull/45215)

## Full Changelog

https://github.com/Soventra/lumina/compare/v1.102.3...v1.102.4
