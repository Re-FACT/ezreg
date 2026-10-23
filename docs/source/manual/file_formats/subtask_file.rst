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

.. option:: dep="<string>"

  Define the dependency for a testcase. Must be a list of valid subtask names in the same subtask file. A testcase will be executed before all the dependent testcases are finished successfully.

.. option:: expect_failures="<bool>"

  Define if the testcase is expected to be failed. By default, it is ``false``.

.. _file_format_subtask_file_reserved_words:

Reserved words
--------------

Variables can be defined from the path configuration file.
For example, the variable ``[TASK_ROOT]`` is defined in the path configuraiton file

.. code-block::

  task_root: "/home/xtang/tests/tasks"

Name patterns can be used in the synthesis tasks. The following reserved word is supported

- ``[current_design]``: Once defined, the content will be replaced by the design name that is specified in the subtask name
