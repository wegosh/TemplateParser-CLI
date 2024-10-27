import os
import argparse
from .file_manager import FileManager
from .input_collector import InputCollector
from .config_manager import ConfigManager, ProgramConfigManager
from .template_processor import TemplateProcessor
from .application import TemplateApplication
from .user_interface import UserInterface

def main():
    parser = argparse.ArgumentParser(description='Template Parser CLI')
    parser.add_argument('template', nargs='?', help='Path to the template JSON file')
    parser.add_argument('--config', help='Path to the program configuration file', default=None)
    args = parser.parse_args()

    file_manager = FileManager()
    input_collector = InputCollector()

    cwd = os.getcwd()
    config_path = os.path.join(cwd, 'files', 'config.json')
    program_config_path = args.config if args.config else os.path.join(cwd, 'files', 'program_config.json')
    templates_dir = os.path.join(cwd, 'files', 'templates')
    output_dir = os.path.join(cwd, 'files', 'output')

    program_config_manager = ProgramConfigManager(program_config_path, file_manager)
    program_config_manager.load_config()

    template_processor = TemplateProcessor()

    user_interface = UserInterface(input_collector=input_collector)
    config_manager = ConfigManager(config_path, file_manager, user_interface=user_interface)

    app = TemplateApplication(
        file_manager=file_manager,
        config_manager=config_manager,
        template_processor=template_processor,
        templates_dir=templates_dir,
        output_dir=output_dir,
        program_config_manager=program_config_manager,
        user_interface=user_interface
    )

    template_path = args.template
    app.run(template_path)

if __name__ == '__main__':
    main()