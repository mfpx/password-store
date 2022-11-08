from datetime import datetime
from string import ascii_letters
from . import cryptography
import time
import hmac
import json
from os.path import exists
from types import NoneType


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

    def read_cache(self, path: str = ".cache") -> dict | bool | NoneType:
        cache_present = exists(path)

        if cache_present:
            with open(path, 'r') as cache_file:
                cache_data = json.loads(cache_file.read())
            return cache_data
        elif self.force_new_cache:
            return False
        else:
            return None

    def write_cache(self, data: dict, path: str = ".cache") -> None | bool:
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



cs = CredentialSecurity()
print(cs.hash('david', 'DXuU9txyqvo0b3f3X0CXUvFHnE980SK9'))

cache = CredentialCache(False)
cache.write_cache({'timestamp': time.mktime(datetime.now().timetuple()), 'uid': 10})
