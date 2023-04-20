def srange(*args):
    l = len(args)
    if l == 1:
        start = 0
        stop = args[0]
        step = 1
    elif l == 2:
        start = args[0]
        stop = args[1]
        step = 1
    elif l == 3:
        start = args[0]
        stop = args[1]
        step = args[2]
    else:
        raise TypeError(f"srange expected at most 3 arguments, got {l}")

    if start > stop:
        return range(start, stop, -step)
    return range(start, stop, step)