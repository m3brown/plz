from colorama import Fore, Style

ERROR = Fore.RED
ERROR_DIM = Fore.RED + Style.DIM
WARNING = Fore.YELLOW
INFO = Fore.CYAN
INFO_DIM = Fore.CYAN + Style.DIM
RESET = Style.RESET_ALL


def __print_text(text, color_code, prefix=None):
    prefix_if_provided = "[{}] ".format(prefix) if prefix else ""
    print(color_code + prefix_if_provided + text + RESET)


def print_error(text, prefix=False):
    prefix_string = "ERROR" if prefix else None
    return __print_text(text, ERROR, prefix_string)


def print_error_dim(text, prefix=False):
    prefix_string = "ERROR" if prefix else None
    return __print_text(text, ERROR_DIM, prefix_string)


def print_warning(text, prefix=False):
    prefix_string = "WARNING" if prefix else None
    return __print_text(text, WARNING, prefix_string)


def print_info(text, prefix=False):
    prefix_string = "INFO" if prefix else None
    return __print_text(text, INFO, prefix_string)


def print_info_dim(text, prefix=False):
    prefix_string = "INFO" if prefix else None
    return __print_text(text, INFO_DIM, prefix_string)
