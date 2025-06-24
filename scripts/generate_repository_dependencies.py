from pathlib import Path

REPO_DIR = Path("app/v1/repositories")
DEPENDENCY_DIR = Path("app/v1/dependencies/repositories")

template = '''from app.v1.repositories.{module} import {class_name}
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_{func_name}(
    session: AsyncSession = Depends(get_async_session),
) -> {class_name}:
    return {class_name}(session)
'''

def snake_to_camel(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_")) + "Repository"

def main():
    DEPENDENCY_DIR.mkdir(parents=True, exist_ok=True)

    for file in REPO_DIR.glob("*_repository.py"):
        module_name = file.stem
        if module_name == "base_repository":
            continue

        dependency_file = DEPENDENCY_DIR / f"{module_name}.py"
        if dependency_file.exists():
            print(f"Skipped (already exists): {dependency_file}")
            continue

        class_name = snake_to_camel(module_name.replace("_repository", ""))
        func_name = module_name

        content = template.format(
            module=module_name,
            class_name=class_name,
            func_name=func_name
        )

        dependency_file.write_text(content)
        print(f"Generated: {dependency_file}")

if __name__ == "__main__":
    main()
