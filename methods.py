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


def is_dependency(l: str):
    if re.match('.+> .+', l):
        return True
    return False


if __name__ == '__main__':

    file1 = ''
    file2 = ''
    f1_lines = []
    f2_lines = []

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

        if alt_pairs != {}:
            alt_class_methods.update({key: alt_pairs})

    # print(alt_class_methods)

    # Identify removed methods for classes in alt_classes
    rm_class_methods = dict()
    for key in alt_classes:
        # initialize
        methods_1 = classes1[key]
        methods_2 = classes2[key]
        alt_methods = {}
        if key in alt_class_methods:
            alt_methods = alt_class_methods[key]
        rm_methods = []

        for m in methods_1:
            if m not in methods_2 and m not in alt_methods.keys():
                rm_methods.append(m)

        rm_class_methods.update({key: rm_methods})
    # print(rm_class_methods)

    # Identify new methods for classes in alt_classes
    new_class_methods = dict()
    for key in alt_classes:
        # initialize
        methods_1 = classes1[key]
        methods_2 = classes2[key]
        alt_methods = {}
        if key in alt_class_methods:
            alt_methods = alt_class_methods[key]
        new_methods = []

        for m in methods_2:
            if m not in methods_1 and m not in alt_methods.values():
                new_methods.append(m)

        new_class_methods.update({key: new_methods})
    # print(new_class_methods)

    # Identify dependencies for both versions
    dependencies_1 = []
    dependencies_2 = []

    for line in f1_lines:
        if is_dependency(line):
            dependencies_1.append(line)

    for line in f2_lines:
        if is_dependency(line):
            dependencies_2.append(line)
    # print(dependencies_1)
    # print(dependencies_2)

    # Identify altered dependencies
    alt_ds = dict()
    for d1 in dependencies_1:

        class1 = d1.split()[0]
        changes = []
        exist = d1 in dependencies_2

        for d2 in dependencies_2:
            class2 = d2.split()[0]
            if class1 == class2 and d1 != d2 and not exist:
                changes.append(d2)

        if changes:
            alt_ds.update({d1: changes})

    # for i in alt_ds.keys():
    #     if alt_ds[i]:
    #         print(i + ': ')
    #         print(alt_ds[i])

    # Identify removed dependencies
    rm_ds = []
    for d in dependencies_1:
        if d not in dependencies_2 and d not in alt_ds.keys():
            rm_ds.append(d)
    # print(rm_ds)

    # Identify new dependencies:
    new_ds = []
    for d in dependencies_2:
        if d not in dependencies_1 and d not in alt_ds.values():
            new_ds.append(d)
    # print(new_ds)

    # Write the results to a file
    with open("changes.txt", 'w') as output:

        # removed dependencies
        output.write("Removed dependencies:\n")
        for line in rm_ds:
            output.write(line)
        output.write('\n')

        # new dependencies
        output.write("New dependencies:\n")
        for line in new_ds:
            output.write(line)
        output.write('\n')

        # altered dependencies
        output.write("Altered dependencies:\n")
        for old in alt_ds.keys():

            output.write(old + 'has been changed to: \n')
            new_d_list = alt_ds[old]

            for new in new_d_list:
                output.write(new)
            output.write('\n')
        output.write('\n')

        # removed methods
        output.write("Removed methods:\n")
        # for removed classes
        for r in rm_classes:
            output.write(r + ': \n')
            methods = classes1[r]
            for m in methods:
                output.write(m)
        # for altered classes
        for alt in rm_class_methods.keys():
            output.write(alt + ':\n')
            methods = rm_class_methods[alt]
            for m in methods:
                output.write(m)
        output.write('\n')

        # new methods
        output.write("New methods:\n")
        # for new classes
        for n in new_classes:
            output.write(n + ':\n')
            methods = classes2[n]
            for m in methods:
                output.write(m)
            output.write('\n')
        # for altered classes
        for alt in rm_class_methods.keys():
            output.write(alt + ':\n')
            methods = new_class_methods[alt]
            for m in methods:
                output.write(m)
            output.write('\n')
        output.write('\n')

        # altered methods
        output.write("Altered methods:\n")
        for alt in alt_class_methods.keys():
            output.write(alt + ':\n')
            # olds = alt_class_methods[alt].keys()
            dicts = alt_class_methods[alt]
            for old in dicts.keys():
                output.write(old)
                output.write('has been changed to:\n')
                methods = dicts[old]
                output.write(methods)
                output.write('\n')
            # output.write('\n')
