import sys, logging

def handle_file_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logging.error(e)
            sys.exit(1)
        except IOError as e:
            logging.error(e)
            sys.exit(1)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            sys.exit(1)
    return wrapper