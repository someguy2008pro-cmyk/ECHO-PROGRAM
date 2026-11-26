
import json
import os
import unicodedata
from pathlib import Path
from datetime import datetime, timezone

MEMORY_FILE = Path(
    os.getenv("ECHO_MEMORY_FILE", "data/memories.json")
)


def normalize(text):
    text = text.casefold()
    text = unicodedata.normalize("NFD", text)
    return "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
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
        "memory_id": str(
            max(
                [int(m.get("memory_id", 0))
                 for m in memories
                 if str(m.get("memory_id", "")).isdigit()]
                + [0]
            ) + 1
        ),
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


def search_memories(query):
    query = normalize(query.strip())

    if not query:
        return []

    keywords = set(query.split())
    results = []

    for memory in load_memories():
        if memory.get("status") != "approved":
            continue

        content = normalize(memory.get("content", ""))
        category = normalize(memory.get("category", ""))

        score = sum(
            1 for word in keywords
            if word in content or word in category
        )

        if score > 0:
            results.append({
                **memory,
                "relevance_score": score
            })

    return sorted(
        results,
        key=lambda item: item["relevance_score"],
        reverse=True
    )
    
