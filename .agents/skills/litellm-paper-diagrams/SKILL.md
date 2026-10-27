---
name: litellm-paper-diagrams
description: Create editable explanatory diagrams for LiteLLM blog posts in Nate's approved white-and-blue paper schematic style, including architecture, request flow, timing, and traffic mix diagrams. Use for this visual style or requests to match recent LiteLLM technical illustrations.
---

# LiteLLM paper diagrams

Create explanatory diagrams in the white schematic direction Nate selected on October 26, 2026. The approved style uses a pale paper surface, restrained blue lines, orthogonal connectors, direct labels, and a faint dot grid. Use it for explanations inside a blog post. The cobalt isometric HANDOFF hero and dark Lens particle field are separate directions; use them only when requested.

Keep only functional labels. Nate explicitly removed decorative framing: repeated LiteLLM eyebrows, source stamps, promotional headings, subtitles, and editorial footer notes. Do not add them by default. Keep component names, choice labels, legends, and annotations that explain the mechanism. The request-time bars have no overall title or subtitle; their row and segment labels provide the explanation. Put essential measurement scope into the relevant row label or accessible description rather than surround every figure with caveats.

## Establish the content

Read the target draft and applicable repository instructions before drawing. Identify the claim each diagram explains, the components, relationships, units, and any proposed behavior. Keep the author's surrounding prose unless the diagram requires a small correction or the user requests an edit.

Ask the author for missing facts before making a factual design decision. Specifically, ask for the timing breakdown, traffic proportions, supported combinations, or source sketch when the draft does not contain what the requested diagram needs. Do not assume the data does not exist, invent values, silently remove requested detail, or substitute an unscaled schematic without the author's agreement. Continue independent diagrams and layout work while an answer is pending. Once supplied, use the values and state the measurement scope where it affects interpretation.

For timing diagrams, distinguish proxy overhead from provider latency and keep before/after scales consistent. Preserve nested spans as nested; do not sum them into a new total. If the source is a screenshot, retain its duration labels and relative positions without inventing exact start timestamps. For traffic diagrams, establish the denominator and whether a split is conditional or a share of all traffic. Endpoint, routing, callback, and provider percentages alone do not establish their joint distribution. A measured Sankey requires counts for connected combinations; ask for them rather than assume independence. If the author explicitly asks for a qualitative traffic mix, show the intended dominant path, omit percentages, and label widths as illustrative. Leave uncertain callback names generic unless the source confirms them. Show alternative fallback criteria as alternatives; do not link them into a sequence that implies they must all occur together.

If the author requests a semi-realistic synthetic mix, use their ratios exactly and label the other modeling assumptions. Save the model beside the diagram so the weights are reviewable. Independent stage choices are appropriate when explicitly selected for an illustrative model, not as an inference about measured traffic. Keep one traffic-width scale for every row, preserve each node's incoming and outgoing totals, and use denser pairwise links when the author wants the broader mix visible. In the October 26 example, endpoint weights are 9:3:2:1 for Messages, chat completions, responses, and other APIs; 60% of every upstream group uses simple shuffle, supported callback sets, and native Anthropic providers at each respective layer. Those are illustrative choices, not product telemetry or defaults for future diagrams.

Choose the diagram form to explain the author's claim. For the effect of a partial migration on total time, use aligned horizontal stacked bars on the same scale. Highlight the work that moves to Rust, shorten that portion in the partial-migration bar, and keep the widths of unchanged Python work identical. Add a full-Rust bar when requested and a relevant total is supplied. Distinguish cold-profile stages, modeled partial migration, and measured hot-path totals in their row labels. Do not infer a hot-path breakdown from cold-path spans. For the October 26 post, Nate corrected the full-Rust hot-path total to 1.7 ms; this replaces the separate Rust cold profile as the source for that bar. Use a waterfall when the requested explanation is a chronological trace; a supplied waterfall can be source data for a different diagram form. Distinguish an illustrative speedup from measured before/after timings.

The paper style is already approved. Do not reopen style selection for every figure. If the user requests a new direction, show a small set of samples and get feedback before completing the set.

For configuration-scope diagrams, arrange layers from top to bottom and list the available options left to right within each layer. Highlight the selected subset in blue and retain other real LiteLLM options in muted cards so readers can see the scope. Distinguish a single routing strategy from multiple callbacks or alternative providers. Label a model-family restriction such as Anthropic models on Bedrock or Vertex explicitly. The connecting arrows describe configuration layers, not callback execution order. Confirm actual option names against the relevant source docs and selected support against the author or implementation. See [assets/configuration-options.svg](assets/configuration-options.svg) for the accepted row layout; its selections are specific to the October 26 Rust post.

When showing flow across these choices, use Sankey-style curved ribbons between cards. Spread the highlighted choices across the rows rather than put all selections at the start. Give ribbons enough vertical room to curve without crossing labels. For the requested destination emphasis, make each selected ribbon light at its source and progressively darker blue as it approaches the next highlighted card. Use faint neutral ribbons for alternative paths. Draw ribbons behind the cards, with precise connections at the card edges. Label illustrative widths as illustrative; callback branches can overlap and do not imply mutually exclusive request counts.

Keep port marks tied to actual connections. The first endpoint row has no incoming port strip, and the final provider row has no outgoing strip. Avoid blue bars that protrude from open ends of the diagram.

When blue denotes an end-to-end fast path, color only the intersection of every eligible condition blue throughout the diagram. A request that reaches one eligible node but fails another condition remains gray. Use a pale-blue card or outline for eligible choices and a stronger blue ribbon for the fully eligible cohort. Conserve the blue cohort at every intermediate node as well as the total flow.

For a cumulative eligibility diagram, blue instead means "Fast-path eligible so far." Its width decreases as unsupported configurations leave; only the final blue stream meets every condition. Do not apply the constant blue-intersection rule to this mode. Nate selected this quieter treatment for the Rust post: one joined input forks at the top, aligned option rows show supported configurations and Python alternatives, and fallback branches join the left edge of a Python lane with a fixed right edge. Move the blue trunk nearer that lane and give the branches enough vertical space to keep their width visible. Include a departure between endpoint and routing. Keep callbacks choose-many and percentages hidden. The approved illustrative mix starts with 60% candidates and retains 48%, 36%, 27%, and 20% of all requests after successive rows. These values describe the example's design, not production traffic or defaults for other diagrams.

See [assets/progressive-eligibility.svg](assets/progressive-eligibility.svg) and [assets/progressive-eligibility-model.json](assets/progressive-eligibility-model.json) for this treatment. The worked renderer accepts explicit model and output paths:

```sh
python3 .agents/skills/litellm-paper-diagrams/scripts/render_request_mix.py \
  --model blog/rust_migration_rerouted/request-mix-model.json \
  --output blog/rust_migration_rerouted/rust-request-mix.svg
```

This renderer implements the four-row Rust-post example. Adapt its options, layout, and scale for another subject.

Show choice cardinality explicitly. Endpoints, routing strategies, and providers are choose-one rows for each request. Callbacks are choose-many: show one enclosing stage labeled "Choose any combination" with checkbox-style options, and let the request ribbons pass through the whole stage. Highlight spend logging and S3 as callbacks that can both apply to the same request. Do not display S3 only, spend only, and both as the user-facing callback choices unless the author specifically wants to explain those partitions. For internal flow accounting, disjoint callback cohorts can still count overlapping selections once; keep that bookkeeping out of the visible choice model. A dense routing-to-provider flow can pass behind the enclosing callback stage, with callback eligibility included in the end-to-end blue cohort.

Weighted ribbons do not require visible numbers. When the author wants qualitative presentation, retain the ratios in the source model and use them for widths while removing percentages, counts, computed cohort totals, and numeric margin notes from the SVG and alt text. Preserve technical names such as S3 and /v1/messages.

[assets/request-mix-model.json](assets/request-mix-model.json) and [assets/configuration-options.svg](assets/configuration-options.svg) provide the worked synthetic example. [scripts/sankey_flow.py](scripts/sankey_flow.py) computes exact rational stage shares and separates fully eligible traffic from the rest. It requires an explicit illustrative independent model and rejects measured-data models. Use actual joint counts or cohorts for measured diagrams. The resulting pairwise edges can be drawn as adjacent blue and gray sub-bands, with matching allocations at each node.

Provider comparisons must distinguish native Messages APIs from LiteLLM's translation support. For example, say Azure OpenAI when showing a translated route; Azure Foundry also serves Claude natively. Verify the relevant deployments in [the native Messages documentation](https://docs.litellm.ai/docs/anthropic_unified/native_passthrough) and [client setup guide](https://docs.litellm.ai/docs/proxy/client_setup/overview). Avoid implying that an unhighlighted provider cannot be called through LiteLLM's Messages endpoint.

## Visual rules

Use editable SVG for lines, labels, and shapes. Set a responsive `viewBox` and a fixed paper-colored background. The diagram canvas does not need an outer frame. A useful starting width is 1040 units with 40-unit outer margins. Choose the height to fit the content rather than compress labels.

| Role | Value |
| --- | --- |
| Paper | `#fbfcfe` |
| Primary text | `#18334b` |
| Active path and selected component | `#123ec9` |
| Secondary text | `#597189` |
| Neutral borders | `#9db2ce` |
| Container fill | `#f0f5fc` |
| Container border | `#a8bad3` |
| Outer rules | `#dce4ee` |
| Decorative dots | `#8aa6cc` at about 23% opacity |

Use `Arial, Helvetica, sans-serif` for portable SVG text. Match Geist when the target renderer has the actual font available. Use a generic `monospace` fallback for API paths and code labels. At a 1040-unit width, start with 22 to 24-unit component labels and 18-unit explanations. Keep essential labels readable at the blog's actual content width. Keep sentence case for content. Boundary labels such as `ONE HOST` are functional; brand eyebrows and other decorative metadata are omitted.

Draw borders at about 1.3 units and connectors at about 1.8 units. Use 4 to 8-unit corner radii for component boxes. Align boxes and connectors to a simple grid. Leave clear gaps between connectors, text, and container edges. Route connections through gutters outside component interiors; avoid crossing a label or an unrelated node. Use real arrowheads rather than Unicode arrow characters. Match arrowhead and line colors.

Blue identifies the principal request path or selected behavior. Use darker neutral lines for fallback request paths. Use dashed muted lines for secondary relationships such as shared state access, with a small legend whenever line styles have different meanings. Give host, process, and service boundaries explicit labels. A branch to Python is a forwarding path, not an automatic retry after an error, unless the source says so.

Use the dot grid lightly in open drawing areas. Keep card surfaces flat, with generous whitespace and no shadows, decorative 3D, rainbow palettes, or promotional badges. Destination-darkening gradients on request ribbons are an approved exception to flat fills. Do not add a visible figure title, LiteLLM logo, version, date, or speed claim unless the user asks or it is needed to explain the mechanism.

## Create and deliver

Inspect [assets/paper-template.svg](assets/paper-template.svg) for the visual baseline. For migration comparisons, inspect [assets/partial-migration-bars.svg](assets/partial-migration-bars.svg): the partial Rust portion shrinks while unchanged segments retain their widths, and a third bar shows the full-Rust hot path. Its 17 ms migrated portion, illustrative 20x speedup, and 1.7 ms full-Rust hot-path total were confirmed by Nate for the October 26 Rust post; obtain the relevant values for a new subject rather than reuse those numbers as defaults. Adapt the arrangement to the concept. The small standard-library module [scripts/paper_svg.py](scripts/paper_svg.py) supplies palette tokens and primitives for text, rectangles, connectors, and a dot grid; its default omits visible headings and eyebrows. It does not choose diagram semantics or supply data.

Save production SVGs beside the post when that matches the repository, and reference them through relative image links. Add meaningful Markdown alt text and SVG `title`/`desc` elements that explain the diagram's relationships. Keep decorative elements out of accessibility text. Include local image assets in the deliverable rather than leave project references pointing to temporary files.

Render every finished SVG and inspect it at full size and at the article's content width. For example, when librsvg is installed:

```sh
rsvg-convert diagram.svg -o /tmp/diagram.png
rsvg-convert -w 720 diagram.svg -o /tmp/diagram-reading-width.png
```

Use the available image viewer to inspect the PNGs. Correct clipping, weak essential text, awkward wraps, connectors through labels, misleading widths, and indistinguishable branches. Check SVG XML, local image references, and the relevant Markdown/MDX integration. Run a full site build when the environment supports it and the changes require it; report the verification actually completed.

Present a visual preview and link the editable source. Explain any unresolved fact or measurement assumption explicitly. Do not publish, commit, or create a PR unless the user asks.

## Reference lineage

### Dark particle-flow header

A dark animated header is an approved companion to the light explanatory diagrams when the user requests this direction. For the Rust migration post, common requests stream quickly through Rust while the remaining requests move through Python at the existing rate, then both routes reach providers. Use motion and density to explain the difference; do not present the illustrative particle cycle times as measured latency or throughput.

[assets/RequestFlowHero.js](assets/RequestFlowHero.js) and [assets/request-flow-hero.module.css](assets/request-flow-hero.module.css) contain the worked Docusaurus header. They use deterministic particles and SVG motion paths, a dark background, sparse pixel trails, and labeled Rust and Python branches. With the existing blog theme, import the component into MDX and export it as `Hero` to place it inside the standard header rather than create a second title or byline. Both source files belong beside the post when copied into a new article.

Keep the hero's path labels and pause control, but omit brand stamps and footer commentary. The pause button can overlay a quiet corner of the figure instead of adding a separate caption bar.

Animation code must render safely on the server and hydrate consistently. Use seeded positions instead of render-time randomness, read browser motion preferences inside effects, provide a pause/play control, pause while offscreen or in a hidden tab, and clean up observers and listeners. Honor reduced-motion preferences and leave a useful static composition when paused. Check the speed contrast and labels in the actual article at reading width. Verify that paused frames remain stable and that playback resumes before publishing.

### Source posts

The approved direction combines the light technical illustrations in [the cloud-agent workshop post](https://docs.litellm.ai/blog/cloud-agent-workshop) with the sparse labels and infrastructure boundaries in [HANDOFF](https://handoff.litellm.ai/). The workshop source uses Geist, blue accents, light panels, thin borders, and line icons. The approved sample simplifies those elements into a flat schematic. [Lens](https://docs.litellm.ai/blog/litellm-lens-launch) uses a distinct particle-and-motion treatment, while [Moyai](https://docs.litellm.ai/blog/moyai-open-source) uses an atmospheric launch hero. Do not treat all of these as one identical house style.
