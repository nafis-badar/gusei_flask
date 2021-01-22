import onetimepad

class Crypt:
    def encrypt(self, password):
        try:
            return onetimepad.encrypt(password, 'random')
        except Exception as ex:
            print(ex)
    def decrypt(self, cipher):
        try:
           return onetimepad.decrypt(cipher, 'random')
        except Exception as ex:
            print(ex)