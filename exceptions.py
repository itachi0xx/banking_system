class BankingError(Exception):
    pass


class ValidationError(BankingError):
    pass


class DuplicateCustomerError(BankingError):
    pass


class CustomerNotFoundError(BankingError):
    pass
