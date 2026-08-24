#!/usr/bin/env python3

import argparse
import json
import re
import sys

PAGE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
COMPONENT_RE = re.compile(r"^[A-Z][A-Z0-9_]*(\.[A-Z][A-Z0-9_]*)*$")
VARIANT_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Naming_Rules fields and build the canonical Figma visible name."
    )
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--page-id", required=True)
    parser.add_argument("--component-id", required=True)
    parser.add_argument("--variant-id")
    parser.add_argument(
        "--figma-variant-property",
        help="Optional legacy escape hatch. Normal skill workflow should preserve the existing 属性名= prefix separately instead of parsing, comparing, or displaying it.",
    )
    args = parser.parse_args()

    display_name = args.display_name.strip()
    page_id = args.page_id.strip()
    component_id = args.component_id.strip()
    variant_id = args.variant_id.strip() if args.variant_id else None
    figma_variant_property = (
        args.figma_variant_property.strip() if args.figma_variant_property else None
    )

    if not display_name:
        fail("display_name must not be empty")
    if "｜" in display_name or "|" in display_name:
        fail("display_name must not contain | or ｜")
    if "#" in display_name or "#" in component_id or (variant_id and "#" in variant_id):
        fail("raw naming fields must not contain #; the machine-side variant separator is added automatically")
    if display_name.count("=") > 1:
        fail("display_name can contain at most one =")

    if not PAGE_RE.fullmatch(page_id):
        fail("page_id must use uppercase English and underscores only")

    if not COMPONENT_RE.fullmatch(component_id):
        fail("component_id must use uppercase dot-separated segments")

    first_segment = component_id.split(".", 1)[0]
    if first_segment != page_id:
        fail("component_id must start with page_id under the current Naming_Rules")

    if variant_id and not VARIANT_RE.fullmatch(variant_id):
        fail("variant_id must use uppercase English and underscores only")
    if figma_variant_property:
        if "=" in figma_variant_property:
            fail("figma_variant_property must not contain =")
        if not variant_id:
            fail("variant_id is required when figma_variant_property is present")

    has_display_variant = "=" in display_name
    if has_display_variant:
        display_base, display_variant = display_name.split("=", 1)
        if not display_base or not display_variant:
            fail("display_name variant format must be display_name=变体名")
    if variant_id and not has_display_variant:
        fail("display_name must include =变体名 when variant_id is present")
    if not variant_id and has_display_variant:
        fail("variant_id is required when display_name includes =变体名")

    visible_name = f"{display_name}｜{component_id}"
    if variant_id:
        visible_name = f"{visible_name}#{variant_id}"
    if figma_variant_property:
        if figma_variant_property != display_base:
            fail("figma_variant_property must match the display_name base before =")
        visible_name = f"{figma_variant_property}={display_variant}｜{component_id}#{variant_id}"

    payload = {
        "display_name": display_name,
        "page_id": page_id,
        "component_id": component_id,
        "visible_name": visible_name,
    }
    if variant_id:
        payload["variant_id"] = variant_id
    if figma_variant_property:
        payload["figma_variant_property"] = figma_variant_property

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
