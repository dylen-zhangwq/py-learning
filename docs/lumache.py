def get_random_ingredients():
    """
    Return a list of random ingredients as strings.

    :raise lumache.InvalidKindError: If the kind is invalid.
    :return: The ingredients list.
    :rtype: list[str]

    """
    return ["shells", "gorgonzola", "parsley"]


class InvalidKindError(Exception):
    """Raised if the kind is invalid."""

    pass
