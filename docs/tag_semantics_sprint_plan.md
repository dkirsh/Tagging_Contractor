# Tag Semantics Sprint Plan (based on audit)

## What to do first (highest leverage)
1. **Fill semantics for the 95 tags that participate in relations** (relation_count > 0). These are the tags your graph “talks about,” so clarifying them improves the whole system.
2. Within those, start with the **top hubs** (highest relation_count / centrality) and with **alias_count == 0** (worst searchability).

## Deliverables included
- `tag_prioritization_top95.csv`: ranked list of the 95 relation-linked tags with alias counts and notes.
- `tag_semantics_top20.jsonl`: ready-to-paste semantics entries for the top 20 hub tags (short/long definition, aliases, examples, scope, extraction notes 2D/3D).

## Suggested sprint cadence
- Sprint 1: Top 20 hubs (seed JSONL).
- Sprint 2: Next 30 hubs (ranks 21–50 in `tag_prioritization_top95.csv`).
- Sprint 3: Remaining 45 relation-linked tags (ranks 51–95).
- Sprint 4+: High-usage non-relational tags ordered by your UI’s actual frequency-of-use logs (if available).
