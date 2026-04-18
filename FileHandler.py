import cryptography
from cryptography.fernet import Fernet

class FileHandler:
    def __init__(self, file, key,token):
        self.files = file
        self.key = key
        self.token = token

    def createKeyPair(self):
        key = Fernet.generate_key()
        self.key = key

    def giveBackData(self, file):
        with open(file, "w") as file:
            file.write(self.token)
            file.close()

    def encrypt(self, file):
        with open(file, "r") as file:
            try:
                handData = file.read()
            except FileNotFoundError:
                print("we could not find this file")
            except EOFError:
                print("no data is in this file")
            except BufferError:
                print("You have a buffer problem")
            except ImportError:
                print("You have a import error")
            else:
                encryptionStuff = Fernet(self.key)
                self.token = encryptionStuff.encrypt(handData)
                self.giveBackData(self, file)
            finally:
                file.close()
    def decrypt(self, file):
        with open(file, "r") as file:
            try:
                handData = file.read()
            except FileNotFoundError:
                print("we could not find this file")
            except EOFError:
                print("no data is in this file")
            except BufferError:
                print("You have a buffer problem")
            except ImportError:
                print("You have a import error")
            else:
                decryptionStuff = Fernet(self.key)
                self.token = decryptionStuff.decrypt(handData)
                self.giveBackData(self,file)
            finally:
                file.close()
