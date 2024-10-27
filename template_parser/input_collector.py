from typing import Callable, Optional, Tuple
from .interfaces import IInputCollector

class InputCollector(IInputCollector):
    def collect_input(self, prompt: str, validation_func: Optional[Callable[[str], Tuple[bool, str]]] = None) -> str:
        while True:
            user_input: str = input(prompt).strip()
            if validation_func:
                valid: bool
                error_message: str
                valid, error_message = validation_func(user_input)
                if valid:
                    return user_input
                else:
                    print(error_message)
            else:
                return user_input
