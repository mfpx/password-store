import sys
from time import sleep
from typing import Any, Callable
from helpers import credential_manager
import querylib
import hmac
from tabulate import tabulate
from getpass import GetPassWarning, getpass
from os import system, name


class Options:

    def call_selection(self, opt: str | int, args: Any = None) -> Callable:
        option = f'menu_item_{opt}'
        func = type(self).__dict__.get(option)
        if hasattr(func, '__call__'):
            return func(self, args)  # type: ignore

        raise ValueError(f'Unknown class function {opt}')


class Menu(Options):

    def __init__(self) -> None:
        self.username = None
        self.password = None

        self.clear()
        print("Welcome, please login\n")
        while not self.username:
            self.username = input("Username: ")
        while not self.password:
            try:
                self.password = getpass("Password: ")
            except GetPassWarning as gpw:
                print(
                    f"WARNING: getpass module returned: {gpw}\nPassword input will be done in CLEARTEXT!")
                self.password = input("Password: ")

        hmac_pwd = hmac.new(bytes(self.password, 'utf-8'),
                            bytes(self.username, 'utf-8'), 'sha512').hexdigest()
        # note: create a hmac with username as the message and password as password; use mysql PASSWORD() to hash it
        # hash of choice is sha512
        login_result = self.__login(
            {'username': self.username, 'password': hmac_pwd})
        if login_result == False:
            self.__init__()
        else:
            print(login_result)

    def clear(self) -> None:
        if name == 'nt':  # win nt
            system('cls')
        else:  # posix-compliant systems
            system('clear')

    def menu_item_1(self, username: str):
        creds = querylib.Credentials(username)
        print(creds.get())

    def menu(self) -> None:
        self.clear()
        print("Welcome!\nPlease select an option\n")
        print("1. Show credentials\n2. Manage credentials\n3. Logout")
        choice = input("> ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice")
            sleep(2)
            self.menu()
        elif choice == '3':
            sys.exit(0)
        else:
            print(self.username)
            self.call_selection(choice, self.username)

    def __login(self, credentials: dict) -> bool | tuple:
        lc = querylib.Login(credentials['username'], credentials['password'])
        res = lc.authenticate()
        if len(res) == 0:
            return False
        else:
            return res


menu = Menu()
menu.menu()
