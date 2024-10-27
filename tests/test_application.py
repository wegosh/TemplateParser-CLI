import pytest
from unittest.mock import MagicMock
from template_parser.application import TemplateApplication
from template_parser.constants import DATA_TYPES
from template_parser.config_manager import ProgramConfigManager
from template_parser.user_interface import UserInterface
from template_parser.file_manager import FileManager
from template_parser.config_manager import ConfigManager
from template_parser.template_processor import TemplateProcessor
from template_parser.validators import InputValidators

@pytest.fixture
def mock_user_interface():
    return MagicMock(spec=UserInterface)

@pytest.fixture
def mock_file_manager():
    return MagicMock(spec=FileManager)

@pytest.fixture
def mock_template_processor():
    return MagicMock(spec=TemplateProcessor)

@pytest.fixture
def mock_config_manager():
    return MagicMock(spec=ConfigManager)

@pytest.fixture
def mock_program_config_manager():
    manager = MagicMock(spec=ProgramConfigManager)
    manager.get_locale.return_value = 'en_GB'
    return manager

@pytest.fixture
def application(
    mock_user_interface,
    mock_file_manager,
    mock_template_processor,
    mock_config_manager,
    mock_program_config_manager,
    templates_dir='templates', 
    output_dir='output'
):
    return TemplateApplication(
        user_interface=mock_user_interface,
        file_manager=mock_file_manager,
        template_processor=mock_template_processor,
        config_manager=mock_config_manager,
        program_config_manager=mock_program_config_manager,
        templates_dir=templates_dir,
        output_dir=output_dir
    )

class TestCurrencyConversion:
    def test_convert_type_currency_standard(self, application):
        value = "1000000"
        typ = DATA_TYPES['CURRENCY']
        options = {'format': 'standard', 'currency_code': 'USD'}
        result = application.convert_type(value, typ, options)
        assert result == "US$1,000,000.00"

    def test_convert_type_currency_format_not_provided(self, application):
        value = "1000000"
        typ = DATA_TYPES['CURRENCY']
        options = {'currency_code': 'USD'}
        result = application.convert_type(value, typ, options)
        assert result == "US$1,000,000.00"

    def test_convert_type_currency_long(self, application, mock_program_config_manager):
        value = "1000000"
        typ = DATA_TYPES['CURRENCY']
        options = {'format': 'long'}
        mock_program_config_manager.get_locale.return_value = 'en'
        result = application.convert_type(value, typ, options)
        assert result == "one million euro, zero cents"

    def test_convert_type_currency_short(self, application):
        value = "1500000"
        typ = DATA_TYPES['CURRENCY']
        options = {'format': 'short', 'currency_code': 'USD'}
        result = application.convert_type(value, typ, options)
        assert result == "US$1,500,000.00"

    def test_convert_type_currency_no_symbol(self, application):
        value = "2500"
        typ = DATA_TYPES['CURRENCY']
        options = {'format': 'standard', 'currency_code': 'USD', 'symbol': 'false'}
        result = application.convert_type(value, typ, options)
        assert result == "2,500.00"

    def test_convert_type_currency_invalid_number(self, application):
        value = "invalid"
        typ = DATA_TYPES['CURRENCY']
        options = {'format': 'standard', 'currency_code': 'USD'}
        with pytest.raises(ValueError):
            application.convert_type(value, typ, options)

    def test_convert_type_currency_invalid_currency_code(self, application):
        value = "1000"
        typ = DATA_TYPES['CURRENCY']
        options = {'format': 'standard', 'currency_code': 'XYZ'}
        result = application.convert_type(value, typ, options)
        assert "XYZ" in result

    def test_convert_type_currency_different_locale(self, application, mock_program_config_manager):
        value = "1000"
        typ = DATA_TYPES['CURRENCY']
        options = {'format': 'standard', 'currency_code': 'EUR'}
        mock_program_config_manager.get_locale.return_value = 'de_DE'
        result = application.convert_type(value, typ, options)
        assert result == "1.000,00\u00A0€"  # German format for EUR

    def test_convert_type_currency_include_symbol(self, application):
        value = "500"
        typ = DATA_TYPES['CURRENCY']
        options = {'format': 'standard', 'currency_code': 'GBP', 'symbol': 'true'}
        result = application.convert_type(value, typ, options)
        assert result == "£500.00"

class TestCollectUserInputs:
    def test_collect_user_inputs(self, application, mock_program_config_manager):
        placeholder_set = {
            'name': {'type': 'str'},
            'age': {'type': 'int'},
            'country': {'type': 'str'}
        }

        mock_program_config_manager.get_required_variables.return_value = [
            {'name': 'name', 'type': 'str'},
            {'name': 'age', 'type': 'int'}
        ]

        application.prompt_for_input = MagicMock(side_effect=['Alice', '30', 'Wonderland'])

        user_inputs = application.collect_user_inputs(placeholder_set)

        assert user_inputs == {
            'name': 'Alice',
            'age': '30',
            'country': 'Wonderland'
        }
        assert application.prompt_for_input.call_count == 3
        application.prompt_for_input.assert_any_call('name', 'str', required=True)
        application.prompt_for_input.assert_any_call('age', 'int', required=True)
        application.prompt_for_input.assert_any_call('country', 'str', {})

class TestPromptForInput:
    def test_prompt_for_input_string(self, application):
        application.user_interface.get_input = MagicMock(return_value='Test String')
        result = application.prompt_for_input('test_key', DATA_TYPES['STRING'])
        assert result == 'Test String'
        application.user_interface.get_input.assert_called_once()

    def test_prompt_for_input_int(self, application):
        application.user_interface.get_input = MagicMock(return_value='42')
        result = application.prompt_for_input('test_int', DATA_TYPES['INTEGER'])
        assert result == '42'  # Raw input is returned
        application.user_interface.get_input.assert_called_once()

    def test_prompt_for_input_date(self, application):
        application.user_interface.get_input = MagicMock(return_value='01-01-2024')
        result = application.prompt_for_input('test_date', DATA_TYPES['DATE'])
        assert result == '01-01-2024'
        application.user_interface.get_input.assert_called_once()

    def test_prompt_for_input_currency(self, application):
        application.user_interface.get_input = MagicMock(return_value='1000')
        result = application.prompt_for_input('price', DATA_TYPES['CURRENCY'])
        assert result == '1000'
        application.user_interface.get_input.assert_called_once()

    def test_prompt_for_input_required(self, application):
        application.user_interface.get_input = MagicMock(return_value='Required Value')
        result = application.prompt_for_input('required_field', DATA_TYPES['STRING'], required=True)
        assert result == 'Required Value'
        application.user_interface.get_input.assert_called_once()

class TestSelectTemplate:
    def test_select_template_valid_choice(self, application):
        templates = ['template1.json', 'template2.json', 'template3.json']
        application.user_interface.get_input = MagicMock(return_value='2')
        selected_template = application.select_template(templates)
        assert selected_template == 'template2.json'
        application.user_interface.get_input.assert_called_once()

    def test_select_template_invalid_choice_then_valid(self, application):
        templates = ['template1.json', 'template2.json', 'template3.json']
        application.user_interface.get_input = MagicMock(side_effect=['5', '1'])
        selected_template = application.select_template(templates)
        assert selected_template == 'template1.json'
        assert application.user_interface.get_input.call_count == 2

    def test_select_template_non_numeric_input(self, application):
        templates = ['template1.json', 'template2.json', 'template3.json']
        application.user_interface.get_input = MagicMock(side_effect=['abc', '2'])
        selected_template = application.select_template(templates)
        assert selected_template == 'template2.json'
        assert application.user_interface.get_input.call_count == 2

class TestGenerateOutputFilename:
    def test_generate_output_filename_success(self, application, mock_program_config_manager):
        mock_program_config_manager.get_output_filename_format.return_value = '{productID}_{date}.json'
        user_inputs = {'productID': 'ABC123'}
        output_filename = application.generate_output_filename(user_inputs)
        assert output_filename.endswith('_{}.json'.format(application.get_context_variables()['date']))
        assert output_filename == 'ABC123_{}.json'.format(application.get_context_variables()['date'])

    def test_generate_output_filename_missing_variable(self, application, mock_program_config_manager):
        mock_program_config_manager.get_output_filename_format.return_value = '{productID}_{userID}.json'
        user_inputs = {'productID': 'ABC123'}
        application.user_interface.display_warning = MagicMock()
        output_filename = application.generate_output_filename(user_inputs)
        # Check that a fallback filename is used
        assert output_filename.startswith('output_')
        assert output_filename.endswith('.json')
        # Check that a warning was displayed
        application.user_interface.display_warning.assert_called_once_with(
            "Missing variable 'userID' required for output filename generation."
        )

    # def test_generate_output_filename_error(self, application, mock_program_config_manager):
    #     mock_program_config_manager.get_output_filename_format.return_value = '{productID}_{date}.json'
    #     user_inputs = {'productID': 'ABC123'}
    #     application.get_context_variables = MagicMock(side_effect=Exception('Context error'))
    #     application.user_interface.display_error = MagicMock()
    #     with pytest.raises(SystemExit):
    #         application.generate_output_filename(user_inputs)
    #     application.user_interface.display_error.assert_called_once_with(
    #         "Error generating output filename: Context error"
    #     )

class TestReplacePlaceholders:
    def test_replace_placeholders_success(self, application):
        template_text = '{"message": "Hello, <name>!"}'
        user_inputs = {'name': 'Alice'}
        result = application.replace_placeholders(template_text, user_inputs)
        expected = '{"message": "Hello, Alice!"}'
        assert result == expected

    def test_replace_placeholders_with_options(self, application):
        template_text = '{"discount": "<discount:int>"}'
        user_inputs = {'discount': 10}
        result = application.replace_placeholders(template_text, user_inputs)
        try:
            result = application.replace_placeholders(template_text, user_inputs)
        except Exception as e:
            print("REXC: ", e)
        expected = {"discount": 10}
        print(f"REXP: {expected}\nACT: {result}")
        # assert result == expected

    def test_replace_placeholders_missing_value(self, application):
        template_text = '{"message": "Hello, <name>!"}'
        user_inputs = {}
        application.user_interface.display_warning = MagicMock()
        result = application.replace_placeholders(template_text, user_inputs)
        assert result == template_text
        application.user_interface.display_warning.assert_called_once_with(
            "Value for 'name' not provided. Leaving placeholder unchanged."
        )

    def test_replace_placeholders_error_in_conversion(self, application):
        template_text = '{"age": "<age:int>"}'
        user_inputs = {'age': 'twenty'}
        application.user_interface.display_error = MagicMock()
        result = application.replace_placeholders(template_text, user_inputs)
        assert result == '{"age": "<age:int>"}'
        application.user_interface.display_error.assert_called_once()

class TestWarnUnusedRequiredVariables:
    # def test_warn_unused_required_variables_no_warning(self, application, mock_program_config_manager):
    #     placeholder_set = {'productID': {}, 'userID': {}}
    #     mock_program_config_manager.get_required_variables.return_value = [
    #         {'name': 'productID'},
    #         {'name': 'userID'}
    #     ]
    #     application.user_interface.display_warning = MagicMock()
    #     application.warn_unused_required_variables(placeholder_set)
    #     application.user_interface.display_warning.assert_not_called()

    def test_warn_unused_required_variables_with_warning(self, application, mock_program_config_manager):
        placeholder_set = {'productID': {}}
        mock_program_config_manager.get_required_variables.return_value = [
            {'name': 'productID'},
            {'name': 'userID'}
        ]
        mock_program_config_manager.get_output_filename_format.return_value = '{productID}.json'
        application.user_interface.display_warning = MagicMock()
        application.warn_unused_required_variables(placeholder_set)
        application.user_interface.display_warning.assert_called_once_with(
            "Required variable 'userID' is not used in the template or output filename format."
        )


class TestGetValidator:
    def test_get_validator_known_type(self, application):
        validator = application.get_validator(DATA_TYPES['INTEGER'])
        assert validator == InputValidators.validate_int

    def test_get_validator_unknown_type(self, application):
        validator = application.get_validator('unknown_type')
        assert validator == InputValidators.validate_non_empty

