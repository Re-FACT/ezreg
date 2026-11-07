import yaml
from typing import Dict, Any, Optional

class EzRegQorJsonKeywords:
    """
    A class to load and encapsulate metric configuration data 
    from a YAML file using PyYAML without caching the file path[cite: 3].
    """
    
    def __init__(self, file_path: str):
        self.__metrics = []
        self.__load_yaml(file_path)

    def __load_yaml(self, file_path: str) -> None:
        """Private method to read the YAML file and store metric data internally."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if data and isinstance(data, dict):
                # Extract the list under the 'metric' key[cite: 3]
                self.__metrics = data.get("metric", [])
        except FileNotFoundError:
            raise FileNotFoundError(f"The configuration file '{file_path}' was not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    def num_metrics(self) -> int:
        """Returns the total number of metrics[cite: 3]."""
        return len(self.__metrics)

    def metrics(self) -> range:
        """Returns the range of valid metric indices for iteration."""
        return range(len(self.__metrics))

    def metric_name(self, index: int) -> Optional[str]:
        """Returns the name of the metric at the given index[cite: 3]."""
        try:
            return self.__metrics[index].get("name")
        except IndexError:
            return None

    def keyword(self, index: int) -> Optional[str]:
        """Returns the keyword hierarchy string for the metric at the given index[cite: 3]."""
        try:
            return self.__metrics[index].get("keyword")
        except IndexError:
            return None

    def upper_bound(self, index: int) -> Optional[float]:
        """Returns the upper bound tolerance value for the metric at the given index[cite: 3]."""
        try:
            return self.__metrics[index].get("upper_bound")
        except IndexError:
            return None

    def lower_bound(self, index: int) -> Optional[float]:
        """Returns the lower bound tolerance value for the metric at the given index[cite: 3]."""
        try:
            return self.__metrics[index].get("lower_bound")
        except IndexError:
            return None


# --- Example Usage ---
if __name__ == "__main__":
    # Initialize the class with the YAML file[cite: 3]
    config = EzRegQorJsonKeywords("ys_rsrc_keyword.yaml")
    
    print(f"Total metrics found: {config.num_metrics()}")
    
    # Walk through each metric index using the methods
    for i in config.metrics():
        print(f"\nIndex: {i}")
        print(f"  Name: {config.metric(i)}")
        print(f"  Keyword Hierarchy: {config.keyword(i)}")
        print(f"  Upper Bound: {config.upper_bound(i)}")
        print(f"  Lower Bound: {config.lower_bound(i)}")
        print("-" * 40)
