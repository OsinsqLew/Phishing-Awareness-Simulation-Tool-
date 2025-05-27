import configparser
from pathlib import Path


def get_from_config(file: str, section: str) -> configparser.SectionProxy:
    """Gets section from .ini file.

    Args:
        file: A string, name of the file to retrieve data from.
        section: A string, name of the section to retrieve data from.

    Returns:
        config section

    Raises:
        FileNotFoundError if file of a given name does not exist.
        KeyError if section/parameter of a provided name does not exist.
    """
    config = configparser.ConfigParser()
    config_file = Path(__file__).parent / file

    if not config_file.is_file():
        raise FileNotFoundError(
            f"No file named {file} in {Path(__file__).parent.name}"
        )

    config.read(config_file)
    if not config.has_section(section):
        raise KeyError(f"No section named {section} in {file}")

    return config[section]