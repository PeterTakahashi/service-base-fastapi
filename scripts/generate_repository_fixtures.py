from pathlib import Path

REPO_DIR = Path("app/v1/repositories")
FIXTURE_DIR = Path("tests/fixtures/repositories")
INIT_FILE = FIXTURE_DIR / "__init__.py"

fixture_template = '''import pytest_asyncio
from app.v1.repositories.{repo_module} import {repo_class}


@pytest_asyncio.fixture
async def {fixture_name}(async_session):
    return {repo_class}(async_session)
'''

def snake_to_pascal(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_")) + "Repository"

def main():
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    init_lines = []

    for file in REPO_DIR.glob("*_repository.py"):
        if file.stem == "base_repository":
            continue

        module = file.stem  # e.g. "user_repository"
        class_name = snake_to_pascal(module.replace("_repository", ""))
        fixture_name = module  # same as function name and file name
        fixture_path = FIXTURE_DIR / f"{module}_fixture.py"

        if fixture_path.exists():
            print(f"Skipped (exists): {fixture_path}")
        else:
            content = fixture_template.format(
                repo_module=module,
                repo_class=class_name,
                fixture_name=fixture_name,
            )
            fixture_path.write_text(content)
            print(f"Generated: {fixture_path}")

        init_lines.append(f"from .{module}_fixture import {fixture_name}")

    # __init__.py の __all__ も更新
    init_lines.append("")
    init_lines.append("__all__ = [")
    for file in REPO_DIR.glob("*_repository.py"):
        if file.stem == "base_repository":
            continue
        init_lines.append(f'    "{file.stem}",')
    init_lines.append("]")

    INIT_FILE.write_text("\n".join(init_lines))
    print(f"Updated: {INIT_FILE}")

if __name__ == "__main__":
    main()
