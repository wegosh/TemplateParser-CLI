from typing import Dict
from .interfaces import ITemplateProcessor
from .constants import PLACEHOLDER_PATTERN


class TemplateProcessor(ITemplateProcessor):
    def __init__(self, placeholder_pattern: str = r'(?P<quote>"?)<(?P<name>[^<>:]+)(?::(?P<type>[^<>:]+))?>\1'):
        self.placeholder_pattern = placeholder_pattern

    def extract_placeholders(self, template_text):
        placeholders = {}
        for match in PLACEHOLDER_PATTERN.finditer(template_text):
            name = match.group('name')
            typ = match.group('type') or 'str'
            options_str = match.group('options')
            options = {}
            if options_str:
                for opt in options_str.lstrip('|').split('|'):
                    if '=' in opt:
                        key, value = opt.split('=', 1)
                        options[key.strip()] = value.strip()
                    else:
                        options[opt.strip()] = True
            placeholders[name] = {'type': typ, 'options': options}
        return placeholders

    # def replace_placeholders(self, template_text, user_inputs):
    #     def placeholder_replacer(match):
    #         name = match.group('name')
    #         typ = match.group('type') or 'str'
    #         options_str = match.group('options')
    #         options = {}
    #         if options_str:
    #             for opt in options_str.lstrip('|').split('|'):
    #                 if '=' in opt:
    #                     key, value = opt.split('=', 1)
    #                     options[key.strip()] = value.strip()
    #                 else:
    #                     options[opt.strip()] = True
    #         base_value = user_inputs.get(name)
    #         if base_value is None:
    #             return match.group(0)
    #         converted_value = self.convert_type(base_value, typ, options)
    #         return converted_value
    #     result = PLACEHOLDER_PATTERN.sub(placeholder_replacer, template_text)
    #     return result

