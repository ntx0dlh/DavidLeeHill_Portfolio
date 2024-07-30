"""
This coding puzzle was given to me by HackerRank.  The request is to simply write a function that can add to strings
or numbers.  Simple conversion to int of float would result in points off, because it has to be able to add very
large numbers.
"""
import re


def padZeroes(int1: str, int2: str, leftOrRight:str="l"):
    """
    This function pads two number strings, so that they are the same length on either side of the decimal, if a decimal
    exists.  It assumes that the left or right of the decimal will be passed separately, and will pad zeroes based on
    the users request.
    :param int1: First string number to add
    :param int2: Second string number to add
    :param leftOrRight: This is where the user specifies whether to pad left ot right.
    :return: Returns 2 strings.  One will always be the original number that was passed.  The other will be a number
    padded left or right with zeroes.
    """
    om = max(len(int1), len(int2))
    pad = "0" * om
    if leftOrRight == "l":
        left = pad
        right = ""
        From = -om
        To = None
    else:
        left = ""
        right = pad
        From = 0
        To = om
    if len(int1) > len(int2):
        int2 = (left + int2 + right)[From:To]
    elif len(int2) > len(int1):
        int1 = (left + int1 + right)[From:To]
    return int1, int2


def main(string1: str, string2: str):
    """
    This function adds two string numbers.
    :param string1: First string number to add
    :param string2: Second string number to add
    :return: Returns a new number that is the sum of the provided values.  Trailing zeroes will be trimmed, after the
    decimal.  The decimal will be trimmed if there are only zeroes, or of there is nothing after it.
    """
    # Test for non-numbers
    if re.search("[^0-9.]", string1):
        raise ValueError("String1 is not a number.  Number must contain all numerical digits (0-9).")
    if re.search("[^0-9.]", string2):
        raise ValueError("String2 is not a number.  Number must contain all numerical digits (0-9).")

    # Add decimals if they are not there.
    if '.' not in string1:
        string1 += "."
    if '.' not in string2:
        string2 += "."

    # SPlit the numbers into left and right sides of the decimal point.
    num1 = string1.split('.')
    num2 = string2.split('.')
    int1 = num1[0]
    int2 = num2[0]
    dec1 = num1[1]
    dec2 = num2[1]

    # Pad numbers on left and right sides of decimal
    dec1, dec2 = padZeroes(dec1, dec2, 'r')
    print(f"dec1: {dec1}, dec2: {dec2}")
    int1, int2 = padZeroes(int1, int2)
    print(f"int1: {int1}, int2: {int2}")

    # put the padded numbers back together, and reverse them.
    s1 = (int1 + '.' + dec1)[::-1]
    s2 = (int2 + '.' + dec2)[::-1]

    # Start doing some math.
    carryover = 0
    result = ""
    for i, j in zip(s1, s2):
        if i == '.':  # Decimal should be in the same place for both, so only need to test 1
            result = "." + result
        else:
            item = str(carryover + int(i) + int(j))
            result = item[-1] + result
            if len(item) > 1:
                carryover = int(item[0])
            else:
                carryover = 0
    if carryover != 0:
        result = str(carryover) + result

    # Clean up, and simplify.
    if result[-1] == ".":
        result = result[:-1]
    while (result[-1] == "0" or result [-1] == ".") and '.' in result:
        result = result[:-1]
    print(result)
    return result


def test_main():
    """
    Various tests to make sure the function is working.
    """
    assert main("1.0", "2") == "3", "Test case 1 failed."  # Decimal and no decimal
    assert main("16516134316749.5143736450", "13151358.918198") == "16516147468108.432571645", "Test case 2 failed."  # Big numbers
    assert main("5", "5") == "10", "Test case 3 failed"  # No decimals, result ends in zero
    assert main("19.305", "4.2") == "23.505", "Test case 4 failed."  # Decimals of different lenghts
    assert main("14.24", "19.64") == "33.88", "Test case 5 failed."  # Same length decimals
    assert main("5", "0.0") == "5", "Test case 6 failed."  # addition of zero with zero decimal
    assert main("0", "4") == "4", "Test case 7 failed."  # addition of zero in first string, no decimal
    try:
        main("1a.43", "17.3")
    except ValueError as e:
        assert str(e) == "String1 is not a number.  Number must contain all numerical digits (0-9).", "Test 8 succeeded.  It returned an error, as it should."
    else:
        assert False, "Test 8 failed, because an error was not raised."

if __name__ == "__main__":
    str1 = "1.0"
    str2 = "2"
    result = main(str1, str2)
    print(result + "\n")
    test_main()
