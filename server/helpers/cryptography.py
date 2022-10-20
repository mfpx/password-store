from Crypto.Cipher import AES
from base64 import b64decode, b64encode


class Encryption:

    def __init__(self, data: bytes, password: str) -> None:
        self.data = data
        self.password = password.encode('utf-8')

    def encrypt(self) -> dict:
        if type(self.data) != bytes:
            raise ValueError(
                f'Data must be of type bytes, but it is of type {type(self.data)}')
        elif type(self.password) != bytes:
            raise ValueError(
                f'Password must be of type bytes, but it is of type {type(self.password)}')
        else:
            first_pass = self.__eax_encrypt(self.data, self.password)
            return first_pass

    def __eax_encrypt(self, data: bytes, key: bytes, header: bytes = b'eax_first_pass') -> dict:
        if len(key) != 32:
            raise ValueError(
                f'Expected key to be 32 bytes, got {len(key)} bytes')
        else:
            cipher = AES.new(key, AES.MODE_EAX)
            cipher.update(header)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            return {'ciphertext': b64encode(ciphertext).decode('utf-8'),
                    'tag': b64encode(tag).decode('utf-8'),
                    'nonce': b64encode(cipher.nonce).decode('utf-8'),
                    'header': b64encode(header).decode('utf-8')}


enc = Encryption(b'helloworld', 'DXuU9txyqvo0b3f3X0CXUvFHnE980SK9')
encrypted = enc.encrypt()
print(encrypted)


class Decryption:

    def __init__(self, data: dict, password: str) -> None:
        self.data = data
        self.password = password.encode('utf-8')

    def decrypt(self):
        if type(self.data) != dict:
            raise ValueError(
                f'Data must be of type dict, but it is of type {type(self.data)}')
        elif type(self.password) != bytes:
            raise ValueError(
                f'Password must be of type bytes, but it is of type {type(self.password)}')
        else:
            first_pass = self.__eax_decrypt(
                self.data, self.password)
            return first_pass

    def __eax_decrypt(self, data: bytes, key: bytes) -> bytes:
        if len(key) != 32:
            raise ValueError(
                f'Expected key to be 32 bytes, got {len(key)} bytes')
        else:
            try:
                cipher = AES.new(key, AES.MODE_EAX, nonce=b64decode(data['nonce']))
                cipher.update(b64decode(data['header']))
                return cipher.decrypt_and_verify(b64decode(data['ciphertext']), b64decode(data['tag']))
            except Exception as ex:
                print(f'Decryption failed: {ex}. This is likely due to an incorrect password')


dec = Decryption(encrypted, 'DXuU9txyqvo0b3f3X0CXUvFHnE980SK9')
print(dec.decrypt())
