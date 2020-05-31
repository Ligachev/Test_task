def fibonacci():
    '''
    Build a Fibonacci sequence and
    get the sum of the even-valued terms.
    '''
    try:
        count = int(input('Enter the number of terms rom 1 to 33: '))
        if count < 1 or count > 33:
            print('You have entered incorrectly number!\nCount of terms will be equal 33')
            count = 33
    except ValueError:
        print('You have entered incorrectly value!\nCount of terms will be equal 33')
        count = 33

    num_one = num_two = 1
    fib_seq = [num_one, num_two]
    result = 0

    if count == 1:
        fib_seq = [num_one, ]

    i = 0
    while i < count - 2:
        num_three = num_one + num_two
        fib_seq.append(num_three)
        if num_three % 2 == 0:
            result += num_three
        num_one = num_two
        num_two = num_three
        i += 1

    return print(
        'Your\'s the Fibonacci sequence will be: {}\nSum of the even-valued terms is: {}'.format(fib_seq, result))


if __name__ == '__main__':
    fibonacci()
