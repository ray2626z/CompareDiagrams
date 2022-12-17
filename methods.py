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
    name = method.split('(')[0]
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
                current_methods = []

        current_class = ''
        current_methods = []
        for line in f2_lines:
            if class_begin(line):
                current_class = c_name(line)
            elif is_method(line):
                current_methods.append(line[2:])
            elif class_end(line):
                classes2.update({current_class: current_methods})
                current_methods = []

    # print(classes1)
    # print(classes2)

    # Identify newly added classes
    new_classes = []
    for i in classes2.keys():
        if i not in classes1.keys():
            new_classes.append(i)
    # print(new_classes)

    # Identify removed classes
    rm_classes = []
    for i in classes1.keys():
        if i not in classes2.keys():
            rm_classes.append(i)
    # print(rm_classes)

    # Identify altered classes
    alt_classes = []
    for i in classes1.keys():
        if i in classes2.keys():
            methods_1 = classes1.get(i)
            methods_2 = classes2.get(i)
            if methods_1 != methods_2:
                alt_classes.append(i)
    # print(alt_classes)

    # Identify altered methods for classes in alt_classes
    alt_class_methods = dict()
    for key in alt_classes:

        # initialize
        methods_1 = classes1[key]
        methods_2 = classes2[key]
        exist = False
        alt_pairs = dict()

        for m1 in methods_1:
            name1 = m_name(m1)
            exist = m1 in methods_2
            # print(name1)
            for m2 in methods_2:
                name2 = m_name(m2)
                if name1 == name2 and m1 != m2 and not exist:
                    # print('Class: ' + key)
                    # print(m1 + ' -> ' + m2)
                    alt_pairs.update({m1: m2})

        alt_class_methods.update({key: alt_pairs})

    # print(alt_class_methods)

    # Identify removed methods for classes in alt_classes
    rm_class_methods = dict()
    for key in alt_classes:
        # initialize
        methods_1 = classes1[key]
        methods_2 = classes2[key]
        alt_methods = alt_class_methods[key]
        rm_methods = []

        for m in methods_1:
            if m not in methods_2 and m not in alt_methods.keys():
                rm_methods.append(m)

        rm_class_methods.update({key: rm_methods})

    # print(rm_class_methods)


