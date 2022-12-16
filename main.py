import re
if __name__ == '__main__':
    s = "+ logStrategy(LogStrategy) Builder"
    # ss = s.split('+')
    s1 = s.split("+")[1]
    s2 = s1.split("(")[0]
    print(s.split(" "))
    print(s2)