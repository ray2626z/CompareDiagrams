# compare.py
This script automatically compares two class diagrams (exported in mermaid.md format). It identifies
- removed, new, and altered dependencies, 
- as well as removed, new, and atered methods in which classes.
## Inputs
- v470 and v480 for mockito
- v1.15 and v2.0.0 for logger
## Outputs
The output files of comparison is:
- m_changes for mockito
- l_changes for logger
## Usage:
python3 compare.py \<diagram1\> \<diagram2\> \<output_file\>

Note: \<diagram1\> and \<diagram2\> are files in mermaid.md format, expoted from intelliJ class diagrams
## Example:
python3 compare.py v470 v480 m_changes  (for mockito)

python3 compare.py v1.15 v2.0.0 l_changes (for logger)
