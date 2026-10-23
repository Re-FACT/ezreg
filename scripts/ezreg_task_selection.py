import time
import logging

ALL_TASK_SELECTED = "all"

# Class of a task selection
# Task selection accepts a string that defines a list of selected tasks, including designs and steps
# The format is
#  taskA.designA.stepA,taskB.designB.stepB
# Note that keyword all may be applied to select all tasks, design and steps!
class EzRegTaskSelection:
    def __init__(self):
        # Internal data
        self.__tasks_ = {}
        self.__is_dirty_ = True  # Remain dirty is there is no predefined tasks!
        # Constants
        self.__SELECT_ALL_ = ALL_TASK_SELECTED
        self.__TASK_DELIMA_ = ","

    # Return the number of selected jobs
    def num_selected(self):
        cnt = 0
        for key in self.__tasks_.keys():
            if self.__tasks_[key]:
                cnt += 1
        return cnt

    # Return the total number of jobs
    def total(self):
        return len(self.__tasks_)

    # Load from predefined tasks which are the based on selected tasks
    def add_predefined_task(self, q_name):
        self.__tasks_[q_name] = False
        # No longer dirty
        self.__is_dirty_ = False

    # Mark all tasks as selected
    def __select_all_tasks(self):
        for task in self.__tasks_:
            self.__tasks_[task] = True

    # Load from an string
    def read_task_selection_str(self, q_str):
        if self.__is_dirty_:
            raise Exception("Read task selection requires tasks to be predefined first!")
        # all select keyword has no. 1 priority
        if q_str == self.__SELECT_ALL_:
            self.__select_all_tasks()
            return 0
        selected_tasks = q_str.split(self.__TASK_DELIMA_)
        # Now parsing
        for s_q in selected_tasks:
            if s_q not in self.__tasks_:
                raise Exception(f"Invalid task '{s_q}' which is not predefined!")
            self.__tasks_[s_q] = True

    def is_selected(self, s_q):
        if s_q not in self.__tasks_:
            raise Exception(f"Invalid task '{s_q}' which is not predefined!")
        return self.__tasks_[s_q]

    # Print a list of designs under the selected task
    def list_tasks(self):
        logging.info(f"List all the tasks:")
        for curr_q in self.__tasks_.keys():
            logging.info(f"\t{curr_q}")
