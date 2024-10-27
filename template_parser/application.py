from datetime import datetime
from typing import Optional, Dict, Any, List, Callable, Tuple
from .interfaces import IFileManager, IConfigManager, ITemplateProcessor
from .validators import InputValidators
from .config_manager import ProgramConfigManager
from .helpers.wrappers import handle_file_exceptions
from .helpers.date_utils import apply_date_operations
from .constants import DATA_TYPES, PLACEHOLDER_PATTERN
from .user_interface import UserInterface
from babel.numbers import format_currency, get_currency_symbol
from num2words import num2words
import sys
import os
import json
import uuid
import logging

class TemplateApplication:
    def __init__(self,
                 file_manager: IFileManager,
                 config_manager: IConfigManager,
                 template_processor: ITemplateProcessor,
                 templates_dir: str,
                 output_dir: str,
                 program_config_manager: ProgramConfigManager,
                 user_interface: UserInterface):
        self.file_manager = file_manager
        self.config_manager = config_manager
        self.template_processor = template_processor
        self.templates_dir = templates_dir
        self.output_dir = output_dir
        self.program_config_manager = program_config_manager
        self.user_interface = user_interface

    @handle_file_exceptions
    def run(self, template_path: Optional[str] = None) -> None:
        if template_path:
            json_file_path = template_path
            if not os.path.isfile(json_file_path):
                msg = f"The template file '{json_file_path}' does not exist."
                self.user_interface.display_error(msg)
                raise FileNotFoundError(msg)
        else:
            if not os.path.isdir(self.templates_dir):
                msg = f"Templates directory '{self.templates_dir}' does not exist."
                self.user_interface.display_error(msg)
                print("Please create the directory and add template files before running the program.")
                raise FileNotFoundError(msg)
                
            templates = self.file_manager.list_directory(self.templates_dir, '.json')

            if not templates:
                msg = f"No JSON template files found in '{self.templates_dir}'."
                self.user_interface.display_warning(msg)
                print("Please add template files to the directory before running the program.")
                raise FileNotFoundError(msg)

            selected_template = self.select_template(templates)
            json_file_path = os.path.join(self.templates_dir, selected_template)

        template_text = self.file_manager.read_file(json_file_path)
        placeholder_set = self.template_processor.extract_placeholders(template_text)
        user_inputs = self.collect_user_inputs(placeholder_set)
        self.warn_unused_required_variables(placeholder_set)
        new_template_text = self.replace_placeholders(template_text, user_inputs)

        try:
            parsed_json = json.loads(new_template_text)
        except json.JSONDecodeError as e:
            self.user_interface.display_error(f"The modified JSON is invalid: {e}")
            sys.exit(1)

        output_filename = self.generate_output_filename(user_inputs)
        self.file_manager.ensure_directory(self.output_dir)
        output_path = os.path.join(self.output_dir, output_filename)
        try:
            self.file_manager.write_file(output_path, json.dumps(parsed_json, indent=2))
            self.user_interface.display_message(f"Modified JSON saved to {output_path}")
        except Exception as e:
            self.user_interface.display_error(f"Error writing to file {output_path}: {e}")

        self.config_manager.load_config()
        self.config_manager.save_config({
            "output_filename": output_filename,
            "details": user_inputs.copy()
        })

    def collect_user_inputs(self, placeholder_set):
        user_inputs = {}

        required_variables = self.program_config_manager.get_required_variables()

        for var in required_variables:
            key = var['name']
            typ = var.get('type', 'str')
            user_inputs[key] = self.prompt_for_input(key, typ, required=True)

        for name, placeholder_info in placeholder_set.items():
            if name in user_inputs:
                continue
            typ = placeholder_info.get('type', 'str')
            options = placeholder_info.get('options', {})
            user_inputs[name] = self.prompt_for_input(name, typ, options)
        return user_inputs

    def prompt_for_input(self, key, typ, options=None, required=False):
        options = options or {}
        example = ''

        if typ == DATA_TYPES['DATE']:
            example_with_time = datetime.now().strftime('%d-%m-%Y %H:%M')
            example_without_time = datetime.now().strftime('%d-%m-%Y')
            prompt = (
                f"Enter value for '{key}' (type: {typ} | examples: {example_without_time} or {example_with_time})"
            )
        elif typ == DATA_TYPES['CURRENCY']:
            prompt = f"Enter value for '{key}' (type: {typ} | example: 1000000)"
        else:
            prompt = f"Enter value for '{key}' (type: {typ})"

        if required:
            prompt += " (required): "
        else:
            prompt += ": "
            
        value = self.user_interface.get_input(prompt=prompt, validation_func=self.get_validator(typ))
        return value 

    def warn_unused_required_variables(self, placeholder_set: Dict[str, str]) -> None:
        used_variables = set(placeholder_set.keys())
        format_string = self.program_config_manager.get_output_filename_format()
        format_variables = set(PLACEHOLDER_PATTERN.findall(format_string))
        used_variables.update(format_variables)

        for var in self.program_config_manager.get_required_variables():
            var_name = var['name']
            if var_name not in used_variables:
                self.user_interface.display_warning(f"Required variable '{var_name}' is not used in the template or output filename format.")

    def select_template(self, templates: List[str]) -> str:
        print("Available templates:")
        for idx, template_name in enumerate(templates, start=1):
            print(f"{idx}. {template_name}")
        while True:
            choice = self.user_interface.get_input(
                "Select a template by entering the corresponding number: ",
                validation_func=lambda x: (
                    x.isdigit() and 1 <= int(x) <= len(templates),
                    "Invalid selection. Please enter a valid number."
                )
            )
            print("Wali sie")
            if choice.isdigit() and 1 <= int(choice) <= len(templates):
                return templates[int(choice) - 1]
            else:
                self.user_interface.display_error("Invalid selection. Please enter a valid number.")


    def get_validator(self, typ: str) -> Callable[[str], Tuple[bool, Optional[str]]]:
        validators = {
            DATA_TYPES['INTEGER']: InputValidators.validate_int,
            DATA_TYPES['FLOAT']: InputValidators.validate_float,
            DATA_TYPES['URL']: InputValidators.validate_url,
            DATA_TYPES['STRING']: InputValidators.validate_non_empty,
            DATA_TYPES['DATE']: InputValidators.validate_date,
            DATA_TYPES['CURRENCY']: InputValidators.validate_currency,
        }
        return validators.get(typ, InputValidators.validate_non_empty)

    def convert_type(self, value: str, typ: str, options: Optional[Dict[str, Any]] = None) -> Any:
        options = options or {}
        if typ == DATA_TYPES['INTEGER']:
            return int(value)
        elif typ == DATA_TYPES['FLOAT']:
            return float(value)
        elif typ == DATA_TYPES['DATE']:
            input_formats = ['%d-%m-%Y %H:%M', '%d-%m-%Y']
            date_obj = None
            for input_format in input_formats:
                try:
                    date_obj = datetime.strptime(value.strip(), input_format)
                    break 
                except ValueError:
                    continue
            if date_obj is None:
                self.user_interface.display_error(
                    f"Invalid date input: '{value}'. Expected formats: DD-MM-YYYY or DD-MM-YYYY HH:MM"
                )
                raise ValueError(f"Invalid date input: '{value}'")

            date_operations = {
                k: v for k, v in options.items() if k.startswith('add_') or k.startswith('subtract_')
            }

            if date_operations:
                date_obj = apply_date_operations(date_obj, date_operations)

            output_format = options.get('format', '%Y-%m-%dT%H:%M:%S')
            return date_obj.strftime(output_format)
        elif typ == DATA_TYPES['CURRENCY']:
            number = float(value)
            locale = self.program_config_manager.get_locale()
            format_style = options.get('format', 'standard')
            include_symbol = options.get('symbol', 'true').lower() == 'true'
            currency_code = options.get('currency_code', 'USD')

            if format_style == 'long':
                amount_in_words = num2words(number, to='currency', lang=locale)
                return amount_in_words
            elif format_style == 'short':
                formatted_currency = format_currency(
                    number, currency_code, locale=locale, format='¤#,##0.00', currency_digits=True
                )
                return formatted_currency
            else:
                formatted_currency = format_currency(
                    number, currency_code, locale=locale, currency_digits=True
                )
                if not include_symbol:
                    formatted_currency = formatted_currency.replace(get_currency_symbol(currency_code, locale), '').strip()
                return formatted_currency
        else:
            return value

    def get_context_variables(self) -> Dict[str, str]:
        return {
            'date': datetime.now().strftime('%Y%m%d'),
            'time': datetime.now().strftime('%H%M%S')
        }

    def generate_output_filename(self, user_inputs: Dict[str, Any]) -> str:
        format_string = self.program_config_manager.get_output_filename_format()
        context = self.get_context_variables()
        all_inputs = {**user_inputs, **context}
        try:
            output_filename = format_string.format(**all_inputs)
        except KeyError as e:
            missing_key = e.args[0]
            self.user_interface.display_warning(f"Missing variable '{missing_key}' required for output filename generation.")
            unique_id = uuid.uuid4().hex[:8]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"output_{timestamp}_{unique_id}.json"
            self.user_interface.display_message(f"Using fallback output filename: {output_filename}")
        except Exception as e:
            self.user_interface.display_error(f"Error generating output filename: {e}")
            sys.exit(1)
        return output_filename

    def replace_placeholders(self, template_text, user_inputs):
        try:
            template_data = json.loads(template_text)
        except json.JSONDecodeError as e:
            self.user_interface.display_error(f"Invalid JSON template: {e}")
            raise

        def replace_in_data(data):
            if isinstance(data, dict):
                return {key: replace_in_data(value) for key, value in data.items()}
            elif isinstance(data, list):
                return [replace_in_data(item) for item in data]
            elif isinstance(data, str):
                match_full = PLACEHOLDER_PATTERN.fullmatch(data.strip())
                if match_full:
                    name = match_full.group('name')
                    typ = match_full.group('type') or 'str'
                    options_str = match_full.group('options')
                    options = {}
                    if options_str:
                        for opt in options_str.lstrip('|').split('|'):
                            if '=' in opt:
                                key, value = opt.split('=', 1)
                                options[key.strip()] = value.strip()
                            else:
                                options[opt.strip()] = True
                    base_value = user_inputs.get(name)
                    if base_value is None:
                        self.user_interface.display_warning(f"Value for '{name}' not provided. Leaving placeholder unchanged.")
                        return data
                    try:
                        converted_value = self.convert_type(base_value, typ, options)
                        return converted_value 
                    except Exception as e:
                        self.user_interface.display_error(f"Error processing placeholder '{data}': {e}")
                        return data 
                else:
                    def placeholder_replacer(match):
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
                        base_value = user_inputs.get(name)
                        if base_value is None:
                            self.user_interface.display_warning(f"Value for '{name}' not provided. Leaving placeholder unchanged.")
                            return match.group(0)
                        try:
                            converted_value = self.convert_type(base_value, typ, options)
                            return str(converted_value)
                        except Exception as e:
                            self.user_interface.display_error(f"Error processing placeholder '{match.group(0)}': {e}")
                            return match.group(0)

                    return PLACEHOLDER_PATTERN.sub(placeholder_replacer, data)
            else:
                return data

        replaced_data = replace_in_data(template_data)
        result = json.dumps(replaced_data)
        return result
