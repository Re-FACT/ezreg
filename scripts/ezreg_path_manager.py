import logging
import yaml
import os

# Constants
# Keywords
ROOT_PATH_KEYWORD = "[ROORT_PATH]"

# Class of a path manager
class EzRegPathManager:
    def __init__(self):
        # Internal data
        self.__db_ = {}
        self.__root_dir_ = ""
        self.__is_dirty_ = True  # By default it should be dirty. After loading data and pass sanity checks, it becomes clean

    def set_root_dir(self, val):
        self.__root_dir_ = val

    def list_path_vars(self):
        self.__check_valid()
        logging.info(f"In total {len(self.__db_.keys())} path variable(s):")
        for pvar in self.__db_.keys():
            logging.info(f"\t{pvar}: {self.__db_[pvar]}")

    def __valid_path_var(self, pvar):
        if pvar not in self.__db_.keys():
            raise Exception(
                f"Path variable '{pvar}' is not defined in the path configuration file!\n{self.list_path_vars()}\n"
            )

    def path_var_name(self, pvar):
        self.__valid_path_var(pvar)
        return "[" + pvar.upper() + "]"

    def path_value(self, pvar):
        self.__valid_path_var(pvar)
        raw_val = self.__db_[pvar]
        final_val = raw_val.replace(ROOT_PATH_KEYWORD, self.__root_dir_)
        return final_val

    def empty(self):
        self.__check_valid()
        return not self.__db_

    # Internal method to check if data is valid, throw exeception when invalid. Useful for accessors
    def __check_valid(self):
        if self.__is_dirty_ == True:
            raise Exception("Try to access data when internal data is still dirty. Load data first")

    def is_valid(self):
        return not (self.__is_dirty_)

    # Load data from yaml file
    def load(self, yaml_filename):
        self.__db_ = {}  # Ensure a clean start
        with open(yaml_filename, "r") as stream:
            try:
                self.__db_ = yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                logging.error(exc)
        # TODO: May need a validator before flip the flag!
        self.__is_dirty_ = False

    # Clear all the data
    def clear(self):
        self.__init__()
