import re


def new_dict():
    '''
    Get data from user.
    '''
    keys = without_spaces(input('Enter an arbitrary number of keys using a space as a separator: '))
    values = without_spaces(input('Enter an arbitrary number of values using a space as a separator: '))

    if len(keys) > len(values):
        values.extend([None] * (len(keys) - len(values)))

    result = create_dict(keys, values)
    # Or we simply can use the built-in zip function
    # result = dict(zip(keys, values))

    return print(result)


def create_dict(keys, values):
    '''
    Create dictionary.
    '''
    res = {}
    for i in range(len(keys)):
        try:
            res[keys[i]] = values[i]
        except StopIteration:
            res[keys[i]] = None

    return res


def without_spaces(arg):
    '''
    Remove extra whitespace.
    '''
    new_list = re.findall(r'[\w]+', arg)

    return new_list


if __name__ == '__main__':
    new_dict()
