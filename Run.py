import os
from crypt import *
import getpass

hash = getpass.getpass(prompt='Hash: ')

if(len(hash) == 0):
    if sys.argv[1] not in ["-find","-list"]:
        print("No hash provided. Exiting")
        sys.exit()
debug = False
if "--debug" in sys.argv:
    debug = True
#Initialize class
crypt = Crypt(hash,debug)
#Add
if sys.argv[1] == "-add":
    if sys.argv[2] != "--key":
        print("No key argument provided")
        sys.exit()
    value = getpass.getpass(prompt='Value: ')
    if(len(value) == 0):
        print("No value provided. Exiting")
        sys.exit()
    crypt.add(sys.argv[3],value)
    sys.exit()
#Get
if sys.argv[1] == "-get":
    result = crypt.get(sys.argv[2])
    os.system("echo '%s' | pbcopy" % result)
    sys.exit()
#Find
if sys.argv[1] == "-find":
    result = crypt.find_keys(sys.argv[2])
    print("----------------------------------------------------------------------")
    print("\n".join(result))
    print("----------------------------------------------------------------------")
    sys.exit()
#Update
if sys.argv[1] == "-update":
    if sys.argv[2] == "--hash":
        new_hash = ""
        new_hash = getpass.getpass(prompt='New Hash: ')
        if(len(hash) == 0):
            print("No new hash provided. Exiting")
            sys.exit()
        result = crypt.update_hash_on_all(new_hash)
        if result:
            print("All values have been encrypted with the new hash")
        else:
            print("There are keys that encrypted with a different hash than the original one provided or the hash provided doesn't matches one with the keys")
    else:
        if sys.argv[2] != "--key":
            print("No key argument provided")
            sys.exit()
        if sys.argv[4] != "--value":
            if sys.argv[4] != "--new-key":
                print("No Value argument provided or New key argument provided")
                sys.exit()
            else:
                crypt.update_key(sys.argv[3],sys.argv[5])
                sys.exit()
        else:
            crypt.update(sys.argv[3],sys.argv[5])
    sys.exit()
#Delete
if sys.argv[1] == "-delete":
    crypt.delete(sys.argv[2])
    sys.exit()
#Inspect
if sys.argv[1] == "-inspect":
    if(sys.argv[2] == "--hash"):
        result = crypt.hash_discrepancy()
        if(len(result)):
            print("The following keys are encrypted with a different hash than the one provided")
            print("----------------------------------------------------------------------")
            print("\n".join(result))
        else:
            print("Hooray!! All keys are encrypted with the same hash")
    sys.exit()
if sys.argv[1] == "-list":
    result = crypt.list_commands()
    print("----------------------------------------------------------------------")
    print("\n".join(result))
    print("----------------------------------------------------------------------")
    sys.exit()
#Export
if sys.argv[1] == "-backup":
    result = crypt.backup()
    if result:
        print("Backup created successfully")
    else:
        print("There are keys that encrypted with a different hash")
    sys.exit()
print("Arguments provided are not valid")
sys.exit()



    


