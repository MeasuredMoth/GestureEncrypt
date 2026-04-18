import base64
import os

import cryptography
from cryptography.fernet import Fernet


class FileHandler:

    def getKey(self, handData):
        byteData = handData.encode("utf-8")
        if byteData:
            byteData = byteData.ljust(32, b'\0')
        key = base64.urlsafe_b64encode(byteData)
        return key

    def encrypt(self, fileName, handData):
        with open(fileName, "r") as f:
            try:
                fileData = f.read()
            except FileNotFoundError:
                print("we could not find this file")
            except EOFError:
                print("no data is in this file")
            except BufferError:
                print("You have a buffer problem")
            except ImportError:
                print("You have a import error")
            else:
                encryptionStuff = Fernet(self.getKey(handData))
                data = encryptionStuff.encrypt(fileData.encode("utf-8"))
                f.close()
                return data

    def decrypt(self, fileName, handData):
        with open(fileName, "r") as f:
            try:
                fileData = f.read()
            except FileNotFoundError:
                print("we could not find this file")
            except EOFError:
                print("no data is in this file")
            except BufferError:
                print("You have a buffer problem")
            except ImportError:
                print("You have a import error")
            else:
                decryptionStuff = Fernet(self.getKey(handData))
                try:
                    data = decryptionStuff.decrypt(fileData.encode("utf-8"))
                except cryptography.fernet.InvalidToken:
                    print("wrong password")
                except TypeError:
                    print("wrong type used for password")
                f.close()
                return data
