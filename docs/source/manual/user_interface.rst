.. _user_interface:

User Interface
--------------

The script has a command-line user interface which allows users to customize their regression jobs.

A short version of command-line options can be shown by calling the help desk through

.. code-block:: yaml

  python3 scripts/run_ezreg_test.py --help 


.. option:: --help

  Show help desk to list all the options

.. option:: --task <string>

  Specify the task configuration file to perform netlist synthesis jobs. See file format in :ref:`file_format_task_file` 

.. option:: --root_dir <string>

  Specify the root directory to apply on [ROOT_PATH] variable in all the configuraiton files

.. option:: --tut_config <string>

  Specify the path to a tool configuration file for *Tool Under Tests* (TUT) and their arguments. See file format in :ref:`file_format_tool_config_file` 

.. option:: --path_config <string>

  A yaml file contains a list of root paths to be used in task configuration file

.. option:: --dryrun

  Perform dry-run without running TUT. Useful for debugging.

.. option:: --task_select <string>

  Pick the single task to be run. Useful for debugging. The format is [task1.subtask1,task2.subtask2,task3.subtask3]. Use comma as a splitter, e.g., task1,task2,task3. By default, run all the listed tasks (except the subtasks that are disabled).

  .. note:: Please do not use the reserved word ``all`` as task name in your task configuration file

.. option:: -j <int> or --jobs <int>

  Specify the maximum number of jobs to be run in parallel

.. option:: --runtime_dirname <string>

  Specify the prefix of the runtime directory to be created

.. option:: --new_thread_wait_time <int>

  Specify the waiting time before starting a new thread (unit: second). Useful for machine which has a slow I/O speed


