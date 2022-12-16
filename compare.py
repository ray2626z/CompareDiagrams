import sys
from difflib import unified_diff
from difflib import context_diff
import difflib as d
import re

if __name__ == '__main__':

    file1 = ''
    file2 = ''

    if len(sys.argv) != 3:
        print("Usage: python3 compare.py <diagram1> <diagram2>")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]

    # Open class diagram flies (format: mermaid.md)
    with open(file1) as f1, open(file2) as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

    # Record all changes
    # diff_lines = unified_diff(a=f1_lines, b=f2_lines, fromfile="f1.txt", tofile="f2.txt", lineterm='\n')
    # diff_lines = context_diff(a=f1_lines, b=f2_lines, fromfile="v4.7.0", tofile='v4.8.0')
    differ = d.Differ()
    diff_lines = differ.compare(f1_lines, f2_lines)

    # Separate changes into groups
    deleted = []
    added = []
    actual_d = []   # the actual deleted list
    actual_a = []   # the actual added list
    changed = []    # derived from actual_a and actual_d

    for line in diff_lines:
        if re.match('-.+', line) and (not re.match("---.+", line)):
            deleted.append(line[2:])

        if re.match('\+.+', line) and (not re.match('\+\+\+.+', line)):
            added.append(line[2:])

    # Compare deleted with added to get actual lists of deleted and added
    diff_lines = differ.compare(deleted, added)
    for line in diff_lines:
        if re.match('-.+', line) and (not re.match("---.+", line)):
            actual_d.append(line[2:])

        if re.match('\+.+', line) and (not re.match('\+\+\+.+', line)):
            actual_a.append(line[2:])

    # Compare actual added list to actual deleted list to get changed list
    for line_a in actual_a:

        lineParts_a = line_a.split()
        class_name_a = ''
        method_a = ''

        if len(lineParts_a) > 0:
            if not (re.match('  -.+', line_a) or re.match('  \+.+', line_a)):
                class_name_a = lineParts_a[0]
            elif re.match('  -.+', line_a):
                method_a = line_a.split("-")[1]
                method_a = method_a.split("(")[0]
            else:
                method_a = line_a.split("+")[1]
                method_a = method_a.split("(")[0]


        for line_b in actual_d:

            lineParts_b = line_b.split()
            class_name_b = ''
            method_b = ''

            if not (re.match('  -.+', line_b) or re.match('  \+.+', line_b)):
                class_name_b = lineParts_b[0]
            elif re.match('  -.+', line_b):
                method_b = line_b.split("-")[1]
                method_b = method_b.split("(")[0]
            elif re.match('  \+.+', line_b):
                method_b = line_b.split("+")[1]
                method_b = method_b.split("(")[0]

            if class_name_a == class_name_b and class_name_a != '':
                changed.append(line_b + ' -> ' + line_a)
                actual_a.remove(line_a)
                actual_d.remove(line_b)

            if method_a == method_b and method_a != '' and line_a != line_b:
                changed.append(line_b + ' -> ' + line_a)
                if line_a in actual_a:
                    actual_a.remove(line_a)
                if line_b in actual_d:
                    actual_d.remove(line_b)

    # Write the result to file
    with open("changes.txt", 'w') as output:

        # Remove duplicated
        actual_d = list(dict.fromkeys(actual_d))
        actual_a = list(dict.fromkeys(actual_a))
        changed = list(dict.fromkeys(changed))

        output.write("Removed:\n")
        for line in actual_d:
            output.write(line)

        output.write("\nNewly Added:\n")
        for line in actual_a:
            output.write(line)

        output.write("\nChanged:\n")
        for line in changed:
            output.write(line)