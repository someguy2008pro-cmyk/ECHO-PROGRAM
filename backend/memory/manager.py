
import json
import os
from pathlib import Path
from datetime import datetime, timezone

MEMORY_FILE = Path(
    os.getenv("ECHO_MEMORY_FILE", "data/memories.json")
)


def load_memories():
    if not MEMORY_FILE.exists():
        return []

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def save_memory(content, category="general"):
    content = content.strip()

    if not content:
        raise ValueError("Memory cannot be empty.")

    memories = load_memories()

    memory = {
        "memory_id": str(len(memories) + 1),
        "content": content,
        "category": category,
        "status": "approved",
        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    memories.append(memory)

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            memories,
            file,
            ensure_ascii=False,
            indent=2
        )

    return memory


def get_memories():
    return load_memories()
  
