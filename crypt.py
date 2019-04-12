import sys
import redis
import base64

class Crypt:
    def __init__(self,hash):
        self._initialize_redis_connection()
        self._setHash(hash)
    def _initialize_redis_connection(self):
        try:
            self.redis = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True, db=0)
        except:
            print("START REDIS LOCAL SERVER FIRST")
            sys.exit(1)
    def _encrypt(self,value):
        encoded_chars = []
        for i in range(len(value)):
            key_c = self.hash[i % len(self.hash)]
            encoded_c = chr(ord(value[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        encoded_string = base64.urlsafe_b64encode(encoded_string.encode('latin')).decode()
        return encoded_string
    def _decrypt(self,value):
        value = base64.urlsafe_b64decode(value)
        value = value.decode('latin')
        encoded_chars = []
        for i in range(len(value)):
            key_c = self.hash[i % len(self.hash)]
            encoded_c = chr((ord(value[i]) - ord(key_c) + 256) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        return encoded_string
    def _setHash(self,new_hash):
        self.hash = str(new_hash)
    def _validate(self,key):
        value = self._decrypt(self._get(key))
        return (self.hash == value[0:len(self.hash)]) 
    def _get(self,key):
        if(self.redis.exists(key)):
            return self.redis.get(key)
        else:
            print("KEY DOESN'T EXIST\n")
            sys.exit(1)
    def add(self,key,value):
        value = self.hash + value
        result = self.redis.set(key,self._encrypt(value))
        return result
    def get(self,key):
        value = self._decrypt(self._get(key))
        value = value[len(self.hash):]
        print(value)
        return value
    #def getAllKeys(self)
    #def updateKey(self)
    #def deleteKey(self)
    #def exportData(self)
    #def importData(self)
    

crypt = Crypt(123)

#encrypted_value = crypt._encrypt('something')
#print(encrypted_value)
#crypt._setHash(123)
#decrypted_value = crypt._decrypt(encrypted_value)
#print(decrypted_value)

#crypt.add('uat-pass','76654534g3')
#crypt._setHash(123)
#print(crypt.get('uat-pass'))