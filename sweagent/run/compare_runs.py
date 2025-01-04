import argparse
import json
from pathlib import Path


def get_resolved(path: Path) -> set[str]:
    data = json.loads(path.read_text())
    if "resolved" in data:
        data["resolved_ids"] = data["resolved"]
    return set(data["resolved_ids"])


def get_submitted(path: Path) -> set[str]:
    return set(json.loads(path.read_text())["submitted_ids"])


def compare(new_path, old_path, *, show_same=False):
    evaluated_ids = get_submitted(new_path)
    old_evaluated_ids = get_submitted(old_path)

    for id in evaluated_ids:
        resolved_now = id in get_resolved(new_path)
        resolved_before = id in get_resolved(old_path)
        if id not in old_evaluated_ids:
            emoji = "❓"
        elif resolved_now and not resolved_before:
            emoji = "😀"
        elif resolved_now and resolved_before:
            emoji = "✅"
            if not show_same:
                continue
        elif not resolved_now and resolved_before:
            emoji = "❌"
        else:
            emoji = "👾"
            if not show_same:
                continue
        print(f"{emoji} {id}")


def run_from_cli(_args: list[str] | None = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("new_path", type=Path)
    parser.add_argument("old_path", type=Path)
    parser.add_argument("--show-same", action="store_true")
    args = parser.parse_args(_args)
    print("Emoji legend:")
    print("❓: Not evaluated in old version")
    print("😀: Newly resolved in new version")
    print("✅: Resolved in both")
    print("❌: Resolved in old, not in new")
    print("👾: Unresolved in both")
    print("-" * 80)
    compare(args.new_path, args.old_path, show_same=args.show_same)
