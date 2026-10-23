.. _file_format_path_config_file:

Path Config File (.yaml)
========================

The path config file defines a list of variables that will be used to replaced with actual values in 

- task file (See details in :ref:`file_format_task_file`)
- subtask file (See details in :ref:`file_format_subtask_file`) 

.. literalinclude:: example_path_config.yaml
  :language: yaml

Syntax
------

.. option:: <variable_name>="<variable_value>"

  Specify the name of the variable (which can be used in task and subtask files), and the values (which will replace the matched keyword)


Reserved words
--------------

- ``[ROOT_PATH]`` is defined by the command-line option ``--root_dir`` (See details in :ref:`user_interface`)
