.. _file_format_task_file:

Task File (.yaml)
=================

- The task file defines a list of regression sub-tasks to be executed

An example of file is shown as follows.

.. literalinclude:: example_reg_task.yaml
  :language: yaml

.. _file_format_task_file_syntax:

Syntax
``````

.. option:: name="<string>"

  Unique name of the task

.. option:: workspace="<string>"

  Specify the location where the runtime directories will be created and tools under test will be executed

.. option:: subtasks="<string>"

  Specify the location to the file which contains subtask definition. See details in the :ref:`file_format_subtask_file`.

.. _file_format_task_file_reserved_words:

Reserved words
``````````````

Variables can be defined from the path configuration file.
For example, the variable ``[TASK_ROOT]`` is defined in the path configuraiton file

.. code-block::

  task_root: "/home/xtang/tests/tasks"
