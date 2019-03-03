OFFSET = 127462 - ord('A')


def flag(code):
    """
    :param code: 2 letter country code: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    :return: emoji country flag
    """
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)
