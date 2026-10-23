import os
import itertools
import re

# Constants

# Class of A general purpose script writer for tool under test
class EzRegScriptWriter:
    def __init__(self):
        # constants
        self.__mlrv_ = {} # Multiple line replaced variable, [var] = [val0, val1]
        self.__slrv_ = {} # Single line replaced variable, [var] = val0
        # Internal data
        self.__template_file_ = ""

    def set_template_file(self, val):
        self.__template_file_ = val
   
    def __var_to_match_pattern(self, var):
        return "${" + var + "}"

    def add_multi_line_replace_variable(self, var, vals):
        self.__mlrv_[var] = vals

    def add_single_line_replace_variable(self, var, val):
        self.__slrv_[var] = val

    def __update_line_with_slrv(self, i_line):
        o_line = i_line
        for var in self.__slrv_.keys():
            mpattern = self.__var_to_match_pattern(var)
            if mpattern in o_line:
                o_line.replace(mpattern, self.__slrv_[var])
        return o_line

    def __found_mlrv_in_line(self, i_line):
        for var in self.__mlrv_.keys():
            mpattern = self.__var_to_match_pattern(var)
            if mpattern in i_line:
                return True
        return False 

    def __update_line_with_mlrv(self, i_line):
        """
        Expands a line containing variables like ${varA}${varB} 
        using the Cartesian product of their respective lists.
        """
        # Find all unique variable placeholders in the line
        placeholders = re.findall(r'\${(\w+)}', line)
        if not placeholders:
            return [line] # Returns the line as-is, keeping \n

        variables = self.__mlrv_
        
        # Extract the lists corresponding to those placeholders
        lists_to_combine = [variables[p] for p in placeholders]
        
        expanded_lines = []
        for combination in itertools.product(*lists_to_combine):
            current_line = line
            for placeholder, value in zip(placeholders, combination):
                current_line = current_line.replace(f"${{{placeholder}}}", value)
            # No .strip() or .rstrip() used here, 
            # so leading padding and trailing \n are fully preserved.
            expanded_lines.append(current_line)
            
        return expanded_lines

    # For an input line to rewrite:
    # 1. replace all the single-line replace variables
    # 2. If the line does not contain any multi-line replace variable, do the output and early exit. Otherwise, continue on next step
    # 3. Base on the result of step 1, replace all the multi-line replace variables. In this step, multiple lines will be created.
    def __rewrite_line(self, fp, i_line):
        # Step 1
        o_line = self.__update_line_with_slrv(i_line)
        # Step 2
        if not self.__found_mlrv_in_line(o_line):
            fp.write(o_line)
            return
        # Step 3
        mo_line = self.__update_line_with_mlrv(o_line)
        fp.write(mo_line)

    # Write content to a file
    def write(self, fname):
        # Sanity checks
        if not os.path.isfile(self.__template_file_):
            raise Exception(f"Script template file '{self.__template_file_}' does not exist")
        # Open the template file, rewrite each line with pattern matcing to the final file
        with open(fname, "w") as o_tmpl_f:
            with open(self.__template_file_, "r") as i_tmpl_f:
                for line in i_tmpl_f.readlines():
                    # For regular lines, replace reserved words and output
                    self.__rewrite_line(o_tmpl_f, line)

    # Clear all the data
    def clear(self):
        self.__init__()
