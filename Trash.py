def stray(arr):
    first = []
    second = []
    for x in arr:
        if x not in first:
            first.append(x)
        else:
            second.append(x)
    value = [y for y in first if y not in second]
    return value 
                

z =[2, 3, 2, 2, 2]

print(stray(z))