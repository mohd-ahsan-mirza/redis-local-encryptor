# Project
A simple command line tool to manage sensitive information such as passwords using redis and python. 
# Notes
## Note 1
This tool is not meant to replace traditional methods of storing methods. Please use last pass in conjunction with this tool
## Note 2
The hash consistency is very important. Please avoid using different hashes. Scheduled backups won't run if values are encrypted with different hashes
## Note 3
DB 0 is for app 
## Note 4
DB 1 is for testing
## Note 5
```
--debug
```
Turns on debug mode
## Note 6
```
--test
```
Turns on test mode. Connects to DB 1 and restores from the latest backup for testing
## Note 7
After every 24 hours, of the last backup file creation, whatever command will be ran will also trigger a backup
## Note 8
```
{{}}
``` 
Denotes optional parameters commands take
## Note 9
```
{}
```
 Denotes mandatory parameters
# Commands
## ADD
Adding a key and value
```
crypt -add --key {KEY} --value '{VALUE}' {{--debug}} {{--test}}"
```
## GET
Get the value for the key provided. If an exact key is not found, closest matching key is returned if there was only one match  
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
Update value based on the key provided
```
crypt -update --key {KEY} --value '{VALUE}' {{--debug}} {{--test}}
```
Update key using an existing key provided
```
crypt -update --key {KEY} --new-key {NEW_KEY} {{--debug}} {{--test}}
```
Update hash on all keys. WARNING: Not recommended
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