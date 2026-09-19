from typing import Dict, Any
import json
import os


def save_report(output_dir: str, idx: int, result: Dict[str, Any]) -> None:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"test_{idx}.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
