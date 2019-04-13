import os
from crypt import *

if len(sys.argv) < 4:
    print("To few arguments provided")
    sys.exit()
if sys.argv[1] != "-hash":
    print("No Hash argument provided")
    sys.exit()
hash = sys.argv[2]
debug = False
if "--debug" in sys.argv:
    debug = True
#Initialize class
crypt = Crypt(hash,debug)
#Add
if sys.argv[3] == "-add":
    if len(sys.argv) < 8:
        print("To few arguments provided")
        sys.exit()
    if sys.argv[4] != "--key":
        print("No key argument provided")
        sys.exit()
    if sys.argv[6] != "--value":
        print("No Value argument provided")
        sys.exit()
    crypt.add(sys.argv[5],sys.argv[7])
#Get
if sys.argv[3] == "-get":
    if len(sys.argv) < 5:
        print("To few arguments provided") 
        sys.exit()
    result = crypt.get(sys.argv[4])
    os.system("echo '%s' | pbcopy" % result)
#Find
if sys.argv[3] == "-find":
    if len(sys.argv) < 5:
        print("To few arguments provided") 
        sys.exit()
    result = crypt.find_keys(sys.argv[4])
    print("\n".join(result))
#Update
if sys.argv[3] == "-update":
    if len(sys.argv) < 6:
        print("To few arguments provided")
        sys.exit()
    if sys.argv[4] == "--hash":
        result = crypt.update_hash_on_all(sys.argv[5])
        if result:
            print("All values have been encrypted with the new hash")
        else:
            print("There are keys that encrypted with a different hash than the original one provided or the hash provided doesn't matches one with the keys")
    else:
        if sys.argv[4] != "--key":
            print("No key argument provided")
            sys.exit()
        if sys.argv[6] != "--value":
            print("No Value argument provided")
            sys.exit()
        crypt.update(sys.argv[5],sys.argv[7])
#Delete
if sys.argv[3] == "-delete":
    if len(sys.argv) < 5:
        print("To few arguments provided") 
        sys.exit()
    crypt.delete(sys.argv[4])
#Inspect
if sys.argv[3] == "-inspect":
    if len(sys.argv) < 5:
        print("Too few arguments provided")
        sys.exit()
    if(sys.argv[4] == "--hash"):
        result = crypt.hash_discrepancy()
        if(len(result)):
            print("The following keys are encrypted with a different hash than the one provided")
            print("----------------------------------------------------------------------")
            print("\n".join(result))
        else:
            print("Hooray!! All keys are encrypted with the same hash")
if sys.argv[3] == "-list":
    result = crypt.list_commands()
    print("\n".join(result))



    


