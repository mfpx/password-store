import json
from Crypto.Cipher import AES
from base64 import b64decode, b64encode


class Encryption:

    def __init__(self, data: dict, password: str) -> None:
        self.data = data
        self.password = password.encode('utf-8')

    def encrypt(self) -> dict:
        if type(self.data) != dict:
            raise ValueError(
                f'Data must be of type dict, but it is of type {type(self.data)}')
        elif type(self.password) != bytes:
            raise ValueError(
                f'Password must be of type bytes, but it is of type {type(self.password)}')
        else:
            first_pass = self.__eax_encrypt(
                self.__to_json_bytes(self.data), self.password)
            return first_pass

    def __to_json_bytes(self, data: dict) -> bytes:
        if type(data) != dict:
            raise ValueError(
                f'Expected input to be of type dict, but got {type(data)}')
        else:
            json_dict = json.dumps(data)
            encoded_bytes = b64encode(bytes(json_dict, 'utf-8'))
            return encoded_bytes

    def __eax_encrypt(self, data: bytes, key: bytes, header: bytes = b'enc_data_storage') -> dict:
        if len(key) != 32:
            raise ValueError(
                f'Expected key to be 32 bytes, got {len(key)} bytes')
        else:
            cipher = AES.new(key, AES.MODE_EAX)
            cipher.update(header)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            return self.__to_json_bytes({'ciphertext': b64encode(ciphertext).decode('utf-8'),
                    'tag': b64encode(tag).decode('utf-8'),
                    'nonce': b64encode(cipher.nonce).decode('utf-8'),
                    'header': b64encode(header).decode('utf-8')})


enc = Encryption({'hello': 'world'}, 'DXuU9txyqvo0b3f3X0CXUvFHnE980SK9')
encrypted = enc.encrypt()
print(encrypted)


class Decryption:

    def __init__(self, data: bytes, password: str) -> None:
        self.data = data
        self.password = password.encode('utf-8')

    def decrypt(self) -> dict:
        if type(self.data) != bytes:
            raise ValueError(
                f'Data must be of type bytes, but it is of type {type(self.data)}')
        elif type(self.password) != bytes:
            raise ValueError(
                f'Password must be of type bytes, but it is of type {type(self.password)}')
        else:
            first_pass = self.__eax_decrypt(
                self.__to_dict(self.data), self.password)
            return self.__to_dict(first_pass)

    def __to_dict(self, data: bytes) -> dict:
        if type(data) != bytes:
            raise ValueError(
                f'Expected input to be of type bytes, but got {type(data)}')
        else:
            json_str = b64decode(data).decode('utf-8')
            output_dict = json.loads(json_str)
            return output_dict

    def __eax_decrypt(self, data: bytes, key: bytes) -> bytes:
        if len(key) != 32:
            raise ValueError(
                f'Expected key to be 32 bytes, got {len(key)} bytes')
        else:
            try:
                cipher = AES.new(key, AES.MODE_EAX,
                                 nonce=b64decode(data['nonce']))
                cipher.update(b64decode(data['header']))
                return cipher.decrypt_and_verify(b64decode(data['ciphertext']), b64decode(data['tag']))
            except Exception as ex:
                print(
                    f'Decryption failed: {ex}. This is likely due to an incorrect password')


dec = Decryption(encrypted, 'DXuU9txyqvo0b3f3X0CXUvFHnE980SK9')
print(dec.decrypt())
