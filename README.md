# figma-name-components

Figma component naming skill for Codex.

This skill audits and renames Figma components according to the bundled naming rules:

- `references/Naming_Rules.md`
- `references/Naming_Component_Notes.md`

## What It Does

- Audits Figma page or module component names.
- Preserves human-readable `display_name`.
- Normalizes machine-readable `component_id` and `variant_id`.
- Skips pure text layers, first-level page frames, and `COMPONENT_SET` containers.
- Generates an HTML conflict report only when visually identical nodes have different `display_name` values.

## Requirements

- Codex with local skill support.
- Figma MCP access.
- The companion `figma-use` skill must be available before `use_figma` write operations.

## Validate

Run from this package root:

```bash
python3 scripts/build_figma_name.py \
  --display-name "酒店商品卡/酒店名称=2行" \
  --page-id "LIST" \
  --component-id "LIST.HOTEL_CARD.HOTEL_NAME" \
  --variant-id "LONG_TEXT_2_LINES"
```

Run tests:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```
