import sys
import re


def class_begin(l: str):
    if re.match('class .+', l):  # match is not boolean
        return True
    return False


def class_end(l: str):
    if re.match('}', l):
        return True
    return False


def is_method(l: str):
    if re.match('  \+.+', l) or re.match('  -.+', l):
        return True
    return False


def c_name(l: str):
    return l.split()[1]


def m_name(l: str):
    parts = l.split()
    method = parts[1]
    name = method.split('1')[0]
    return name


if __name__ == '__main__':

    file1 = ''
    file2 = ''

    # Use dictionary to record methods for each class
    classes1 = dict()
    classes2 = dict()

    if len(sys.argv) != 3:
        print("Usage: python3 compare.py <diagram1> <diagram2>")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]

    # Populate classes and methods for both dictionaries
    # Open class diagram flies (format: mermaid.md)
    with open(file1) as f1, open(file2) as f2:
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

        current_class = ''
        current_methods = []
        for line in f1_lines:
            if class_begin(line):
                current_class = c_name(line)
            elif is_method(line):
                current_methods.append(line[2:])
            elif class_end(line):
                classes1.update({current_class: current_methods})

        current_class = ''
        current_methods = []
        for line in f2_lines:
            if class_begin(line):
                current_class = c_name(line)
            elif is_method(line):
                current_methods.append(line[2:])
            elif class_end(line):
                classes2.update({current_class: current_methods})

    # print(classes1)
    # print(classes2)

    # Determine newly added classes
    for i in classes2.keys():
        if
