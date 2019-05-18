import os
from crypt import *
import getpass

#hash = ""
#if sys.argv[1] not in ["-find","-list","-restore"]:
hash = getpass.getpass(prompt='Hash: ')
if(len(hash) == 0):
    print("No hash provided. Exiting")
    sys.exit()
test = False
if "--test" in sys.argv:
    test = True
    print("---TEST MODE ON----")
debug = False
if "--debug" in sys.argv:
    debug = True
    print("---DEBUG MODE ON----")
#Initialize class
crypt = Crypt(hash,debug,test)
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
    if len(sys.argv) >= 4 and sys.argv[3] == "--return-value":
        os.system("echo '%s'" % result)
    else:
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
            update_key_value = getpass.getpass(prompt='New Value: ')
            if(len(update_key_value) == 0):
                print("No new hash provided. Exiting")
                sys.exit()
            crypt.update(sys.argv[3],update_key_value)
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
        print("There are keys that encrypted with a different hash. Please ensure consistency in hash")
    sys.exit()
#Restore
if sys.argv[1] == "-restore":
    confirm_restore =  getpass.getpass(prompt='Value (Y/N):')
    if confirm_restore == "Y":
        if(sys.argv[2] == "--file"):
            crypt.restore(sys.argv[3])
        else:
            crypt.restore()
        print("Restore finished")
    else:
        print("Exiting")
    sys.exit()
#Flush
if sys.argv[1] == "-flush":
    if sys.argv[2] == "--test-data":
        crypt.flush_test_data()
        print("Test data flushed")
        sys.exit()
print("Arguments provided are not valid")
sys.exit()



    


