from http import HTTPStatus
import re


def status_code_to_snake_case(code: int) -> str:
    phrase = HTTPStatus(code).phrase
    snake = re.sub(r"\W+", "_", phrase).lower()
    return snake.strip("_")
