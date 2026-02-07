"""Recipe data model."""

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path

RECIPES_FILE = Path.home() / ".recipe-book" / "recipes.json"


@dataclass
class Recipe:
    id: int
    name: str
    ingredients: list[str] = field(default_factory=list)
    instructions: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


def load_recipes():
    if not RECIPES_FILE.exists():
        return []
    content = RECIPES_FILE.read_text().strip()
    if not content:
        return []
    return [Recipe.from_dict(r) for r in json.loads(content)]


def save_recipes(recipes):
    RECIPES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RECIPES_FILE, "w") as f:
        json.dump([r.to_dict() for r in recipes], f, indent=2)
