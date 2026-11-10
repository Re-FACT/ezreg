.. _tutorial_quickstart:

Quick Start
-----------

Prerequisites
~~~~~~~~~~~~~

Ezreg is designed to be a one-stop tool for testing EDA tools on 

- creating regression tasks
- running testcases, and 
- checking Quality-of-results

Before starting, please ensure that your EDA tool: 

- have a command-line interface supporting positional and keyword arguments
- support a script mode where the script can be load from the command-line interface

Preparation
~~~~~~~~~~~

In this example, we showcase how to create and run regression tasks for an open-source synthesis tool `yosys <https://github.com/YosysHQ/yosys>`_.

.. note:: To keep a clean project structure, strongly recommend users to create a new directory for regression tests. The following is an example how the regression test subdirectory ``tests`` is organized

.. code-block::

tests
├── benchmarks
│   └── and2x2
│       ├── and2.v
│       └── and2x2.v
├── common
│   ├── path_config.yml
│   ├── quick_test.yml
│   └── syn_tool_config.yml
├── requirements
│   ├── log_error_keywords.yaml
│   └── ys_rsrc_keywords.yaml
├── tasks
│   └── ys_quick_test
│       └── config
│           ├── golden.csv
│           └── task.yaml
└── tmpl
    └── ys_run_tmpl.ys

In the example, the tests contains a list of files as inputs:

- ``benchmarks``: Input designs for each testcases. Optional if the EDA tool does not require input files.
- ``common``: Contains the configuration files to drive Ezreg

  - ``path_config.yml``: The configuration file contains variables for regression test templates and tool configuration. Use to drive the ``--path_config`` option (See details in the :ref:`user_interface`)
  - ``quick_test.yml``: The configuration file contains regression tasks to be run. Use to drive the ``--task`` option (See details in the :ref:`user_interface`). You may create multiple task file and call them selectively.
  - ``syn_tool_config.yml``: The configuration file to describe how to use the command-line interface in regression tasks. Use to drive the ``--tut_config`` option (See details in the :ref:`user_interface`). 

- ``requirements``: The configuration file to extract and check *Quality-of-Result* (QoR) as the pass requirements for regression tasks. Use in the task configuration file (See details in the :ref:`file_format_subtask_file`).

  - ``log_error_keywords.yaml``: A configuration file to define the format of error messages when extracting from log files of EDA tools under tests. If the log contains any line that matches the error messages, the regression test will not pass. Depeneding on the actual tool, you need to customize the configuration file. 

  - ``ys_rsrc_keywords.yaml``: A configuration file to define what QoR metrics should be extracted from report files outputted by EDA tools under tests. Depeneding on the actual tool and report file format, you need to customize the configuration file. 

- ``tasks``: contain all the subtask configuration, golden results. Under the directory, there could be a number of regression tasks, each of which contains a subtask, golden result etc. 

  - ``config``: The subdirectory contains a subtask, a golden result etc. Suggest to have the subdirectory, as the local test data will be kept in the same level of the ``config`` subdirectory, for example, ``_work``. Separation between runtime workspace and configuration files is a good practice.

- ``tmpl``:  contain all the template script to drive the EDA tools. Subject to the purposes of regression tests, a number of template scripts may be created.
