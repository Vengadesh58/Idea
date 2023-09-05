def analyze(numbers):
    result = []
    index = {}
    min = None
    max = None
    for n in numbers:
        index[n] = True
        if not max or n > max:
            max = n
        elif not min or n < min:
            min = n
    for n in range(min + 1, max):
        if not n in index.keys():
            result.append(n)
    return result


analyze([1,2,3,7])
