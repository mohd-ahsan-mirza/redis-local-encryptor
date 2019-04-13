import sys
import redis
import base64
import inspect

class Crypt:
    def __init__(self,hash,debug=False):
        self._initialize_redis_connection()
        self._debug = debug
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
        self._print(inspect.currentframe().f_code.co_name,encoded_string)
        return encoded_string
    def _decrypt(self,value):
        value = base64.urlsafe_b64decode(value)
        value = value.decode('latin')
        encoded_chars = []
        for i in range(len(value)):
            key_c = self.hash[i % len(self.hash)]
            encoded_c = chr((ord(value[i]) - ord(key_c) + 256) % 256)
            encoded_chars.append(encoded_c)
        decoded_string = ''.join(encoded_chars)
        self._print(inspect.currentframe().f_code.co_name,decoded_string)
        return decoded_string
    def _setHash(self,new_hash):
        self.hash = str(new_hash)
        self._print(inspect.currentframe().f_code.co_name,new_hash)
    def _validate(self,key):
        value = self._decrypt(self._get(key))
        self._print(inspect.currentframe().f_code.co_name,value,"Function returns true when hash is appended to the decoded string")
        return (self.hash == value[0:len(self.hash)]) 
    def _get(self,key):
        if(self.redis.exists(key)):
            result = self.redis.get(key)
            self._print(inspect.currentframe().f_code.co_name,result)
            return result
        else:
            matching_keys = self.find_keys("*"+str(key)+"*")
            if(len(matching_keys)):
                if(len(matching_keys)) > 1:
                    self._print(inspect.currentframe().f_code.co_name,matching_keys,"TOO MANY MATCHING KEY PATTERNS\n",True)
                    sys.exit(1)
                else:
                    print("Warning!! The exact key was not found. Returning value of closest matching key:"+str(matching_keys[0]))
                    result = self.redis.get(matching_keys[0])
                    self._print(inspect.currentframe().f_code.co_name,result)
                    return result
            else:
                self._print(inspect.currentframe().f_code.co_name,key,"KEY DOESN'T EXIST\n",True)
                sys.exit(1)
    def _print(self,function_name,value,message="",force_print=False):
        if(self._debug or force_print):
            if(len(message)):
                message = ", Message -> "+message
            print("FUNCTION-> "+function_name+", RESULT-> "+str(value)+message)
    def find_keys(self,pattern):
        result = []
        for key in self.redis.scan_iter(pattern):
            result.append(key)
        self._print(inspect.currentframe().f_code.co_name,result)
        return result
    def add(self,key,value):
        value = self.hash + value
        result = self.redis.set(key,self._encrypt(value))
        self._print(inspect.currentframe().f_code.co_name,result)
        return result
    def get(self,key):
        value = self._decrypt(self._get(key))
        value = value[len(self.hash):]
        self._print(inspect.currentframe().f_code.co_name,value)
        return value
    #def updateKey(self)
    #def deleteKey(self)
    #def update_hash_on_all(self)
    #def inspect_hash_discrepancies(self)
    #def _update_hash_warning(self)
    #def master_key_hint(self)
    #def get_hash_using_master_key(self)
    #def command_list(self)
    #def exportData(self)
    #def importData(self)
    
#unitTesting
#setup.sh

#crypt -hash {Hash} -add --key {KEY} --value {VALUE} {{-debug}}
#crypt -hash {HASH} -get {KEY} {{-debug}}
#crypt -hash {HASH} -find {KEY_PATTERN} {{-debug}}

#Installation
#Pull the repo
#Install redis locally
#Start the redis server
#Install python3 redis package


#crypt = Crypt(123,debug=True)

#encrypted_value = crypt._encrypt('something')
#print(encrypted_value)
#crypt._setHash(123)
#decrypted_value = crypt._decrypt(encrypted_value)
#print(decrypted_value)

#crypt.add('uat-pass','76654534g3')
#crypt._setHash(123)
#crypt.get('uat-pass')

#crypt.find_keys('*uat*')
#crypt.get('uat-passwo')