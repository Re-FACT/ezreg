.. _file_format_tool_config_file:

Tool Config File (.yaml)
========================

The tool config file defines a list of *Tool Under Tests* (TUT) for which regression tests should be performed (See details in :ref:`file_format_task_file`)

For each tool, detailed command-line options can be described for Ezreg to launch the tool

.. literalinclude:: example_tool_config.yaml
  :language: yaml

General Syntax
--------------

For each tool, a unique name should be defined. The name will be used as the tool name in the synthesis task file.

.. option:: bin="<string>"

  Specify the path to the binary executable of the tool. If the tool is in the system path, the detailed path can be omitted

.. option:: runtime_script="<string>"

  Specify the runtime script name to be applied when running the regression test. For example, ``run.tcl`` indicates a tcl file 

.. option:: runtime_log="<string>"

  Specify the runtime log file name to be applied when running the regression test. For example, ``run.log`` indicates a log file 

.. option:: options="<string>"

  Specify the command-line options (detailed arguments) when calling the tool. There are two types of arguments supported:

  - ``kargs``: keyword arguments which can be swapped in command line options. For example, ``--config run,tcl``
  - ``pargs``: positional arguments which must appear in a fixed location of command-line options. For example, ``run.tcl``
  
  The ``options`` should define the sequence of the keyword arguments and positional arguments. For example, ``pargs kargs``. User can also define only keyword arguments or positioinal arguments is considered.


Positional Arguments
--------------------

Positional arguments should be defined under ``pargs``. A list of arguments can be defined in the syntax of ``name``.

.. option:: name="<string>"

  Specify a positional argument. For example, 

.. code-block::

  # The [runtime_script] will be replaced with an auto-generated tcl file
  # The [runtime_log] will be replaced with the file name in runtime_log variable
  # When calling yosys, the command line options will be 
  #   /usr/bin/yosys/yosys -s local_run.ys
  yosys:
    bin: /usr/bin/yosys/yosys
  runtime_script: "local_run.ys"
  runtime_log: "run.log"
  options: "kargs"
  kargs:
    - name: "-s [runtime_script]"
    - name: "-l [runtime_log]"

Keyword Arguments
-----------------

Keyword arguments should be defined under ``kargs``. A list of arguments can be defined in the syntax of ``name``.

.. option:: name="<string>"

  Specify a positional argument. For example, 

.. code-block::

  # The [runtime_script] will be replaced with an auto-generated tcl file
  # The [runtime_log] will be replaced with the file name in runtime_log variable
  # When calling yosys, the command line options will be 
  #   /usr/bin/yosys/yosys local_run.ys --log ys.log
  yosys:
    bin: /usr/bin/yosys/yosys
  runtime_script: "local_run.ys"
  runtime_log: "ys.log"
  options: "pargs kargs"
  pargs:
    - name: "[runtime_script]"
  kargs:
    - name: "--log [runtime_log]"

