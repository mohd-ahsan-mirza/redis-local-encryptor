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
    def _get_hash_of_key(self,key):
        value = self._decrypt(self._get(key))
        self._print(inspect.currentframe().f_code.co_name,value,"Function returns true when hash is appended to the decoded string")
        return value[0:len(self.hash)]
    def _validate(self,key):
        return (self.hash == self._get_hash_of_key(key))
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
        #TODO
        value = self.hash + value
        result = self.redis.set(key,self._encrypt(value))
        self._print(inspect.currentframe().f_code.co_name,result)
        return result
    def get(self,key):
        value = self._decrypt(self._get(key))
        #TODO
        value = value[len(self.hash):]
        self._print(inspect.currentframe().f_code.co_name,value)
        return value
    def update(self,key,value):
        #TODO: Validate hash
        if(self.redis.exists(key)):
            self.add(key,value)
        else:
            print("No key exists -> "+str(key))
    def delete(self,key):
        #TODO: Validate hash
        if(self.redis.exists(key)):
            self.redis.delete(key)
        else:
            print("No key exists -> "+str(key))
    def hash_discrepancy(self):
        result = []
        for key in self.find_keys("*"):
            if not self._validate(key):
                result.append(key)
        return result
    def update_hash_on_all(self,new_hash):
        if(len(self.hash_discrepancy())):
            return False
        else:
            keys = self.find_keys("*")
            keys_values = {}
            for key in keys:
                if not self._validate(key):
                    return False
            for key in keys:
                keys_values[key] = self.get(key)
            self._setHash(new_hash)
            for key in keys:
                self.update(key,keys_values[key])
            return True
    def list_commands(self):
        return [
            "crypt -hash {Hash} -add --key {KEY} --value '{VALUE}' {{-debug}}",
            "crypt -hash {HASH} -get {KEY} {{-debug}}",
            "crypt -hash {HASH} -find '{KEY_PATTERN}' {{-debug}}",
            "crypt -hash {HASH} -update --key {KEY} --value '{VALUE}' {{-debug}}",
            "crypt -hash {HASH} -update --hash '{new hash}' {{--debug}}",
            "crypt -hash {HASH} -delete {KEY} {{-debug}}",
            "crypt -hash {HASH} -inspect --hash {{-debug}}",
            "crypt -hash {HASH} -list"

        ]

#TODO
# Add unit test. Connect to a different db for testing
#crypt -test
# Change functions, add, get, _get_hash_of_key
#def exportData(self)
#def importData(self)


#setup.sh
#Pull the repo
#Install redis locally
#Start the redis server
#Install python3 redis package
