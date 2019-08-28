__all__ = ('hello',)

from getpass import getuser


def hello():
    print(f'Hello {getuser()}!')
