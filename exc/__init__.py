class CustomValidationError(Exception):
    def __init__(self, message="Custom Validation Error"):
        self.message = message
        super().__init__(self.message)


class ConstraintsError(Exception):
    def __init__(self, message="Constrain message"):
        self.message = message
        super().__init__(self.message)


class PriceConstrainError(ConstraintsError):
    def __init__(self, message="Price can only be positive number"):
        self.message = message
        super().__init__(self.message)

class DividendAmountConstrainError(ConstraintsError):
    def __init__(self, message="Constrain message"):
        self.message = message
        super().__init__(self.message)

class ParValueConstrainError(ConstraintsError):
    def __init__(self, message="Constrain message"):
        self.message = message
        super().__init__(self.message)

