import base64

import cryptography
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, kdf
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class FileHandler:
    def __init__(self):
        self.token = ""

    def giveBackFile(self,fileName):
        newFileName = os.path.basename(fileName).split(".")[0] + ".gesture"
        with open(newFileName, "wb") as f:
            f.write(self.token)
            f.close()


    def getKey(self,handData):
        byteData = handData.encode("utf-8")
        if byteData:
            byteData = byteData.ljust(32, b'\0')
        key = base64.urlsafe_b64encode(byteData)
        return key

    def encrypt(self,fileName,handData):
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
                self.token = encryptionStuff.encrypt(fileData.encode("utf-8"))
                self.giveBackFile(fileName)
            finally:
                f.close()

    def decrypt(self,fileName,handData):
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
                    self.token = decryptionStuff.decrypt(fileData)
                except cryptography.fernet.InvalidToken:
                    print("wrong password")
                except TypeError:
                    print("wrong type used for password")
                else:
                    self.giveBackFile(fileName)
            finally:
                f.close()
