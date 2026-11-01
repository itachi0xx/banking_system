class BankingError(Exception):
    pass


class ValidationError(BankingError):
    pass


class DuplicateCustomerError(BankingError):
    pass


class CustomerNotFoundError(BankingError):
    pass


class AccountNotFoundError(BankingError):
    pass


class AccountInactiveError(BankingError):
    pass


class InvalidAmountError(BankingError):
    pass


class InsufficientAmountError(BankingError):
    pass


class SameAccountError(BankingError):
    pass


class InvalidTransactionError(BankingError):
    pass
