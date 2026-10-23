#####################################################################
# A script to run tests with a given list of tasks
#####################################################################
import os
from os.path import dirname, abspath
import argparse
import logging
import subprocess
import tarfile
import yaml
import re
import time
from datetime import timedelta
import datetime
import threading
import ezreg_script_writer
import ezreg_tool_manager
import ezreg_path_manager
import ezreg_task_manager
import ezreg_job_manager
import ezreg_task_selection

#####################################################################
# Error codes
#####################################################################
error_codes = {"SUCCESS": 0, "ERROR": 1, "FILE_ERROR": 2}

#####################################################################
# Initialize logger
#####################################################################
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


#####################################################################
# Generate the runtime script
def generate_run_script_fpath(fdir, fname):
    return os.path.join(os.path.abspath(fdir), fname)


#####################################################################
# Generate the runtime script based on a given template and task settings
def generate_run_script_file(run_script_fpath, task_mgr, task_idx, subtask_idx):
    # Log runtime
    start_time = time.time()
    num_err = 0
    logging.info("Writing run script file '" + str(run_script_fpath) + "'...")

    script_writer = ezreg_script_writer.EzRegScriptWriter()
    # Set template file
    script_tmpl_file_abspath = task_mgr.subtask_template_path(task_idx, subtask_idx)
    print(f"template: {script_tmpl_file_abspath}")
    script_writer.set_template_file(script_tmpl_file_abspath)
    # Add variables to replace
    for slrv_name in task_mgr.subtask_single_line_replace_variables(task_idx, subtask_idx):
        script_writer.add_single_line_replace_variable(
            slrv_name, task_mgr.subtask_single_line_replace_value(task_idx, subtask_idx, slrv_name)
        )
    for mlrv_name in task_mgr.subtask_multi_line_replace_variables(task_idx, subtask_idx):
        script_writer.add_multi_line_replace_variable(
            mlrv_name, task_mgr.subtask_multi_line_replace_value(task_idx, subtask_idx, mlrv_name)
        )

    # Output to file
    os.makedirs(os.path.dirname(run_script_fpath), exist_ok=True)
    script_writer.write(run_script_fpath)

    end_time = time.time()
    time_diff = timedelta(seconds=(end_time - start_time))

    time_str = "Write runtime script file took " + str(time_diff)
    logging.info(time_str)

    return num_err


##################################################################
# Main function
##################################################################
if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement

    # Parse the options and apply sanity checks
    parser = argparse.ArgumentParser(description="Run regression tests with a given task list ")
    parser.add_argument(
        "--path_config",
        required=True,
        help="A yaml file contains a list of root paths to be used in task configuration file",
    )
    parser.add_argument(
        "--tut_config", required=True, help="A yaml file contains a list of tools under tests"
    )
    parser.add_argument(
        "--task", required=True, help="A yaml file contains a list of tasks to test"
    )
    parser.add_argument(
        "--root_dir",
        required=True,
        help="Root directory to apply on [ROOT_PATH] variable in all the configuraiton files",
    )
    parser.add_argument(
        "--task_select",
        default=ezreg_task_selection.ALL_TASK_SELECTED,
        help="Pick the single task to be run. Useful for debugging. The format is [task1,task2,task3]. By default, all tasks are selected",
    )
    parser.add_argument(
        "--new_thread_wait_time",
        type=int,
        default="1",
        help="Specify the waiting time before starting a new thread (unit: second)",
    )
    parser.add_argument(
        "--j", type=int, default=2, help="Specify maximum number of jobs to be run in parallel"
    )
    parser.add_argument(
        "--runtime_dirname",
        type=str,
        default="_ezreg_",
        help="Specify the prefix of the runtime directory to be created",
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="Perform dry-run without running program. Useful for debugging.",
    )
    # TODO: Add log error keyword setting file
    # TODO: Add log qor keyword setting file
    # TODO: generatei HTML format report or other format
    # parser.add_argument("--report", help="Output status report")

    args = parser.parse_args()

    num_errors = 0

    # Read tool configuration
    tut_mgr = ezreg_tool_manager.EzRegToolManager()
    tut_mgr.load(args.tut_config)
    # Early exit condition: when no test case is listed
    if tut_mgr.empty():
        logging.info("No tool under test found. Exiting...")
        exit(error_codes["ERROR"])
    # Read common settings on paths
    path_mgr = ezreg_path_manager.EzRegPathManager()
    path_mgr.set_root_dir(args.root_dir)
    path_mgr.load(args.path_config)

    # Read task configuration
    task_mgr = ezreg_task_manager.EzRegTaskManager()
    # load keywords
    for pvar in path_mgr.path_vars():
        pvar_name = path_mgr.path_var_name(pvar)
        pval = path_mgr.path_value(pvar)
        task_mgr.add_replace_keyword(pvar_name, pval)
    # Now load from Yaml
    task_mgr.load(args.task)

    # Early exit condition: when no test case is listed
    if task_mgr.empty():
        logging.info("No test case found. Exiting...")
        exit(error_codes["SUCCESS"])

    logging.info(f"Found {task_mgr.num_tasks()} tasks")
    # Preload task selection
    t_sel = ezreg_task_selection.EzRegTaskSelection()
    for t_idx in task_mgr.tasks():
        for st_idx in task_mgr.subtasks(t_idx):
            t_name = task_mgr.subtask_job_name_str(t_idx, st_idx)
            t_sel.add_predefined_task(t_name)
    t_sel.read_task_selection_str(args.task_select)
    # Report a stats for selected jobs
    logging.info(f"Selected {t_sel.num_selected()}/{t_sel.total()} tasks")
    # Configure job manager
    job_mgr = ezreg_job_manager.EzRegJobManager()
    # Add jobs one by one
    for task_id in task_mgr.tasks():
        task_name = task_mgr.task_name(task_id)
        # Walk through subtasks
        for stask_id in task_mgr.subtasks(task_id):
            stask_name = task_mgr.subtask_name(task_id, stask_id)
            job_name_str = task_mgr.subtask_job_name_str(task_id, stask_id)
            job_name = task_mgr.subtask_job_name(task_id, stask_id)
            # Bypass the task which is not selected
            if not t_sel.is_selected(job_name_str):
                continue
            if not task_mgr.subtask_enable(task_id, stask_id):
                continue
            job_mgr.create_job(job_name, task_mgr.subtask_expect_failure(task_id, stask_id))
            curr_rundir = task_mgr.subtask_workspace(task_id, stask_id)
            job_mgr.set_rundir(job_name, curr_rundir)
            # generate run script
            curr_tool = task_mgr.subtask_tut(task_id, stask_id)
            curr_run_script_fpath = generate_run_script_fpath(
                curr_rundir, tut_mgr.runtime_script(curr_tool)
            )
            num_errors += generate_run_script_file(
                curr_run_script_fpath, task_mgr, task_id, stask_id
            )
            job_mgr.set_job_run_script(job_name, curr_run_script_fpath)
            # Config the tool, binary and args for the current job
            cust_args = {}
            cust_args[ezreg_tool_manager.TCL_KEYWORD] = [
                str(os.path.abspath(curr_run_script_fpath))
            ]
            curr_tool_bin = tut_mgr.binary_path(curr_tool)
            curr_tool_args = tut_mgr.tool_args(curr_tool, cust_args)
            # configure tool args to job mgr
            job_mgr.set_tool(job_name, curr_tool, curr_tool_bin, curr_tool_args)
            # Set job dependencies
            for job_dep in task_mgr.subtask_dependencies(task_id, stask_id):
                job_mgr.add_depenency(job_name, job_dep)

    # Run jobs
    job_mgr.run_all(args.j, args.dryrun, True)
    num_errors += job_mgr.num_errors()
    if num_errors:
        logging.info(f"Regression jobs finished with {num_errors} errors")
    else:
        logging.info(f"Regression jobs finished successfully")

    if num_errors == 0:
        exit(error_codes["SUCCESS"])
    else:
        exit(error_codes["ERROR"])
