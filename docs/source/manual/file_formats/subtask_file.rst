.. _file_format_subtask_file:

Subtask File (.yaml)
====================

- The subtask file defines a list of regression testcases to be executed

An example of file is shown as follows.

.. literalinclude:: example_reg_subtask.yaml
  :language: yaml

.. _file_format_subtask_file_syntax:

Syntax
------

.. option:: enable="<bool>"

  Specify if the testcase should be enabled or not.

.. option:: tool_under_test="<string>"

  Specify the tool under test in this testcase. Must be a valid tool defined in the tool configuration file. See details in :ref:`file_format_tool_config_file`

.. option:: path="<string>"

  Specify the template file path to be used for the tool under test

.. option:: multiple_line_replaced_variables="<string>"

  Define the variable to be replaced in the final script when being generated from the template file. Each variable must have a list of values. Each value will result in a new line to be added

.. option:: single_line_replaced_variables="<string>"

  Define the variable to be replaced in the final script when being generated from the template file. Each variable must be a string. 

.. option:: depend="<string>"

  Define the dependency for a testcase. Must be a list of valid subtask names in the same subtask file. A testcase will be executed before all the dependent testcases are finished successfully. For example,

.. code-block::

  depend:
    - "and2"
    - "and2x2"

.. option:: pass_checks="<list>"

  Specify a list of log check keyword files which should be applied on checking the logs in the testcase. See details in :ref:`file_format_log_check_keyword_file`

.. option:: qor_checks="<list>"

  Detailed settings to apply QoR check on the testcase

.. option:: file="<string>"

  Specify the report file path which contains QoR metrics. By default, find the file under the runtime workspace of the testcase. If the report file is outside the workspace, add relative path to it. For example,

.. code-block::

  - file: ../reports/area_report.txt 

.. option:: type="[json|log]"

  Specify the type of the report files. Dedicated file parser will be allocated when parsing Qor metrics and different type of keywords are required.

.. option:: metric="[string]"

  Specify the metrics to be extracted from the report files. See details in :ref:`file_format_qor_check_keyword_file`

.. option:: expect_failures="<bool>"

  Define if the testcase is expected to be failed. By default, it is ``false``.

Variable matching
-----------------

To match the variables, the template script file should use the uppercase within ``${}`` 
For example:

.. code-block:: yaml

  # Subtask
  single_line_replaced_variables:
    top_module: and2

.. code-block::

  # template file
  write_verilog ${TOP_MODULE}

.. _file_format_subtask_file_reserved_words:

Reserved words
--------------

Variables can be defined from the path configuration file.
For example, the variable ``[TASK_ROOT]`` is defined in the path configuration file

.. code-block::

  task_root: "/home/xtang/tests/tasks"

Name patterns can be used in the synthesis tasks. The following reserved word is supported

- ``[current_design]``: Once defined, the content will be replaced by the design name that is specified in the subtask name
- ``[current_subtask_root]``: Once defined, the content will be replaced by the absolute path to the parent directory of the current subtask configuration file
