.. _file_format_log_check_keyword_file:

Log Check Keywords File (.yaml)
===============================

The log check keyword file defines a list of regular expression that will be used to identify error message in log files of EDA tool under test

.. literalinclude:: example_log_check_keyword.yaml
  :language: yaml

Syntax
------

.. option:: name="string>"

  Specify the name of the keyword. Only for debugging

.. option:: regex="<string>"

  Regular expression. For example, you can specify any matching pattern with anchors (e.g., at the beginning or end of a line). See details in `Python3 regular expression <https://docs.python.org/3/library/re.html>_`

.. option:: ignore_case="<bool>"

  If the regular expression should be case sensitive or not
