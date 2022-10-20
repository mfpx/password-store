from typing import Any, Callable
import connector
import login
import hmac
from tabulate import tabulate
from getpass import GetPassWarning, getpass


class Options:

    def call_selection(self, opt: str | int) -> Callable:
        option = f'menu_item_{opt}'
        func = type(self).__dict__.get(option)
        if hasattr(func, '__call__'):
            return func(self)  # type: ignore

        raise ValueError(f'Unknown class function {opt}')


class Menu(Options):

    def __init__(self) -> None:
        username = None
        password = None

        print("Welcome, please login\n")
        while not username:
            username = input("Username: ")
        while not password:
            try:
                password = getpass("Password: ")
            except GetPassWarning as gpw:
                print(
                    f"WARNING: getpass module returned: {gpw}\nPassword input will be done in CLEARTEXT!")
                password = input("Password: ")

        hmac_pwd = hmac.new(bytes(password, 'utf-8'),
                            bytes(username, 'utf-8'), 'sha512').hexdigest()
        # note: create a hmac with username as the message and password as password; use mysql PASSWORD() to hash it
        # hash of choice is sha512
        login_result = self.__login(
            {'username': username, 'password': hmac_pwd})
        if login_result == False:
            self.__init__()
        else:
            print(login_result)

    def menu(self) -> None:
        print("hello")

    def __login(self, credentials: dict) -> bool | tuple:
        lc = login.Login(credentials['username'], credentials['password'])
        res = lc.authenticate()
        if len(res) == 0:
            return False
        else:
            return res


menu = Menu()
menu.menu()
