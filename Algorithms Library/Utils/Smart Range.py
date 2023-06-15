def srange(*args: list[int]): # returns a generator

    """
    smart range function that supports negative and float steps
    if start is larger or more positive than stop, then step will automatically be negated
    float steps work intuitively as one would expect

    all input arguments should be integers and floats
    however if a type mismatch happens, the function will try to convert unknown type into float or int
    examples of such include an int/float in string, Decimal class, etc.

    the default value for start is 0, and for step is 1 (or -1 if start > stop)
    all values are rounded to 10 decimal places to avoid float precision error
    error feedbacks are 1-indexed, meaning that argument 1 refers to the first argument
    """

    l = len(args)

    args = list(args)

    for i in range(l):
        t = type(args[i])
        if t != int and t != float:
            try: # try to convert unknown argument type into floats, then ints if applicable
                args[i] = float(args[i])
                if args[i] % 1 == 0:
                    args[i] = int(args[i])
            except Exception:
                raise ValueError(f"srange argument {i+1} must be of type int or float, not {t}")

    if l == 1: # srange(stop)
        start = 0
        stop = args[0]
        step = 1
    elif l == 2: # srange(start, stop)
        start = args[0]
        stop = args[1]
        step = 1
    elif l == 3: # srange(start, stop, step)
        start = args[0]
        stop = args[1]
        if args[2] != 0:
            step = args[2]
        else:
            raise ValueError("srange arg 3 must not be zero")
    else:
        raise Exception(f"srange expected at most 3 arguments, got {l}")
    
    # at this point, start, stop, step are all defined

    if start > stop:
        if step > 0:
            step = -step
            
    current_value = start

    if start < stop:
        while current_value < stop:
            yield current_value
            current_value = round(current_value + step, 10)
    else:
        while current_value > stop:
            yield current_value
            current_value = round(current_value + step, 10)


if __name__ == "__main__":

    # Regular use cases
    print(list(srange(-10)))
    print(list(srange(5, -5)))
    print(list(srange(1, 10, 0.5)))
    print(list(srange(-10, -100, 10)))

    # Exception cases
    print(list(srange(0, "-10", 2)))
    print(list(srange("1", 9, "0.3")))
    from decimal import Decimal
    print(list(srange("1", 5, Decimal(0.33))))

    # Error cases
    # print(list(srange("k")))