import base64
import os
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

class FileHandler:
    def get_old_key(self, hand_data, file_name):
        salt = self.get_salt(file_name)
        key = self.derive_key(hand_data, salt)
        return key

    def create_key(self, hand_data):
        salt = os.urandom(16)
        key = self.derive_key(hand_data, salt)
        self.create_salt_file(salt)
        return key

    @staticmethod
    def create_salt_file(salt):
        with open("important.salt","x") as f:
            try:
                f.write(str(salt))
            except FileExistsError:
                print("this file already exists. Please delete before you continue encryption")
            except OSError:
                print("You have an OS issue")
            finally:
                f.close()

    @staticmethod
    def get_salt(file_name):
        with open(file_name, "r") as f:
            try:
                file_data = f.read()
            except FileNotFoundError:
                print("we could not find this file")
            except EOFError:
                print("no data is in this file")
            except BufferError:
                print("You have a buffer problem")
            except ImportError:
                print("You have a import error")
            else:
                salt = file_data.encode("utf-8")
                return salt
            finally:
                f.close()

    @staticmethod
    def derive_key(hand_data, salt):
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=1,
            lanes=4,
            memory_cost=2 ** 21
        )
        key = base64.urlsafe_b64encode(kdf.derive(hand_data.encode("utf-8")))
        return key

    def encrypt(self, file_name, hand_data):
        with open(file_name, "r") as f:
            try:
                file_data = f.read()
            except FileNotFoundError:
                print("we could not find this file")
            except EOFError:
                print("no data is in this file")
            except BufferError:
                print("You have a buffer problem")
            except ImportError:
                print("You have a import error")
            else:
                encryption_stuff = Fernet(self.create_key(hand_data))
                data = encryption_stuff.encrypt(file_data.encode("utf-8"))
                f.close()
                return data

    def decrypt(self, hand_file, hand_data, salt_file):
        with open(hand_file, "r") as f:
            try:
                wanted_return_data = f.read()
            except FileNotFoundError:
                print("we could not find this file")
            except EOFError:
                print("no data is in this file")
            except BufferError:
                print("You have a buffer problem")
            except ImportError:
                print("You have a import error")
            else:
                salt = self.get_salt(salt_file)
                decryption_stuff = Fernet(self.get_old_key(hand_data,salt))
                data = None
                try:
                    data = decryption_stuff.decrypt(wanted_return_data.encode("utf-8"))
                except cryptography.fernet.InvalidToken:
                    print("wrong password")
                except TypeError:
                    print("wrong type used for password")
                f.close()
                return data
