import logging
from typing import Optional, Callable
from .interfaces import IInputCollector

class UserInterface:
    def __init__(self, input_collector: IInputCollector):
        self.input_collector = input_collector

    def display_message(self, message: str) -> None:
        print(message)
        logging.info(message)

    def display_warning(self, message: str) -> None:
        logging.warning(message)

    def display_error(self, message: str) -> None:
        logging.error(message)

    def get_input(self, prompt: str, validation_func: Optional[Callable[[str], tuple[bool, str]]] = None) -> str:
        return self.input_collector.collect_input(prompt, validation_func=validation_func)
