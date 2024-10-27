# JSON Template Parser

A command-line interface (CLI) tool for parsing JSON templates and replacing placeholders with user-provided values. This tool simplifies the process of generating customized JSON files based on templates, making it ideal for configuration management, testing, and other automation tasks.

## Features

- **Template Parsing:** Parses JSON templates with placeholders and replaces them with user inputs.
- **Supports Data Types and Options:** Handles different data types like strings, integers, floats, dates, currencies, and URLs with validation and formatting options.
- **Date and Currency Formatting:** Supports date arithmetic and formatting, currency formatting in different locales and styles.
- **Configuration Management:** Stores user inputs and output filenames in a `config.json` file for tracking.
- **Error Handling:** Provides clear and user-friendly error messages.
- **Command-Line Interface:** Easy to use from the terminal with optional arguments for flexibility.

## Installation

To install the `template_parser` CLI tool, follow these steps:

1. **Clone the repository**

    ```bash
    git clone https://github.com/wegosh/TemplateParser-CLI
    ```

2. **Navigate to the project directory**

    ```bash
    cd TemplateParser-CLI
    ```

3. **Install the Package**

    You can install the package locally using pip:

    ```bash
    pip install .
    ```

    **Note:** You might need to use `pip3` instead of `pip` depending on your Python installation.

## Usage

After installation, you can use the `template-parser` command from any directory.

### Basic usage

```bash
template-parser
```

**Note:** If you run the command without any arguments, the program expects to find a `files/templates/` directory in your current working directory containing JSON template files.

### Using a specific template

```bash
template-parser path/to/template.json
```

**Note:** You can specify the path to a JSON template file directly.

### Optional Arguments

The CLI tool supports optional arguments for specifying directories:

```bash
template-parser [template] [--templates-dir TEMPLATES_DIR] [--output-dir OUTPUT_DIR] [--config-path CONFIG_PATH]
```

#### Arguments:

- `template`: Path to the template JSON file.
- `--templates-dir`: Path to the directory containing templates.
- `--output-dir`: Path to the directory where output files will be saved.
- `--config-path`: Path to the `config.json` file.

## Examples

### Example 1: Using templates directory

1. **Create the `files/templates` directory**

    In your current working directory, create the necessary directories:

    ```bash
    mkdir -p files/templates
    ```

2. **Add template files**

    Place your JSON template files in the `files/templates/` directory.

    **Example templates:**

    - `files/templates/CombinedSample.json`
    - `files/templates/CurrencyAlone.json`
    - `files/templates/DateAlone.json`
    - `files/templates/NumbersAlone.json`

3. **Run the CLI tool**

    ```bash
    template-parser
    ```

4. **Follow the prompts**

    The program will list available templates and prompt you to select one:

    ```bash
    Available templates:
    1. CombinedSample.json
    2. CurrencyAlone.json
    3. DateAlone.json
    4. NumbersAlone.json
    Select a template by entering the corresponding number: 1
    ```

    Then, it will prompt you to enter values for each placeholder:

    ```bash
    Enter value for 'TemplateName' (type: str) (required): SampleOutput
    Enter value for 'number' (type: float): 123.45
    Enter value for 'eventDate' (type: date): 25-12-2023
    Enter value for 'date_input' (type: date): 01-01-2024
    Enter value for 'price' (type: currency): 99.99
    ```

5. **Check the output**

    The generated JSON file will be saved in `files/output/`:

    `files/output/SampleOutput.json`

    ```json
    {
      "numbers": {
        "float": 123.45,
        "int": 123
      },
      "date": {
        "format1": "2023-12 25",
        "format2": "25/12/23",
        "format3": "25 December 2023",
        "futureDate": "The next event takes place on: 25/12/24",
        "original_date": "2024-01-01",
        "one_year_later": "2025-01-01",
        "two_months_earlier": "2023-11-01",
        "next_week": "2024-01-08"
      },
      "currency": {
        "product_price": "ninety-nine pounds and ninety-nine pence",
        "discounted_price": "99.99",
        "price_in_euros": "€99.99",
        "price_in_dollars": "$99.99",
        "short_price": "£99.99",
        "not_formatted_price": "GBP99.99"
      }
    }
    ```

6. **Configuration file**

    The user inputs and output filename are stored in `files/config.json`:

    ```json
    [
      {
        "output_filename": "SampleOutput.json",
        "details": {
          "TemplateName": "SampleOutput",
          "number": "123.45",
          "eventDate": "25-12-2023",
          "date_input": "01-01-2024",
          "price": "99.99"
        }
      }
    ]
    ```

### Example 2: Specifying template path

If you prefer to specify the template file directly:

```bash
template-parser files/templates/CurrencyAlone.json
```

**Note:** The program will use the specified template and prompt for inputs as usual.

#### Notes

- **Current Working Directory:** The program uses the current working directory for templates, outputs, and config files unless specified otherwise.
- **Directories:** If the necessary directories (`files/templates/`, `files/output/`, etc.) do not exist, the program will inform you and may create them when possible.
- **Data Types:** The program supports the following data types for placeholders:
  - `str` (default)
  - `int`
  - `float`
  - `date`
  - `currency`
  - `url`

- **Options and Formatting:**

  - **Date Placeholders:** Support date arithmetic operations like `add_years`, `subtract_months`, `add_days`, and formatting with `format`.
  - **Currency Placeholders:** Support formatting options like `format=long`, `format=short`, `symbol=false`, `currency_code`.

## Directory Structure

Here's an example of how your project directory might look:

```bash
your_project/
├── files/
│   ├── templates/
│   │   ├── CombinedSample.json
│   │   ├── CurrencyAlone.json
│   │   ├── DateAlone.json
│   │   ├── NumbersAlone.json
│   ├── output/
│   │   ├── SampleOutput.json
│   ├── config.json
│   ├── program_config.json
```

- **files/templates/:** Contains your JSON template files.
- **files/output/:** Where the generated JSON files are saved.
- **files/config.json:** Stores user inputs and output filenames.
- **files/program_config.json:** Configuration for the application.

## Creating Templates

Templates are JSON files that contain placeholders in the following format:

- `<placeholderName>`: For string values.
- `<placeholderName:type>`: For values with a specific type.
- `<placeholderName:type|option1|option2=value2>`: For values with specific type and options.

### Supported Types

- **str:** String (default if no type is specified).
- **int:** Integer.
- **float:** Floating-point number.
- **date:** Date values with formatting and arithmetic options.
- **currency:** Currency values with formatting options.
- **url:** Validates that the input is a valid URL.

### Example Templates

#### CombinedSample.json

```json
{
  "numbers": {
    "float": "<number:float>",
    "int": "<number:int>"
  },
  "date": {
    "format1": "<eventDate:date|format=%Y-%m %d>",
    "format2": "<eventDate:date|format=%d/%m/%y>",
    "format3": "<eventDate:date|format=%d %B %Y>",
    "futureDate": "The next event takes place on: <eventDate:date|format=%d/%m/%y|add_years=1>",
    "original_date": "<date_input:date|format=%Y-%m-%d>",
    "one_year_later": "<date_input:date|format=%Y-%m-%d|add_years=1>",
    "two_months_earlier": "<date_input:date|format=%Y-%m-%d|subtract_months=2>",
    "next_week": "<date_input:date|format=%Y-%m-%d|add_days=7>"
  },
  "currency": {
    "product_price": "<price:currency|format=long|currency_code=GBP>",
    "discounted_price": "<price:currency|format=standard|currency_code=GBP|symbol=false>",
    "price_in_euros": "<price:currency|format=standard|currency_code=EUR>",
    "price_in_dollars": "<price:currency|format=standard|currency_code=USD>",
    "short_price": "<price:currency|format=short|currency_code=GBP>",
    "not_formatted_price": "<price:currency|currency_code=GBP>"
  }
}
```

#### CurrencyAlone.json

```json
{
  "product_price": "<price:currency|format=long|currency_code=GBP>",
  "discounted_price": "<price:currency|format=standard|currency_code=GBP|symbol=false>",
  "price_in_euros": "<price:currency|format=standard|currency_code=EUR>",
  "price_in_dollars": "<price:currency|format=standard|currency_code=USD>",
  "short_price": "<price:currency|format=short|currency_code=GBP>",
  "not_formatted_price": "<price:currency|currency_code=GBP>"
}
```

#### DateAlone.json

```json
{
  "format1": "<eventDate:date|format=%Y-%m %d>",
  "format2": "<eventDate:date|format=%d/%m/%y>",
  "format3": "<eventDate:date|format=%d %B %Y>",
  "futureDate": "The next event takes place on: <eventDate:date|format=%d/%m/%y|add_years=1>",
  "original_date": "<date_input:date|format=%Y-%m-%d>",
  "one_year_later": "<date_input:date|format=%Y-%m-%d|add_years=1>",
  "two_months_earlier": "<date_input:date|format=%Y-%m-%d|subtract_months=2>",
  "next_week": "<date_input:date|format=%Y-%m-%d|add_days=7>"
}
```

#### NumbersAlone.json

```json
{
  "float": "<number:float>",
  "int": "<number:int>"
}
```

### Placeholder Options

- **Date Options:**
  - `format`: Specifies the output format of the date using strftime directives.
  - `add_years`: Adds the specified number of years to the date.
  - `subtract_months`: Subtracts the specified number of months from the date.
  - `add_days`: Adds the specified number of days to the date.

- **Currency Options:**
  - `format`: Specifies the format style (`long`, `short`, `standard`).
  - `currency_code`: Specifies the currency code (e.g., `USD`, `GBP`, `EUR`).
  - `symbol`: Specifies whether to include the currency symbol (`true` or `false`).

## Configuration

The application uses a `program_config.json` file to specify required variables and output filename format.

### Example `program_config.json`

```json
{
  "required_variables": [
    {"name": "TemplateName", "type": "str"}
  ],
  "output_filename_format": "{TemplateName}.json",
  "locale": "en_GB"
}
```

- **required_variables:** A list of variables that are required and will be prompted before processing the template.
- **output_filename_format:** A string specifying the format of the output filename, which can include placeholders for variables.
- **locale:** Specifies the locale for currency and number formatting.

### Customizing `program_config.json`

You can modify the `program_config.json` file to suit your needs:

- Add or remove required variables.
- Change the output filename format using placeholders.
- Set the locale for formatting.

**Note:** The placeholders in `output_filename_format` should match the names of variables provided in `required_variables` or in the template.

## Error Handling

The program includes error handling to provide a smooth user experience:

- **Missing Templates Directory:** If the `files/templates/` directory is missing, the program will inform you and exit gracefully.
- **No Templates Found:** If no templates are found in the directory, you'll be prompted to add some.
- **Invalid Input:** If you enter invalid data (e.g., a non-integer value for an integer field), the program will prompt you to try again.
- **Missing Output Directory:** The program will create the `files/output/` directory if it doesn't exist.

## Uninstallation

If you wish to uninstall the `template_parser` package:

```bash
pip uninstall template_parser
```

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/wegosh/TemplateParser-CLI).