from collections.abc import Callable


class conditional_decorator:
    def __init__(self, decorator: Callable[[Callable], Callable], condition: bool) -> None:
        self.decorator = decorator
        self.condition = condition

    def __call__(self, func: Callable) -> Callable:
        if self.condition:
            return self.decorator(func)
        return func
