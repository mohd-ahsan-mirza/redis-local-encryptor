# Project
A simple command line tool to manage sensitive information such as passwords using redis and python. I built this tool because I got tired of copying and pasting passwords when accessing remote servers
# Prerequisites
* Python3
* Redis-cli
* Redis python package
# Setup
## Step 1
Pull the repo
## Step 2
Add the following line in your .bash_profile. Replace the path to the path where this project is pulled
```
alias crypt='python3 {Absolute path of encryptor folder}/Run.py'
```
To load the changes
```
source ~/.bash_profile
```
## Step 3
Ensure local redis server is running
## Step 4
CD to the project and then run the following command
```
mkdir .backup
```
## Step 5
[Add your first value](https://github.com/mohd-ahsan-mirza/redis-local-encryptor#add)
## Step 6
[Create your first backup file](https://github.com/mohd-ahsan-mirza/redis-local-encryptor#backup)
# Notes
## Note 1
This tool is not meant to replace traditional methods of storing sensitive info. Please use last pass in conjunction with this tool
## Note 2
The hash consistency is very important. Please avoid using different hashes. Scheduled backups won't run if values are encrypted with different hashes
## Note 3
### DON'T forget the hash you choose. You won't be able to retrieve it anyway if you forget
## Note 4
DB 0 is for app 
## Note 5
DB 1 is for testing
## Note 6
```
--debug
```
Turns on debug mode
## Note 7
```
--test
```
Turns on test mode. Connects to DB 1 and restores from the latest backup for testing
## Note 8
After every 24 hours, of the last backup file creation, whatever command will be ran will also trigger a backup
## Note 9
```
{{}}
``` 
Denotes optional parameters commands take
## Note 10
```
{}
```
 Denotes mandatory parameters
## Note 11
When adding or updating values, you might have to use double or single quotes for values depending if there are any special characters
# Commands
## Add
Adding a key and value. You will be prompted to enter value
```
crypt -add --key {KEY} {{--debug}} {{--test}}"
```
## Get
Get the value for the key provided. If an exact key is not found, closest matching key is returned if there was only one match  
### IMPORTANT: If successful, value returned is copied in the clipboard
```
crypt -get {KEY} {{--debug}} {{--test}}
```
## Find
Find all keys
```
crypt -find "*" {{--debug}} {{--test}}
```
Find keys matching pattern. Read redis documentation on pattern matching
```
crypt -find '{KEY_PATTERN}' {{--debug}} {{--test}}
```
## Update
Update value based on the key provided. You will be prompted to enter value
```
crypt -update --key {KEY} --value {{--debug}} {{--test}}
```
Update key using an existing key provided
```
crypt -update --key {KEY} --new-key {NEW_KEY} {{--debug}} {{--test}}
```
### WARNING: Not recommended
Update hash on all keys. 
```
crypt -update --hash {NEW_HASH} {{--debug}} {{--test}}
```
## Delete
Delete value based on the key provided
```
crypt -delete {KEY} {{--debug}} {{--test}}
```
## Inspect
Inspect if all keys are encrypted with the same hash
```
crypt -inspect --hash {{--debug}} {{--test}}
```
## Backup
Backup the app database into a file under .backup. There is a scheduled backup that will run every 24 hours
```
crypt -backup {{--debug}}
```
## Restore
Restore either from a selected file or from the last file that was created
```
crypt -restore {{--file}} {{file}} {{--debug}} {{--test}}
```
## Flush
Flush db 1 data
```
crypt -flush --test-data {{--debug}}
```
## List
List all currently available commands
```
crypt -list
```