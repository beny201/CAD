def compute_depth(n):
    i = 1
    container = []
    while len(container) <= 9:
        first = n*i
        second = list(str(first))
        for x in second:
            if x not in container:
                container.append(x)
        i += 1
    return i

list("42")


print(compute_depth(2))

y = [0,1,2,3,4,5,6,7,8,9]

len(y)