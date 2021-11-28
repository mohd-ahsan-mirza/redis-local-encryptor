# Use this script to install all necessary packages on MAC OS
pip3 install redis
brew install redis
brew services start redis
mkdir .backup
touch .backup/placeholder
