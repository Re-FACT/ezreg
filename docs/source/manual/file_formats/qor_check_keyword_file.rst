.. _file_format_qor_check_keyword_file:

QoR Check Keyword File (.yaml)
==============================

The *Quality of Result* (QoR) check keyword file defines a list of QoR metrics that will be used to extract from json reports outputted by the EDA tool under test

.. literalinclude:: example_qor_check_keywords.yaml
  :language: yaml

Syntax
------

.. option:: name="<string>"

  Specify the name of the metric, which will be shown in QoR report. For example, if the name is set to ``num_of_gates``. the QoR report will has a column with the same name in the header row

.. code-block::

  task,num_of_gates
  ys_quick_test.and2,1
  ys_quick_test.and2x2,2

.. option:: keyword="<string>"

  Specify the hierarchy in the json content. Use '/' as the splitter in hierarchy. For example, the 'design/num_cells_by_type/$lut', indicate the json file tree: 

.. code-block::

  { 
    "design": {
      "num_cells_by_type": {
         "$lut": 33
      }
    }
  }

.. option:: upper_bound="<float>"

  Specify the upper bound in the value of the metric that can be tolerated during Qor check. Must be a positive number. For example, 0.3 indicates that Qor check can pass when the value is lower than 130% of the golden value

.. option:: lower_bound="<float>"

  Specify the lower bound in the value of the metric that can be tolerated during Qor check. Must be a positive number. For example, 0.3 indicates that Qor check can pass when the value is above 70% of the golden value

