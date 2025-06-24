import os
from pathlib import Path

MODELS_DIR = Path("app/models")
REPO_DIR = Path("app/v1/repositories")
BASE_REPO_IMPORT = "from app.v1.repositories.base_repository import BaseRepository"
SQLALCHEMY_IMPORT = "from sqlalchemy.ext.asyncio import AsyncSession"

REPO_TEMPLATE = '''{sqlalchemy_import}
from app.models.{model_module} import {model_class}
{base_repo_import}


class {repo_class}(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, {model_class})
'''

def snake_to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))

def main():
    REPO_DIR.mkdir(parents=True, exist_ok=True)

    for file in MODELS_DIR.glob("*.py"):
        if file.name in {"__init__.py"}:
            continue

        model_module = file.stem  # e.g. "user_wallet"
        model_class = snake_to_pascal(model_module)
        repo_class = f"{model_class}Repository"
        repo_filename = f"{model_module}_repository.py"
        repo_path = REPO_DIR / repo_filename

        if repo_path.exists():
            print(f"Skipped (already exists): {repo_path}")
            continue

        content = REPO_TEMPLATE.format(
            sqlalchemy_import=SQLALCHEMY_IMPORT,
            base_repo_import=BASE_REPO_IMPORT,
            model_module=model_module,
            model_class=model_class,
            repo_class=repo_class,
        )

        repo_path.write_text(content)
        print(f"Generated: {repo_path}")

if __name__ == "__main__":
    main()
