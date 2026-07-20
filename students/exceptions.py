class InvalidMarksException(Exception):
    """
    Custom exception raised when student marks are invalid.
    """

    def __init__(self, message="Marks must be between 0 and 100."):
        self.message = message
        super().__init__(self.message)


def validate_marks(*marks):
    """
    Validate one or more subject marks.

    Raises:
        InvalidMarksException:
            If any mark is not a number or is outside 0-100.
    """

    for mark in marks:

        # Check numeric type
        if not isinstance(mark, (int, float)):
            raise InvalidMarksException(
                f"Invalid value '{mark}'. Marks must be numeric."
            )

        # Check range
        if mark < 0 or mark > 100:
            raise InvalidMarksException(
                f"Invalid marks ({mark}). Marks should be between 0 and 100."
            )

    return True