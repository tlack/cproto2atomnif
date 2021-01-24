from src import parser as c2n

def compare_list(value, expected):
    print('compare_list', value, expected)
    for i, x in enumerate(expected):
        if not compare(value[i], x):
            return False
    return True

def compare_dict(value, expected):
    print('compare_dict')
    for k, v in expected.items():
        if type(v) is dict:
            if not compare_dict(value[k], v):
                return False
        else:
            if not compare(value[k], v):
                print(k, v, value[k], 'differs')
                return False
    return True

def compare(value, expected):
    passed = False
    if type(value) is list and type(expected) is list:
        passed = compare_list(value, expected)
    elif type(value) is dict and type(expected) is dict:
        # for dictionaries, we only want to match the fields supplied in
        # the expected value. easier on the coder.
        passed = compare_dict(value, expected)
    else:
        print(value,expected)
        passed = value == expected
    return passed

def test(msg, value, expected):
    passed = compare(value, expected)
    if not passed:
        print('TEST FAILED! ', msg)
    else:
        print('test ok: ', msg)

def run_tests():

    a = c2n.parse_line(0, 'void nothing()', 'test');
    b = {'func': 'nothing', 'returns': 'void', 'args': []};
    test('1', a, b)

    a = c2n.parse_line(0, 'char nothing()', 'test');
    b = {'func': 'nothing', 'returns': 'char', 'args': []};
    test('2', a, b)

    a = c2n.parse_line(0, 'wchar_t nothing()', 'test');
    b = {'func': 'nothing', 'returns': 'wchar_t', 'args': []};
    test('2 underscores', a, b)

    a = c2n.parse_line(0, 'char nothing(int a)', 'test');
    b = {'func': 'nothing', 'returns': 'char', 'args': [
        {'type': 'int', 'argname': 'a', 'access': None, 'modifiers': None}
    ]};
    test('3', a, b)

    a = c2n.parse_line(0, 'char nothing(int a, int zzz_32)', 'test');
    b = {'func': 'nothing', 'returns': 'char', 'args': [
        {'type': 'int', 'argname': 'a', 'access': None, 'modifiers': None},
        {'type': 'int', 'argname': 'zzz_32', 'access': None, 'modifiers': None}
    ]};
    test('3-2', a, b)

    a = c2n.parse_line(0, 'char* nothing(int a)', 'test');
    b = {'func': 'nothing', 'returns': 'char*', 'args': [
        {'type': 'int', 'argname': 'a', 'access': None, 'modifiers': None}
    ]};
    test('4', a, b)

    a = c2n.parse_line(0, 'char* nothing(int* a)', 'test');
    b = {'func': 'nothing', 'returns': 'char*', 'args': [
        {'type': 'int*', 'argname': 'a', 'access': None, 'modifiers': None}
    ]};
    test('5', a, b)

    a = c2n.parse_line(0, 'char* M5.Blah.nothing(int* a)', 'test');
    b = {'func': 'M5.Blah.nothing', 'returns': 'char*', 'args': [
        {'type': 'int*', 'argname': 'a', 'access': None, 'modifiers': None}
    ]};
    test('6', a, b)

    a = c2n.parse_line(0, 'static char* M5.Blah.nothing(int* a)', 'test');
    b = {'func': 'M5.Blah.nothing', 'returns': 'static char*', 'args': [
        {'type': 'int*', 'argname': 'a', 'access': None, 'modifiers': None}
    ]};
    test('7 storage modifier', a, b)

    a = c2n.parse_line(0, 'static char* M5.Blah.nothing(int a[])', 'test');
    b = {'func': 'M5.Blah.nothing', 'returns': 'static char*', 'args': [
        {'type': 'int', 'argname': 'a', 'modifiers': '[]'}
    ]};
    test('8', a, b)

def main():
    run_tests()

main()
