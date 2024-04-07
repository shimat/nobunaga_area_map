from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class conditional_decorator:
    def __init__(
        self,
        decorator: Callable[[F], F],
        condition: bool,
    ) -> None:
        self.decorator = decorator
        self.condition = condition

    def __call__(self, func: F) -> F:
        if self.condition:
            return self.decorator(func)  # type: ignore
        return func
