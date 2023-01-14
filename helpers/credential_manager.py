from datetime import datetime
from string import ascii_letters
import time
import hmac
import json
from os.path import exists
import os
import pwd
from stat import *

# Relative imports break when running the file directly
try:
    from . import cryptography
except ImportError:
    import cryptography

class CredentialSecurity:

    def hash(self, username: str, password: str) -> str:
        hmac_data = hmac.new(bytes(password, 'utf-8'),
                             bytes(username, 'utf-8'), 'sha512').hexdigest()

        return {'username': username, 'password': hmac_data}

    def decrypt(self, data: str, password: str) -> dict:
        decrypted = cryptography.Decryption(bytes(data, 'utf-8'), password).decrypt()

        return decrypted
                

class CredentialCache:

    def __init__(self, force_new_cache: bool = False) -> None:
        self.force_new_cache = force_new_cache

    def check_validity(self, str = ".cache") -> bool:
        """
        Checks the time difference between current UNIX epoch and the timestamp in the cache file
        """
        cache_data = self.read_cache(str)
        time_since_epoch = time.mktime(datetime.now().timetuple())
        if cache_data == None or cache_data == False:
            return False
        else:
            difference = time_since_epoch - float(cache_data['timestamp']) # time difference in seconds
            if difference >= 86400: # 24hrs in seconds
                print(f'Difference in hours is: ~{round(difference/3600)}\nDifference in seconds is: {round(difference)}')
                return False
            else:
                return True

    def read_cache(self, path: str = ".cache") -> dict | bool | None:
        """
        Reads the cache file and parses the JSON-formatted contents
        """
        cache_present = exists(path)

        if cache_present:
            try:
                with open(path, 'r') as cache_file:
                    try:
                        cache_data = json.loads(cache_file.read())
                    except json.JSONDecodeError as ex:
                        print(f"Unable to parse the cache file: {ex}")
                return cache_data
            except OSError as ex:
                print(f"Unable to open the cache file for reading: {ex}")
        elif self.force_new_cache:
            return False
        else:
            return None

    def __set_file_perms(self, str = ".cache") -> None:
        """
        Reads the cache file permissions and changes them if necessary
        """
        mode = os.stat(str)
        uid = pwd.getpwnam(os.getenv('USER')).pw_uid
        gid = pwd.getpwnam(os.getenv('USER')).pw_gid

        if mode.st_uid != uid:
            os.chown(path = str, uid = pwd.getpwnam(os.getenv('USER')).pw_uid)
        
        if mode.st_gid != gid:
            os.chown(path = str, gid = pwd.getpwnam(os.getenv('USER')).pw_gid)

        if mode.st_mode & S_IRGRP == 0 and mode.st_mode & S_IROTH == 0:
            if mode.st_mode & S_IWUSR <= 0 and mode.st_mode & S_IRUSR <= 0:
                os.chmod(str, S_IWUSR + S_IRUSR) # OWN:RW-, GRP:---, OTH:---
        else:
            os.chmod(str, S_IWUSR + S_IRUSR) # OWN:RW-, GRP:---, OTH:---

    def write_cache(self, data: dict, path: str = ".cache") -> None | bool:
        """
        Writes data to the cache file if appropriate and sets file permissions.
        NOTE: You must check if the cache is valid before calling ``write_cache()``
        as this function will not perform any validity checks.
        """
        cache_present = exists(path)

        if cache_present and not self.force_new_cache:
            return False
        else:
            with open(path, 'x') as cache_file:
                if type(data) != dict:
                    raise ValueError(
                        f'Cannot serialise data of type {type(data)} to JSON')
                else:
                    print(json.dumps(data))
                    cache_file.write(json.dumps(data))
                cache_file.close()
                self.__set_file_perms(str) # Check and set file perms after writing
                

cs = CredentialSecurity()
print(cs.hash('david', 'DXuU9txyqvo0b3f3X0CXUvFHnE980SK9'))

cache = CredentialCache(False)
cache.write_cache({'timestamp': time.mktime(datetime.now().timetuple()), 'uid': 10})
print(cache.check_validity())
