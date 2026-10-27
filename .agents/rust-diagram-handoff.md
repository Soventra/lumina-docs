# Rust migration diagram continuation

Continue on `codex/rust-diagram-refinements` in `BerriAI/litellm-docs`. The original article PR, #2605, merged on October 26, 2026. This branch starts from the updated `main` and contains only the subsequent diagram refinements and the portable skill resources.

The article is `blog/rust_migration_rerouted/index.md`, rendered at `/blog/rust-migration-rerouted`. Preserve Nate's prose. He authorized only mechanical copy fixes in the previous revision. Ask him for missing facts instead of assuming they do not exist. He strongly prefers one commit per feature branch: amend the existing feature commit for further changes and use force-with-lease when asked to push.

The latest Sankey is `blog/rust_migration_rerouted/rust-request-mix.svg`. One incoming request stream forks at the top into fast-path candidates and Python requests. Blue means eligible so far, rather than the final intersection throughout the diagram. It starts at about 60% and ends at about 20%. The illustrative cumulative shares after endpoint, routing, callbacks, and provider are 48%, 36%, 27%, and 20%. More traffic branches away between endpoint and routing. Branches merge into the left edge of the Python lane, whose right edge stays fixed; this shortens their horizontal travel. There is more vertical space for smooth, visible curves. Matching option cards are centered on the same horizontal lines. No numbers appear in the diagram.

Endpoint, routing, and provider are choose-one layers. Callbacks are choose-many; spend logging and S3 logs can both apply to the same request. Unsupported callback examples remain in the Python lane. Provider eligibility is scoped to Anthropic models on Anthropic, Amazon Bedrock, and Vertex AI. The mix is illustrative, not production telemetry. Nate has seen the latest image; await further visual feedback before treating it as final.

The repository-local skill is `.agents/skills/litellm-paper-diagrams/SKILL.md`. It includes the paper schematic style, examples, helpers, animation reference, and the latest cumulative eligibility rules. The SVG generator is `.agents/skills/litellm-paper-diagrams/scripts/render_request_mix.py`. Regenerate with:

```sh
python3 .agents/skills/litellm-paper-diagrams/scripts/render_request_mix.py \
  --model blog/rust_migration_rerouted/request-mix-model.json \
  --output blog/rust_migration_rerouted/rust-request-mix.svg
```

The other diagrams and dark particle-flow header were approved earlier. Keep their functional labels and omit decorative framing, titles, subtitles, stamps, and edge text. The timing diagram has three bars: Python cold profile at 48.1 ms, illustrative partial Rust at about 32 ms with 17 ms of work accelerated 20x, and full Rust messages hot path at 1.7 ms. The post's separate 1.5 ms target wording is Nate's copy; do not change it without asking. The header sends common requests quickly through Rust and other requests through Python, with pause and reduced-motion support.

Local checks passed: writing style, Markdown structure, SVG rendering at full and reading widths, and whitespace. A full build passed before the later SVG-only refinements. Re-run the appropriate checks after subsequent changes. On a cloud machine install the dependencies required by the repository; do not use the previous machine's absolute paths. A local server can run with `LITELLM_DOCS_OFFLINE=1 npm start -- --host 0.0.0.0 --port 3000 --no-open`.

To resume in a cloud task, use the repository's published cloud environment, start from `codex/rust-diagram-refinements`, read this note and the skill, and preserve the current artwork pending Nate's next instructions. No cloud task was started by the local session because its Cloud CLI returned no configured environments.
