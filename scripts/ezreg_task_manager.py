import logging
import yaml
import os
from xml.dom import minidom

# Constants
REG_TASK_TAG = "reg_tasks"
REG_TASK_NAME_TAG = "name"
REG_TASK_WORKSPACE_TAG = "workspace"
REG_TASK_SUBTASKS_TAG = "subtasks"
REG_TASK_DEP_TAG = "depend"
REG_TASK_EXPECT_FAILURE_TAG = "expect_failure"
REG_SUBTASK_ENABLE_TAG = "enable"
REG_SUBTASK_TUT_TAG = "tool_under_test"
REG_SUBTASK_TMPL_TAG = "template"
REG_SUBTASK_TMPL_PATH_TAG = "path"
REG_SUBTASK_TMPL_MLRV_TAG = "multiple_line_replaced_variables"
REG_SUBTASK_TMPL_SLRV_TAG = "single_line_replaced_variables"

class EzRegTaskManager:
    def __init__(self):
        # Internal data
        self.__task_names_ = []
        self.__task_workspaces_ = []
        self.__task_subtask_configs_ = [] # file of subtasks
        self.__task_dependencies_ = []
        self.__task_expect_failures_ = []
        # Subtasks
        self.__task_subtask_names_ = [] # [itask][isubtask] = str
        self.__task_subtask_enable_ = []# [itask][isubtask] = bool
        self.__task_subtask_tut_ = []# [itask][isubtask] = str
        self.__task_subtask_template_paths_ = []# [itask][isubtask] = str
        self.__task_subtask_multi_line_replaced_variables_ = [] # [itask][isubtask][var_name] = [str0, str1 ... ]
        self.__task_subtask_single_line_replaced_variables_ = [] # [itask][isubtask][var_name] = str
        self.__is_dirty_ = True  # By default it should be dirty. After loading data and pass sanity checks, it will be flipped to clean
        self.__EXPECT_FAILURE_STRING_ = {"true": True, "false": False}
        # Replace keywords
        self.__replace_keywords_ = {}

    def add_replace_keyword(self, kw, val):
        self.__replace_keywords_[kw] = val

    def __replace_keyword(self, in_str):
        tmp_str = in_str
        for kw in self.__replace_keywords_.keys():
            tmp_str = tmp_str.replace(kw, self.__replace_keywords_[kw])
        return tmp_str
 
    def empty(self):
        return len(self.__task_names_) == 0

    # Internal method to check if data is valid, throw exeception when invalid. Useful for accessors
    def __check_valid(self):
        if self.__is_dirty_ == True:
            raise Exception("Try to access data when internal data is still dirty. Load data first")

    def num_tasks(self):
        self.__check_valid()
        return len(self.__task_names_)

    def tasks(self):
        self.__check_valid()
        return range(len(self.__task_names_))

    def __valid_task(self, task_idx):
        if task_idx not in self.tasks():
            raise Exception(f"Invalid task id {task_idx}")

    def task_name(self, task_idx):
        self.__check_valid()
        self.__valid_task(task_idx)
        return self.__task_names_[task_idx]

    def task_workspace(self, task_idx):
        self.__check_valid()
        self.__valid_task(task_idx)
        return self.__task_workspaces_[task_idx]

    def task_command(self, task_idx):
        self.__check_valid()
        self.__valid_task(task_idx)
        return self.__task_commands_[task_idx]

    def task_dependency(self, task_idx):
        self.__check_valid()
        self.__valid_task(task_idx)
        return self.__task_dependencies_[task_idx]

    def task_expect_failure(self, task_idx):
        self.__check_valid()
        self.__valid_task(task_idx)
        return self.__task_expect_failures_[task_idx]

    def is_valid(self):
        return not (self.__is_dirty_)

    def __check_required_yaml_syntax(self, parent_node, req_node_name, loc_msg):
        if req_node not in parent_node:
            raise Exception(f"Require syntax '{TASK_TAG}' is missing {loc_msg}\n")

    # Load data from yaml file
    def __load_from_yaml(self, yaml_filename):
        yaml_db = {}
        with open(yaml_filename, "r") as stream:
            try:
                yaml_db = yaml.load(stream, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                logging.error(exc)
        # For each sclibs
        self.__task_names_ = []
        self.__task_workspaces_ = []
        self.__task_dependencies_ = []
        # check required syntax
        self.__check_required_yaml_syntax(yaml_db, REG_TASK_TAG, "as root node"):
        for itask in range(len(yaml_db[REG_TASK_TAG])):
            self.__check_required_yaml_syntax(yaml_db[REG_TASK_TAG][itask], REG_TASK_NAME_TAG, f"under '{REG_TASK_TAG}' node {itask}"):
            task_name = yaml_db[REG_TASK_TAG][itask][REG_TASK_NAME_TAG]
            self.__check_required_yaml_syntax(yaml_db[REG_TASK_TAG][itask], REG_TASK_TASK_WORKSPACE_TAG, f"under task '{task_name}'"):
            self.__check_required_yaml_syntax(yaml_db[REG_TASK_TAG][itask], REG_TASK_TASK_SUBTASKS_TAG, f"under task '{task_name}'"):
            task_wkspace = self.__replace_keyword(yaml_db[REG_TASK_TAG][itask][REG_TASK_WORKSPACE_TAG])
            task_subtask_config = self.__replace_keyword(yaml_db[REG_TASK_TAG][itask][REG_TASK_SUBTASKS_TAG])
            task_deps = []
            if REG_TASK_DEP_TAG in yaml_db[REG_TASK_TAG][itask]:
                task_deps = yaml_db[REG_TASK_TAG][itask][REG_TASK_DEP_TAG]
            task_expect_failure = False
            if REG_TASK_EXPECT_FAILURE_TAG in yaml_db[REG_TASK_TAG][itask]:
                task_expect_failure = yaml_db[REG_TASK_TAG][itask][REG_TASK_EXPECT_FAILURE_TAG]
            self.__task_names_.append(task_name)
            self.__task_workspaces_.append(task_wkspace)
            self.__task_subtask_configs_.append(task_subtask_config)
            self.__task_dependencies_.append(task_deps)
            self.__task_expect_failures_.append(task_expect_failure)
            self.__task_subtask_names_.append([])
            self.__task_subtask_enable_.append([])
            self.__task_subtask_tut_.append([])
            self.__task_subtask_template_paths_.append([])
            self.__task_subtask_multi_line_replaced_variables_.append([])
            self.__task_subtask_single_line_replaced_variables_.append([])
            # Parse subtasks
            subyaml_db = {}
            with open(task_subtask_config, "r") as substream:
                try:
                    subyaml_db = yaml.load(substream, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:
                    logging.error(exc)
            for subtask_name in subyaml_db:
                self.__check_required_yaml_syntax(subyaml_db[subtask_name], REG_SUBTASK_ENABLE_TAG, f"under subtask '{subtask_name}' of task '{task_name}'"):
                self.__check_required_yaml_syntax(subyaml_db[subtask_name], REG_SUBTASK_TUT_TAG, f"under subtask '{subtask_name}' of task '{task_name}'"):
                self.__check_required_yaml_syntax(subyaml_db[subtask_name], REG_SUBTASK_TMP_TAG, f"under subtask '{subtask_name}' of task '{task_name}'"):
                self.__check_required_yaml_syntax(subyaml_db[subtask_name][REG_SUBTASK_TMPL_TAG], REG_SUBTASK_TMP_PATH_TAG, f"under node '{REG_SUBTASK_TMPL_TAG}' of subtask '{subtask_name}' of task '{task_name}'"):
                self.__check_required_yaml_syntax(subyaml_db[subtask_name][REG_SUBTASK_TMPL_TAG], REG_SUBTASK_TMP_MLRV_TAG, f"under node '{REG_SUBTASK_TMPL_TAG}' of subtask '{subtask_name}' of task '{task_name}'"):
                self.__check_required_yaml_syntax(subyaml_db[subtask_name][REG_SUBTASK_TMPL_TAG], REG_SUBTASK_TMP_SLRV_TAG, f"under node '{REG_SUBTASK_TMPL_TAG}' of subtask '{subtask_name}' of task '{task_name}'"):
                subtask_enable = subyaml_db[subtask_name][REG_SUBTASK_ENABLE_TAG]
                subtask_tut = subyaml_db[subtask_name][REG_SUBTASK_TUT_TAG]
                subtask_tmpl_path = subyaml_db[subtask_name][REG_SUBTASK_TMPL_TAG][REG_SUBTASK_TMPL_PATH_TAG]
                # Fill data
                self.__task_subtask_names_[itask].append(subtask_name)
                self.__task_subtask_enable_[itask].append(subtask_name)
                self.__task_subtask_tut_[itask].append(subtask_tut)
                self.__task_subtask_template_paths_[itask].append(subtask_tmpl_path)
                curr_mlrv = subyaml_db[subtask_name][REG_SUBTASK_TMPL_TAG][REG_SUBTASK_TMPL_MLRV_TAG]:
                self.__task_subtask_multi_line_replaced_variables_.append(curr_mlrv)
                curr_slrv = subyaml_db[subtask_name][REG_SUBTASK_TMPL_TAG][REG_SUBTASK_TMPL_MLRV_TAG]:
                self.__task_subtask_single_line_replaced_variables_.append(curr_slrv)

    def __valid_dep(self, dep_name):
        for itask in range(len(self.__task_names_)):
            if dep_name == self.__task_names_[itask]:
                return True
        return False

    def load(self, fname):
        if fname.endswith(".yaml") or fname.endswith(".yml"):
            self.__load_from_yaml(fname)
        else:
            raise Exception("Invalid file format. Support only YAML and XML file")
        # Validate all the deps
        for itask in range(len(self.__task_names_)):
            for dep_name in self.__task_dependencies_[itask]:
                if dep_name == self.__task_names_[itask]:
                    raise Exception(
                        f"Task '{self.__task_names_[itask]}' cannot have a dependency on itself!\n"
                    )
                if not self.__valid_dep(dep_name):
                    raise Exception(
                        f"Dependency '{dep_name}' of task '{self.__task_names_[itask]}' is not a valid task name!\n"
                    )

        # TODO: May need a validator before flip the flag!
        self.__is_dirty_ = False

    # Clear all the data
    def clear(self):
        self.__init__()
