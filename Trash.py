from math import ceil, sqrt


def even_digit_squares(a, b):

    def checking_square_each(n):
        for qty in str(n):
            if int(qty) % 2 != 0:
                return None
        return n
    # Getting the very first number
    number = ceil(sqrt(a))

    # First number's square
    n2 = number * number

    # Next number is at the difference of
    number = (number * 2) + 1
    values = []
    # While the perfect squares
    # are from the range
    while ((n2 >= a and n2 <= b)):

        values.append(n2)
        # Get the next perfect square
        n2 = n2 + number

        # Next odd number to be added
        number += 2
    cleaned_values = [x for x in values if checking_square_each(x) != None]
    return cleaned_values

print(even_digit_squares(100,1000))
