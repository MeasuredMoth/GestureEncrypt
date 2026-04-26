import base64
import os
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

class FileHandler:
    def getOldKey(self, handData, salt):
        key = self.deriveKey(handData, salt)
        return key

    def createKey(self, handData):
        salt = os.urandom(16)
        key = self.deriveKey(handData, salt)
        self.createSaltFile(salt)
        return key

    @staticmethod
    def createSaltFile(salt):
        try:
            with open("important.salt","xb") as f:
                f.write(salt)
        except FileExistsError:
            data = input("do you want to overwrite this file? Y or N: ")
            if data == "Y":
                try:
                    with open("important.salt","wb") as f:
                        f.write(salt)
                except FileNotFoundError:
                    print("we could not find this file")
                finally:
                    f.close()
            else:
                print("\nOkay, we did not overwrite this file")
                f.close()
        except OSError:
            print("you had an OS issue")
        finally:
                f.close()

    @staticmethod
    def getSalt(filename):
        try:
            with open(filename, "rb") as f:
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
            salt = fileData
            f.close()
            return salt
        finally:
            f.close()

    @staticmethod
    def deriveKey(handData, salt):
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=1,
            lanes=4,
            memory_cost=2 ** 21
        )
        key = base64.urlsafe_b64encode(kdf.derive(handData.encode("utf-8")))
        return key

    def encrypt(self, filename, handData):
        try:
            with open(filename, "r") as f:
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
            encryptionStuff = Fernet(self.createKey(handData))
            data = encryptionStuff.encrypt(fileData.encode("utf-8"))
            f.close()
            return data

    def decrypt(self, gestureFile, handData, saltFile):
        try:
            with open(gestureFile, "r") as f:
                wantedData = f.read()
        except FileNotFoundError:
            print("we could not find this file")
        except EOFError:
            print("no data is in this file")
        except BufferError:
            print("You have a buffer problem")
        except ImportError:
            print("You have a import error")
        else:
            f.close()
            salt = self.getSalt(saltFile)
            decryptionStuff = Fernet(self.getOldKey(handData,salt))
            try:
                data = decryptionStuff.decrypt(wantedData.encode("utf-8"))
            except cryptography.fernet.InvalidToken:
                print("wrong password")
            except TypeError:
                print("wrong type used for password")
            else:
                if data is not None:
                    stringData = data.decode("utf-8")
                    return stringData
                else:
                    return data
        finally:
            f.close()