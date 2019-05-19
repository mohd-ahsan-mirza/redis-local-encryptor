import sys
import redis
import base64
import inspect
import pickle
import datetime
import os
import glob
import time

class Crypt:
    def __init__(self,hash,debug=False,test=False):
        self._test = test
        self._debug = debug
        self._setHash(hash)
        self.backup_directory = os.path.abspath(os.path.dirname(__file__)) + "/.backup/"
        self._initialize_redis_connection(0) #Main db
        if self._test: 
            self._initialize_redis_connection(1) #Test db
            self.restore() #Restore from latest backup for testing
        else:
            self._initiate_backup()
    def _initialize_redis_connection(self,db_index):
        self._print(inspect.currentframe().f_code.co_name,db_index,"DB Index")
        try:
            self.redis = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True, db=db_index)
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
        return decoded_string
    def _setHash(self,new_hash):
        self.hash = str(new_hash) + "-"
        #self._print(inspect.currentframe().f_code.co_name,self.hash)
    def _get_hash_of_key(self,key):
        value = self._decrypt(self._get(key))
        self._print(inspect.currentframe().f_code.co_name,value,"Function returns true when hash is appended to the decoded string")
        return value[0:len(self.hash)]
    def _validate(self,key,shudown=True):
        self._print(inspect.currentframe().f_code.co_name,self.hash,"Hash provided")
        self._print(inspect.currentframe().f_code.co_name,self._get_hash_of_key(key),"Hash of key")
        result = (self.hash == self._get_hash_of_key(key))
        if not result:
            if shudown:
                print("Error!! The hash provided doesn't match. Shutting down")
                sys.exit(1)
        return result
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
    def _get_latest_from_backup(self):
        list_of_files = glob.glob(self.backup_directory+"*")
        return max(list_of_files, key=os.path.getctime)
    def _initiate_backup(self):
        now = time.time()
        day_ago = now - 60*60*24
        latest_file = self._get_latest_from_backup()
        self._print(inspect.currentframe().f_code.co_name,latest_file,"Last backup file")
        file_creation_time = os.path.getctime(latest_file)
        if file_creation_time < day_ago:
            print("Initiating scheduled backup")
            self.backup()
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
    def update(self,key,value):
        self._validate(key)
        if(self.redis.exists(key)):
            self.add(key,value)
        else:
            print("No key exists -> "+str(key))
            self.add(key,value)
            print("New key added")
    def update_key(self,key,new_key):
        value = self.get(key)
        self.delete(key)
        self.add(new_key,value)
    def delete(self,key):
        self._validate(key)
        if(self.redis.exists(key)):
            self.redis.delete(key)
        else:
            print("No key exists -> "+str(key))
    def hash_discrepancy(self):
        result = []
        for key in self.find_keys("*"):
            if not self._validate(key,False):
                result.append(key)
        return result
    def update_hash_on_all(self,new_hash):
        if(len(self.hash_discrepancy())):
            return False
        else:
            keys = self.find_keys("*")
            keys_values = {}
            for key in keys:
                keys_values[key] = self.get(key)
            self._setHash(new_hash)
            for key in keys:
                self.add(key,keys_values[key])
            return True
    def list_commands(self):
        return [
            "crypt -add --key {KEY} {{--debug}} {{--test}}",
            "crypt -get {KEY} {{--return-value}} {{--debug}} {{--test}}",
            "crypt -find '{KEY_PATTERN}' {{--debug}} {{--test}}",
            "crypt -update --key {KEY} --value {{--debug}} {{--test}}",
            "crypt -update --key {KEY} --new-key {NEW_KEY} {{--debug}} {{--test}}",
            "crypt -update --hash {NEW_HASH} {{--debug}} {{--test}}",
            "crypt -delete {KEY} {{--debug}} {{--test}}",
            "crypt -inspect --hash {{--debug}} {{--test}}",
            "crypt -backup {{--debug}}",
            "crypt -restore {{--file}} {{file}} {{--debug}} {{--test}}",
            "crypt -flush --test-data {{--debug}}",
            "crypt -list"
        ]
    def backup(self):
        if(self._test):
            print("Warning!!! Can't backup in test mode")
            sys.exit(1)
        if(len(self.hash_discrepancy())):
            return False
        else:
            keys = self.find_keys("*")
            keys_values = {}
            for key in keys:
                keys_values[key] = self._get(key)
            self._print(inspect.currentframe().f_code.co_name,keys_values)
            file_name = self.backup_directory+"backup"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".pickle"
            self._print(inspect.currentframe().f_code.co_name,file_name,"File to be generated",True)
            pickle_out = open(file_name,"wb")
            pickle.dump(keys_values, pickle_out)
            pickle_out.close()
            return True
    def restore(self,selected_file=""):
        if selected_file == "":
            selected_file = self._get_latest_from_backup()
        else:
            selected_file = self.backup_directory + selected_file
            if not os.path.isfile(selected_file):
                print("FILE DOESN'T EXIST!! SHUTTING DOWN")
                sys.exit(1)
        self._print(inspect.currentframe().f_code.co_name,selected_file,"File selected")
        pickle_in = open(selected_file,"rb")
        data = pickle.load(pickle_in)
        self._print(inspect.currentframe().f_code.co_name,data)
        for key in data:
            self.redis.set(key,data[key])
    def flush_test_data(self):
        self._initialize_redis_connection(1) #Test db
        keys = self.find_keys("*")
        self._print(inspect.currentframe().f_code.co_name,keys,"Keys in test db")
        if len(keys) == 0:
            return False
        for key in keys:
            self.redis.delete(key)
        return True
            
#TODO
#Email the backup to the work email. New class. Set option to use. Email or dropbox. Multithreading
