import re
import yaml
from typing import Dict, Any, Optional, Pattern


class EzRegLogErrorKeywords:
    """
    A class to load error keyword configurations from a YAML file
    and generate compiled regex patterns internally.
    """

    def __init__(self, file_path):
        self.__keywords = []
        self.__load_yaml(file_path)

    def __load_yaml(self, file_path):
        """Private method to read the YAML file and store data internally."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data and isinstance(data, dict):
                self.__keywords = data.get("keywords", [])
        except FileNotFoundError:
            raise FileNotFoundError(f"The configuration file '{file_path}' was not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    def num_keywords(self):
        """Returns the total number of keyword configurations available."""
        return len(self.__keywords)

    def keywords(self):
        return range(len(self.__keywords))

    def __valid_keyword(self, kw_id):
        return kw_id in self.keywords()

    def regex(self, kw_id):
        """
        Retrieves the regex pattern for a keyword at a given index and
        compiles it into a re.Pattern object, applying re.IGNORECASE if
        specified in the YAML configuration.
        """
        if not self.__valid_keyword(kw_id):
            raise Exception(
                "Invalid keyword id '{kw_id}' which is out of range [0, {len(self.__keywords) - 1}]"
            )
        keyword = self.__keywords[kw_id]

        pattern_str = keyword.get("regex")
        ignore_case = keyword.get("ignore_case", False)

        if not pattern_str:
            return None

        flags = re.IGNORECASE if ignore_case else 0
        return re.compile(pattern_str, flags)


# --- Example Usage ---
if __name__ == "__main__":
    # Initialize the class with your YAML file
    config_loader = EzRegLogErrorKeywords("log_error_keywords.yaml")

    total_keywords = config_loader.num_keywords()
    print(f"Total keywords found: {total_keywords}\n")

    # Walk through by index using the new method
    for i in config_loader.keywords():
        compiled_regex = config_loader.regex(i)
        print(f"Index: {i}")
        print(f"  Compiled Regex: {compiled_regex}")
        print("-" * 40)
        # Example test match
        test_line = "error: something went wrong"
        if compiled_regex and compiled_regex.search(test_line):
            print(f"  -> Matched test line: '{test_line}'")
        print("-" * 40)
