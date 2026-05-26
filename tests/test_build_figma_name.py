import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "build_figma_name.py"
)


class BuildFigmaNameCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def parse_success(self, *args: str) -> dict:
        result = self.run_cli(*args)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        return json.loads(result.stdout)

    def assert_failure(self, expected_message: str, *args: str) -> None:
        result = self.run_cli(*args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(expected_message, result.stderr)

    def test_builds_visible_name_without_variant(self) -> None:
        payload = self.parse_success(
            "--display-name",
            "酒店卡片/图片区",
            "--page-id",
            "LIST",
            "--component-id",
            "LIST.HOTEL_CARD.IMAGE_AREA",
        )
        self.assertEqual(payload["visible_name"], "酒店卡片/图片区｜LIST.HOTEL_CARD.IMAGE_AREA")
        self.assertNotIn("variant_id", payload)

    def test_builds_visible_name_with_machine_side_variant_separator(self) -> None:
        payload = self.parse_success(
            "--display-name",
            "搜索模块/Tab切换区=国内",
            "--page-id",
            "HOME",
            "--component-id",
            "HOME.SEARCH_MODULE.TAB_SWITCH",
            "--variant-id",
            "DOMESTIC",
        )
        self.assertEqual(
            payload["visible_name"],
            "搜索模块/Tab切换区=国内｜HOME.SEARCH_MODULE.TAB_SWITCH#DOMESTIC",
        )
        self.assertEqual(payload["variant_id"], "DOMESTIC")

    def test_preserves_figma_variant_property_prefix(self) -> None:
        payload = self.parse_success(
            "--display-name",
            "Tab切换区=国内",
            "--page-id",
            "HOME",
            "--component-id",
            "HOME.SEARCH_MODULE.TAB_SWITCH",
            "--variant-id",
            "DOMESTIC",
            "--figma-variant-property",
            "Tab切换区",
        )
        self.assertEqual(
            payload["visible_name"],
            "Tab切换区=国内｜HOME.SEARCH_MODULE.TAB_SWITCH#DOMESTIC",
        )
        self.assertEqual(payload["figma_variant_property"], "Tab切换区")

    def test_builds_visible_name_with_component_set_semantic_property_name(self) -> None:
        payload = self.parse_success(
            "--display-name",
            "猜你喜欢/酒店卡片/标题区=常规",
            "--page-id",
            "HOME",
            "--component-id",
            "HOME.RECOMMENDED.HOTEL_CARD.TITLE_AREA",
            "--variant-id",
            "DEFAULT",
            "--figma-variant-property",
            "猜你喜欢/酒店卡片/标题区",
        )
        self.assertEqual(
            payload["visible_name"],
            "猜你喜欢/酒店卡片/标题区=常规｜HOME.RECOMMENDED.HOTEL_CARD.TITLE_AREA#DEFAULT",
        )
        self.assertEqual(payload["figma_variant_property"], "猜你喜欢/酒店卡片/标题区")

    def test_rejects_raw_hash_in_input_fields(self) -> None:
        self.assert_failure(
            "raw naming fields must not contain #",
            "--display-name",
            "搜索模块/Tab切换区=国内",
            "--page-id",
            "HOME",
            "--component-id",
            "HOME.SEARCH_MODULE.TAB_SWITCH#DOMESTIC",
            "--variant-id",
            "DOMESTIC",
        )


if __name__ == "__main__":
    unittest.main()
