---
title: "Lumina v1.103.1, v1.102.2, v1.101.3 and v1.100.4 fix UI and CLI session tokens"
description: "Changes UI and CLI session tokens to AES-256-GCM tokens that start with lumina_login_. Admin UI and lite CLI users must log in again."
slug: "v1-102-2"
date: 2026-09-30T00:58:30
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
docker.lumina.ai/soventra/lumina:1.102.2
```

</TabItem>
<TabItem value="pip" label="Pip">

```bash
pip install lumina==1.102.2
```

</TabItem>
</Tabs>

This release is published as [`ghcr.io/soventra/lumina:v1.102.2`](https://github.com/Soventra/lumina/pkgs/container/lumina). See the [GitHub release](https://github.com/Soventra/lumina/releases/tag/v1.102.2) and the full [releases page](https://github.com/Soventra/lumina/releases)

:::danger Breaking Changes

**Session tokens issued before the upgrade stop working.** Admin UI and `lite` CLI users sign in once more after upgrading. During a rolling upgrade, pods on the old and new versions reject each other's session tokens, so finish the rollout before asking users to sign in again. Virtual keys, the master key and stored credentials are unaffected. See [`1d5fdc8`](https://github.com/Soventra/lumina/commit/1d5fdc87fed66b49e1df8cf7d708ad93249eb7d0)

:::

:::warning `lite` CLI users must log in again

After upgrading the proxy, every `lite` CLI user has to run `lite login` once more. Until they do, the CLI keeps sending its old session token and its requests to the proxy fail

:::

`v1.102.2` is a patch release on top of [`v1.102.1`](https://github.com/Soventra/lumina/releases/tag/v1.102.1). It carries one change: the session tokens the Admin UI and the `lite` CLI receive after sign-in now use their own encryption context and a header-safe format. Both the Docker image and the PyPI package were built from [`a0c4a33`](https://github.com/Soventra/lumina/commit/a0c4a3347afe19decf500ecf436f21d7fb471c34)

## UI and CLI session tokens get their own format

Session tokens were encrypted with the same routine the proxy uses for stored credentials, so they carried a `v2:gcm:` prefix and base64 padding. Basic auth parsers split on the first `:` and browsers reject `:` and `=` in WebSocket subprotocols, so Langfuse pass-through and the realtime playground could not use them. About one login in 262,144 also produced a token starting with `sk-`, which the proxy then treated as a virtual key and rejected with a 401

Session tokens are now AES-256-GCM encrypted under a context of their own and returned as `lumina_login_` followed by unpadded base64url. They pass through any header, are easy to spot in logs, and are checked only as session tokens. Stored credentials keep their current encryption, so there is nothing to migrate

### What's Changed

- refactor(auth): bind UI/CLI session tokens to their own AES-GCM context - [`1d5fdc8`](https://github.com/Soventra/lumina/commit/1d5fdc87fed66b49e1df8cf7d708ad93249eb7d0)
- chore(lint): scope a TRY004 suppression to the bearer-token salt key check - [`02a0dc1`](https://github.com/Soventra/lumina/commit/02a0dc1480754f12c3244d4ce866bb3fe9af4ba0)

## Full Changelog

https://github.com/Soventra/lumina/compare/v1.102.1...v1.102.2
