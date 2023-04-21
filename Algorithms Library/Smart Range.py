# smart range function that automatically negates the step argument when start is more positive than stop
def srange(*args: list[int]):
    l = len(args)
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
            raise ValueError("srange() arg 3 must not be zero")
    else:
        raise TypeError(f"srange expected at most 3 arguments, got {l}")

    if start > stop:
        if step > 0:
            return range(start, stop, -step)
        return range(start, stop, step)
    return range(start, stop, step)