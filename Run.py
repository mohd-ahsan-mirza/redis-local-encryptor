import os
from crypt import *

if len(sys.argv) < 5:
    print("To few arguments provided")
    sys.exit()
if sys.argv[1] != "-hash":
    print("Hash argument provided")
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

    


