"""CLI entry point for Recipe Book."""

import sys
from .models import Recipe, load_recipes, save_recipes


def cmd_add(args):
    tags = []
    while "--tag" in args:
        idx = args.index("--tag")
        tags.append(args[idx + 1])
        args = args[:idx] + args[idx + 2:]
    name = " ".join(args)
    if not name:
        print("Error: recipe name required")
        sys.exit(1)
    recipes = load_recipes()
    next_id = max((r.id for r in recipes), default=0) + 1
    recipe = Recipe(id=next_id, name=name, tags=tags)
    recipes.append(recipe)
    save_recipes(recipes)
    print(f"Added recipe {recipe.id}: {recipe.name}")


def cmd_list(args):
    recipes = load_recipes()
    for r in recipes:
        tags = f"  [{', '.join(r.tags)}]" if r.tags else ""
        print(f"{r.id}: {r.name}{tags}")


def cmd_search(args):
    query = " ".join(args).lower()
    recipes = load_recipes()
    matches = [r for r in recipes if query in r.name.lower() or any(query in t.lower() for t in r.tags)]
    for r in matches:
        tags = f"  [{', '.join(r.tags)}]" if r.tags else ""
        print(f"{r.id}: {r.name}{tags}")


def cmd_show(args):
    if not args:
        print("Error: recipe ID required")
        sys.exit(1)
    recipe_id = int(args[0])
    recipes = load_recipes()
    for r in recipes:
        if r.id == recipe_id:
            print(f"# {r.name}")
            if r.tags:
                print(f"Tags: {', '.join(r.tags)}")
            if r.ingredients:
                print("\nIngredients:")
                for ing in r.ingredients:
                    print(f"  - {ing}")
            if r.instructions:
                print(f"\n{r.instructions}")
            return
    print(f"Error: recipe {recipe_id} not found")
    sys.exit(1)


COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "search": cmd_search,
    "show": cmd_show,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m recipe_book <command> [args]")
        print(f"Commands: {', '.join(COMMANDS)}")
        sys.exit(1)

    command = sys.argv[1]
    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        sys.exit(1)

    COMMANDS[command](sys.argv[2:])


main()
