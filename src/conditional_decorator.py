from collections.abc import Callable
from typing import Any


class conditional_decorator:
    def __init__(self, decorator: Callable[[Callable[..., Any]], Callable[..., Any]], condition: bool) -> None:
        self.decorator = decorator
        self.condition = condition

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        if self.condition:
            return self.decorator(func)
        return func
