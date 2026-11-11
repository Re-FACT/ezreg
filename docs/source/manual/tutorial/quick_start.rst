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

If you are using ezreg as a submodule, suggest to place it under the ``tests`` directory

.. code-block::

  tests
  ├── ezreg
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

.. _tutorial_quickstart_path_config:

Path Configuration
~~~~~~~~~~~~~~~~~~

The path configuration file contains variables which can be replaced in the task and subtask configuration files. 
The reserved word ``[ROOT_PATH]`` will be replaced by the ``--root_dir`` when running the regression test. (See details in :ref:`file_format_path_config_file`).
This is designed to make the task configuration files portable between machines without modification. 
In the following example, four variables are defined which will impact the :ref:`tutorial_quickstart_example_subtask` 

.. code-block:: yaml
  :caption: Example path configuration file
  :name: tutorial_quickstart_example_path_config

  benchmark_root: "[ROOT_PATH]/tests/benchmarks"
  template_root: "[ROOT_PATH]/tests/tmpl"
  task_root: "[ROOT_PATH]/tests/tasks"
  req_root: "[ROOT_PATH]/tests/requirements"


.. _tutorial_quickstart_tool_config:

Tool Configuation
~~~~~~~~~~~~~~~~~

Before writing the configuration file, suggest to check if your EDA tool has been properly installed or built.

The tool configuration file tells ezreg how to call the EDA tool in your testcase. 

In a tool configuration file, you can

- Define the command-line option for a EDA tool
- Define multiple tools with their usages. This is to cover flow tests based on a series of EDA tools.
- Define different command-line options on the same tool. This is to cover different objective/features for EDA tools

In this example, we focus on a typical usage of the ``yosys``.

.. code-block:: yaml
  :caption: Example tool configuration file
  :name: tutorial_quickstart_example_tool_config

  yosys:
    bin: yosys
    runtime_script: run.ys
    options: "kargs"
    kargs:
      - name: "-s [runtime_script]"

For detailed syntax, refer to :ref:`file_format_tool_config_file`

In the following example, ezreg will call ``yosys`` with the following command-line options

.. code-block:: shell

  yosys -s run.ys > ys.log

Note that, in the example, it requires that the ``yosys`` binary is in the system path. If ``yosys`` is not under the system path, you may give the full path to the ``yosys`` binary, e.g., 

.. code-block:: yaml

  yosys:
    bin: /home/xtang/github/yosys/build/yosys
    runtime_script: run.ys
    options: "kargs"
    kargs:
      - name: "-s [runtime_script]"

.. _tutorial_quickstart_run_script_tmpl:

Run Script Template
~~~~~~~~~~~~~~~~~~~

Note that the runtime script ``run.ys`` in the :ref:`tutorial_quickstart_tool_config` is generated by ezreg on-fly.

The runtime script is generated by replacing variables for each testcase based on a given template.

Here is an example of the template, showing a simple and quick usage on Ysoys:

- read design source files in Verilog format
- synthesis the design in the recipe for Xilinx devices
- write out post-synthesis netlists
- report the resource usage to a json file

Note that each line contains a variable in the format of ``${}`` whose actual value is defined in task configuration file.

.. code-block::
  :caption: Example run script template
  :name: tutorial_quickstart_example_run_script_template

  read_verilog ${DESIGN_INPUTS}
  synth_xilinx -top ${TOP_MODULE}
  write_verilog ${DESIGN_OUTPUT}
  tee -o ${RESOURCE_REPORT} stat -json 

.. _tutorial_quickstart_task_config:

Task Configuration
~~~~~~~~~~~~~~~~~~

A regression task should be defined in a task configuration file.
Here is an example of the ``common/quick_test.yaml`` 

.. code-block:: yaml
  :caption: Example task configuration file
  :name: tutorial_quickstart_example_task

  reg_tasks:
    - name: ys_quick_test
      workspace: "[TASK_ROOT]/ys_quick_test/_work"
      subtasks: "[TASK_ROOT]/ys_quick_test/config/task.yaml" 
      golden_result: "[TASK_ROOT]/ys_quick_test/config/golden.csv"

A task configuration file may consists of one or more subtasks, each of which has 

- a unique name
- a dedicated workspace, where all the runtime data will be generated and outputted
- a dedicated subtask configuration file
- a golden result file for Qor tracking

A subtask configuration file can be created.
Here is an example of the ``tasks/ys_quick_test/config/task.yaml`` 

.. code-block:: yaml
  :caption: Example subtask configuration file
  :name: tutorial_quickstart_example_subtask

  and2:
    tool_under_test: yosys 
    template:
      path: "[TEMPLATE_ROOT]/ys_run_tmpl.ys"
      multiple_line_replaced_variables: 
        design_inputs:
          - "[BENCHMARK_ROOT]/and2x2/and2.v"
      single_line_replaced_variables: 
        design_output: "and2_post_synth.v"
        top_module: "[current_design]"
        resource_report: "resource.json"
    pass_checks:
      - "[REQ_ROOT]/log_error_keywords.yaml"
    qor_checks:
      - file: resource.json
        type: json
        metric: "[REQ_ROOT]/ys_rsrc_keywords.yaml"
  and2x2:
    tool_under_test: yosys
    template:
      path: "[TEMPLATE_ROOT]/ys_run_tmpl.ys" 
      multiple_line_replaced_variables: 
        design_inputs:
          - "[BENCHMARK_ROOT]/and2x2/and2.v"
          - "[BENCHMARK_ROOT]/and2x2/and2x2.v"
      single_line_replaced_variables: 
        design_output: "and2x2_post_synth.v"
        top_module: "[current_design]"
        resource_report: "resource.json"
    depend:
      - "and2"
    pass_checks:
      - "[REQ_ROOT]/log_error_keywords.yaml"
    qor_checks:
      - file: resource.json
        type: json
        metric: "[REQ_ROOT]/ys_rsrc_keywords.yaml"

A subtask configuration file may consists of one or more testcases, each of which has

- a unique name in the subtask context
- a template file to generate runtime script
- variables to replace the template script during runtime
- pass requirements to check errors in log
- Qor check requirements as compared to the golden results

In the example above, two testcases ``and2`` and ``and2x2`` are defined.
As the ``and2x2`` is dependent on the ``and2``, when running the regression test, the ``and2x2`` will not be executed only after ``and2`` is finished successfully.

AS the two testcases share the same template file, they have the same list of variables but in different values

- ``design_inputs``: replace the ``${DESIGN_INPUTS}`` in the :ref:`tutorial_quickstart_example_run_script_template`. Note that the variable is defined as the ``multiple_line_replaced_variables``, multiple lines will be added to the autogenerated runtime script on each matched pattern. For example,  

.. code-block::

  # Assume the ROOT_PATH is /home/xtang/github/ezreg/
  read_verilog /home/xtang/github/ezreg/tests/benchmarks/and2x2/and2.v
  read_verilog /home/xtang/github/ezreg/tests/benchmarks/and2x2/and2x2.v

- ``top_module``: replace the ``${TOP_MODULE}`` in the :ref:`tutorial_quickstart_example_run_script_template`. Note that here the reserved word ``[current_design]`` is used which is the subtask name, e.g., ``and2``.
- ``design_output``: replace the ``${DESIGN_OUTPUT}`` in the :ref:`tutorial_quickstart_example_run_script_template`
- ``resource_report``: replace the ``${RESOURCE_REPORT}`` in the :ref:`tutorial_quickstart_example_run_script_template`

In the pass requirements, ezreg will parse the log file of each yosys run and check any pattern defined as error messages. The patterns are defined in the ``[REQ_ROOT]/log_error_keywords.yaml``, which is ``/home/xtang/github/ezreg/tests/requirements/log_error_keywords.yaml`` after replacing variables in the :ref:`tutorial_quickstart_example_path_config` 

.. code-block:: yaml
  :caption: Example pass requirement file to identify log errors
  :name: tutorial_quickstart_example_log_error_keywords

  keywords:
  - name: "Regular error"
    ignore_case: true
    regex: "^Error"
  - name: "Failures"
    ignore_case: true
    regex: "^Fail [^0]"
  - name: "SegFault"
    regex: "^Segmentation fault"
  - name: "Assertation"
    regex: "^Asseration.*failed"

In the :ref:`tutorial_quickstart_example_log_error_keywords`, there are 4 error patterns defined through regular expressions. 

For example, the ``^Error`` indicates any line starts with ``Error`` will be treated as an error message.

In the QoR check requirements, ezreg will parse the report file of each yosys run and extract values by following the ``[REQ_ROOT]/ys_rsrc_keywords.yaml``, which is ``/home/xtang/github/ezreg/tests/requirements/ys_rsrc_keywords.yaml`` after replacing variables in the :ref:`tutorial_quickstart_example_path_config` 

.. code-block:: yaml
  :caption: Example Qor requirement file to extract metrics
  :name: tutorial_quickstart_example_qor_check_keywords

  metric:
   - name: num_of_luts
     keyword: "design/num_cells_by_type/$_lut_"
     upper_bound: 0.3
     lower_bound: 0.5

Ezreg will use a json parser to extract metrics from the ``resource.json`` file outputted by yosys. The metric is in the hierarchy of ``design/num_cells_by_type/$lut`` in the json file. For example, 

.. code-block:: json

  { 
    "design": {
      "num_cells_by_type": {
         "$lut": 33
      }
    }
  }

In the golden results (csv file format), the metric will be named as ``num_of_luts`` in the header row.

.. code-block:: csv

  task,num_of_luts
  ys_quick_test.and2,1

During the QoR check, as defined in the ``upper_bound`` and ``lower_bound``, ezreg will fail when the number of luts is 30% higher than the golden result ``1`` or 50% lower than the golden result. 

.. _tutorial_quickstart_dryrun_reg_test:

Dryrun regression tests
~~~~~~~~~~~~~~~~~~~~~~~

After all the required inputs are ready, now it is time to run the regression tests.
Assume you are under the parent directory of the ``tests``.
If this is the first to launch your regression test, suggest to dryrun the regression tests.

.. code-block::

  python3 tests/ezreg/scripts/run_ezreg_test.py --path_config tests/common/path_config.yml --tut_config tests/common/syn_tool_config.yml --task tests/common/quick_test.yml --root_dir . --dryrun 

In dryrun mode, ezreg will 

- create workspace for each testcase 
- generate runtime script
- show guidelines with exact commands to run each testcase

In dryrun mode, ezreg will not call the EDA tool under test, check log and QoR.

After calling ezreg in dryrun mode, You may see the following printed on your screen 

.. code-block:: 

  ==== Quick test ====
  INFO: Found 1 tasks
  INFO: Selected 2/2 tasks
  INFO: Writing run script file '/home/xtang/github/tests/tasks/ys_quick_test/_work/and2/run.ys'...
  INFO: Write runtime script file took 0:00:00.000306
  INFO: Writing run script file '/home/xtang/github/tests/tasks/ys_quick_test/_work/and2x2/run.ys'...
  INFO: Write runtime script file took 0:00:00.000211
  INFO: ys_quick_test_and2 start at......................... 2026-11-11T09:57:23.833658
  INFO: User choose to perform dryrun
   User may run with 
  	yosys -s /home/xtang/github/tests/tasks/ys_quick_test/_work/and2/run.ys > ys_quick_test_and2_ezreg_run.log
  INFO: ys_quick_test_and2 ends  at......................... 2026-11-11T09:57:23.833804
  INFO: ys_quick_test_and2 ............................................................ [Pass]
  INFO: ys_quick_test_and2......................................... took 0:00:00.000147
  INFO: ys_quick_test_and2x2 start at....................... 2026-11-11T09:57:24.835084
  INFO: User choose to perform dryrun
   User may run with 
  	yosys -s /home/xtang/github/tests/tasks/ys_quick_test/_work/and2x2/run.ys > ys_quick_test_and2x2_ezreg_run.log
  INFO: ys_quick_test_and2x2 ends  at....................... 2026-11-11T09:57:24.835244
  INFO: ys_quick_test_and2x2 .......................................................... [Pass]
  INFO: ys_quick_test_and2x2....................................... took 0:00:00.000160
  INFO: Finished 2 jobs
  INFO: 	Passed 2
  INFO: 	Failed 0
  INFO: 
  	[Fail*] Expect fail but it passed in the run
  INFO: 
  	[Pass*] Expect fail but it failed in the run
  INFO: Regression jobs finished successfully
  INFO: Skip Qor check as dryrun is enabled by user


You may follow the guideline on try a testcase, e.g., 

.. code-block::

  cd /home/xtang/github/tests/tasks/ys_quick_test/_work/and2x2
  yosys -s /home/xtang/github/tests/tasks/ys_quick_test/_work/and2x2/run.ys > ys_quick_test_and2x2_ezreg_run.log

- If any error occurs, debug can start immediately.
- If it finishes successfully, you can move to run regression tests 

.. _tutorial_quickstart_run_reg_test:

Run regression tests
~~~~~~~~~~~~~~~~~~~~

Once you can pass dryrun mode and local run can also pass, it is time to try running regression tests without Qor check
Assume you are under the parent directory of the ``tests``.
You can run the regression tests

.. code-block::

  python3 tests/ezreg/scripts/run_ezreg_test.py --path_config tests/common/path_config.yml --tut_config tests/common/syn_tool_config.yml --task tests/common/quick_test.yml --root_dir . 

Ezreg will 

- create workspace for each testcase 
- generate runtime script
- run the EDA tool under test in the dedicated workspace for each testcase.
- check logs on errors and parse all the reports for QoR metrics

You may see the following printed on your screen 

.. code-block::

  ==== Regression test ====
  INFO: Found 1 tasks
  INFO: Selected 2/2 tasks
  INFO: Writing run script file '/home/xifan/github/tests/tasks/ys_quick_test/_work/and2/run.ys'...
  INFO: Write runtime script file took 0:00:00.000338
  INFO: Writing run script file '/home/xifan/github/tests/tasks/ys_quick_test/_work/and2x2/run.ys'...
  INFO: Write runtime script file took 0:00:00.000244
  INFO: ys_quick_test_and2 start at......................... 2026-11-11T10:18:34.703993
  INFO: ys_quick_test_and2 ends  at......................... 2026-11-11T10:18:36.983773
  INFO: Checking log file '/home/xifan/github/tests/tasks/ys_quick_test/_work/and2/ys_quick_test_and2_ezreg_run.log'...
  INFO: Checking log file took 0:00:00.002428
  INFO: ys_quick_test_and2 ............................................................ [Pass]
  INFO: ys_quick_test_and2......................................... took 0:00:02.279779
  INFO: ys_quick_test_and2x2 start at....................... 2026-11-11T10:18:36.986690
  INFO: ys_quick_test_and2x2 ends  at....................... 2026-11-11T10:18:39.279089
  INFO: Checking log file '/home/xifan/github/tests/tasks/ys_quick_test/_work/and2x2/ys_quick_test_and2x2_ezreg_run.log'...
  INFO: Checking log file took 0:00:00.002235
  INFO: ys_quick_test_and2x2 .......................................................... [Pass]
  INFO: ys_quick_test_and2x2....................................... took 0:00:02.292399
  INFO: Finished 2 jobs
  INFO: 	Passed 2
  INFO: 	Failed 0
  INFO: 
  	[Fail*] Expect fail but it passed in the run
  INFO: 
  	[Pass*] Expect fail but it failed in the run
  INFO: Regression jobs finished successfully

.. _tutorial_quickstart_create_golden:

Create Golden Results
~~~~~~~~~~~~~~~~~~~~~

If your regression tests pass, the remaining work is on the QoR checks.
Note that in :ref:`tutorial_quickstart_run_reg_test`, QoR check is not enabled as there are not golden results yet.
In this step, you can run Ezreg to generate golden results:

.. note:: Each time new testcases are added, you need to update the golden results 

.. code-block::

  python3 tests/ezreg/scripts/run_ezreg_test.py --path_config tests/common/path_config.yml --tut_config tests/common/syn_tool_config.yml --task tests/common/quick_test.yml --root_dir . --create_golden --parse_report_only

Ezreg will skip running EDA tool under test, and directly start  

- checking logs on errors
- parsing all the reports for QoR metrics
- creating golden result as designated in :ref:`tutorial_quickstart_example_task`

You may see the following printed on your screen 

.. code-block::

  ==== Regression test ====
  INFO: Found 1 tasks
  INFO: Selected 2/2 tasks
  INFO: Writing run script file '/home/xifan/github/tests/tasks/ys_quick_test/_work/and2/run.ys'...
  INFO: Write runtime script file took 0:00:00.000322
  INFO: Writing run script file '/home/xifan/github/tests/tasks/ys_quick_test/_work/and2x2/run.ys'...
  INFO: Write runtime script file took 0:00:00.000208
  INFO: Created/Updated golden QoR for task 'ys_quick_test' under '/home/xifan/github/tests/tasks/ys_quick_test/config/golden.csv'
  
The golden result file is humanreadble in CSV format. For example, 

.. code-block::

  task,num_of_gates
  ys_quick_test.and2,1
  ys_quick_test.and2x2,2

.. _tutorial_quickstart_qor_check:

QoR Check
~~~~~~~~~

If your golden results are set, you can start iteration on regression tests with the QoR checks.
Note that in :ref:`tutorial_quickstart_run_reg_test`, QoR check is not enabled as there are not golden results yet.
In this step, you can run Ezreg with Qor check enabled:

.. code-block::

  python3 tests/ezreg/scripts/run_ezreg_test.py --path_config tests/common/path_config.yml --tut_config tests/common/syn_tool_config.yml --task tests/common/quick_test.yml --root_dir . --check_qor

Ezreg will skip running EDA tool under test, and directly start  

- create workspace for each testcase 
- generate runtime script
- run the EDA tool under test in the dedicated workspace for each testcase.
- checking logs on errors
- parsing all the reports for QoR metrics
- compare to golden result and check if all the QoR metrics are in acceptable ranges

You may see the following printed on your screen 

.. code-block::

  ==== Regression test ====
  INFO: Found 1 tasks
  INFO: Selected 2/2 tasks
  INFO: Writing run script file '/home/xifan/github/refact-fpga/ezreg/tests/tasks/ys_quick_test/_work/and2/run.ys'...
  INFO: Write runtime script file took 0:00:00.000307
  INFO: Writing run script file '/home/xifan/github/refact-fpga/ezreg/tests/tasks/ys_quick_test/_work/and2x2/run.ys'...
  INFO: Write runtime script file took 0:00:00.000195
  INFO: ys_quick_test_and2 start at......................... 2026-11-11T10:34:08.737307
  INFO: ys_quick_test_and2 ends  at......................... 2026-11-11T10:34:11.036718
  INFO: Checking log file '/home/xifan/github/refact-fpga/ezreg/tests/tasks/ys_quick_test/_work/and2/ys_quick_test_and2_ezreg_run.log'...
  INFO: Checking log file took 0:00:00.002448
  INFO: ys_quick_test_and2 ............................................................ [Pass]
  INFO: ys_quick_test_and2......................................... took 0:00:02.299411
  INFO: ys_quick_test_and2x2 start at....................... 2026-11-11T10:34:11.039632
  INFO: ys_quick_test_and2x2 ends  at....................... 2026-11-11T10:34:13.336430
  INFO: Checking log file '/home/xifan/github/refact-fpga/ezreg/tests/tasks/ys_quick_test/_work/and2x2/ys_quick_test_and2x2_ezreg_run.log'...
  INFO: Checking log file took 0:00:00.002428
  INFO: ys_quick_test_and2x2 .......................................................... [Pass]
  INFO: ys_quick_test_and2x2....................................... took 0:00:02.296798
  INFO: Finished 2 jobs
  INFO: 	Passed 2
  INFO: 	Failed 0
  INFO: 
  	[Fail*] Expect fail but it passed in the run
  INFO: 
  	[Pass*] Expect fail but it failed in the run
  INFO: Regression jobs finished successfully
  INFO: QoR check passed

If the QoR check failed, details about which metric failed in which testcase will be printed.
For example, 

.. code-block::

  INFO: Regression jobs finished successfully
  INFO: 'num_of_luts' of design 'ys_quick_test.and2' in current run (1) exceeds the lower bound limit 0.3 (reference value is 4)
  INFO: 'num_of_luts' of design 'ys_quick_test.and2x2' in current run (2) exceeds the lower bound limit 0.3 (reference value is 6)
  INFO: 'num_of_luts' of design 'ys_quick_test.and2' in current run (1) exceeds the lower bound limit 0.3 (reference value is 4)
  INFO: 'num_of_luts' of design 'ys_quick_test.and2x2' in current run (2) exceeds the lower bound limit 0.3 (reference value is 6)
  ERROR: QoR failed with 4 errors
  
