class RepositoryException(Exception):
    """Базавая ошибка репозиториев"""


class WalletNotFoundException(RepositoryException):
    """Кошелек не найден"""


class WalletAmountException(RepositoryException):
    """Недостаточно средств"""
