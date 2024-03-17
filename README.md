# ABEMiddle: An ABE Encryption Cloud Storage Program

ABEMiddle is a program that acts as an encryption middlepoint between a user and a cloud storage. ABEMiddle handles all encryption operations so users do not have to worry about configuring their cloud storages securely. 

Files:
- main.py: Main file to run, starts the program.
  - Initializes new PyQT5 window environment
  - Calls on loginWindow to to run login screen
- loginWindow.py: Runs UI for login and checks login credentials with MySQL database.
  - Displays login screen to user
  - Takes input credentials and sends MySQL query to see if they match the database
  - Calls on fileWindow in case of success to run storage screen
- fileWindow.py: Runs UI for storage screen.
  - Connects with AWS S3 bucket
  - Displays table viewing cloud storage files, and an upload button
  - Prompts user to choose local file if uploading, sends file with user attributes to KPABE, gets encrypted file back, and uploads to AWS.
  - Requests AWS for a certain file when downloading, sends encrypted file and user attributes to KPABE, gets decrypted file back, and prompts users for place to download file locally.
- KPABE.py: Holds the ABE algorithm that encrypts and decrypts files.
- .env: Holds environmental attributes including AWS S3 credentials and MySQL connection details
