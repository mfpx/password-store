import sys
from time import sleep
from typing import Any, Callable
from helpers import credential_manager as credman
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
            return func(self, args)

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
        if name == 'nt': # windows
            system('cls')
        else: # posix-compliant systems
            system('clear')

    def menu_item_1(self, username: str):
        creds = querylib.Credentials(username)
        data = creds.get()
        decrypted = credman.CredentialSecurity().decrypt(data[0]['data'], self.password)
        print(decrypted)
        print(tabulate(decrypted, headers='keys', tablefmt='grid'))

    def menu_item_2(self, username: str):
        self.clear()
        print("1. Search credentials\n2. Add credentials\n3. Delete credentials")
        choice = input("> ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice")
            sleep(2)
        elif choice == '1':
            print("Not implemented")
            pass

    def menu_item_3(self):
        self.clear()
        print("Please select an option\n")
        print("1. Caching\n2. Main menu")
        choice = input("> ")
        if choice not in ['1']:
            print("Invalid choice")
            sleep(2)
            self.menu_item_3()
        elif choice == '2':
            self.menu()
        else:
            self.call_selection('3' + choice)

    def menu_item_31(self):
        self.clear()
        print("Please select an option\n")
        print("1. Turn on credential caching\n2. Turn off credential caching\n3. Back to settings")
        choice = input("> ")
        if choice not in ['1', '2', '3']:
            print("Invalid choice")
            sleep(2)
            self.menu_item_31()
        elif choice == '3':
            self.menu_item_3()
        else:
            self.call_selection('31' + choice)

    def menu_item_311(self):
        pass #TODO

    def menu_item_312(self):
        pass #TODO

    def menu(self) -> None:
        self.clear()
        print("Welcome!\nPlease select an option\n")
        print("1. Show credentials\n2. Manage credentials\n3. Settings\n4. Logout")
        choice = input("> ")
        if choice not in ['1', '2', '3', '4']: # ideally should enumerate all choices automatically, instead of making a list
            print("Invalid choice")
            sleep(2)
            self.menu()
        elif choice == '4':
            sys.exit(0)
        else:
            self.call_selection(choice, self.username)

    def __login(self, credentials: dict) -> bool | tuple:
        lc = querylib.Login(credentials['username'], credentials['password'])
        try:
            res = lc.authenticate()
            if len(res) == 0:
                return False
            else:
                return res
        except Exception as ex:
            print("Connection failed, see the above error message")
            sys.exit(1)


menu = Menu()
menu.menu()
