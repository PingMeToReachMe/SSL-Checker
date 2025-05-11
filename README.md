# SSL Certification Checker

## Installation Instructions 

- Clone the Repository
Run the following command in terminal to download:

git clone https://github.com/PingMeToReachMe/SSL-Checker.git

This will create a folder titled SSL-Checker. 

- Navigate to 'cd SSL-Checker'  

There are no third party packages required for installation. 

- Execute the script using Python: 
python ssl_checker.py

## Instructions for Use - Inputs/Outputs 

Output - Are you backing up the information in a log file? (yes/no):

Input - yes

Output - Enter the path name to your .txt file for logging. 

Input - C:\User\Admin\Documents\logfile.txt

OR

Input - cancel (this will cancel your previous input to move onto the next step)

OR

Input - no

Output - Enter website, or type 'file' to load from .txt, or 'exit' to quit:

Input - yahoo.com (example)

Output - Checking SSL certificate for: yahoo.com Website: yahoo.com Subject: yahoo.com Issuer: DigiCert SHA2 High Assurance Server CA Expiration Date: 2025-06-11 23:59:59 Days Until Expiration: 31 days Status: Valid

OR

Input - file (in order to use a .txt file with a list of domains) 

Output - Enter path to your .txt file (e.g., domains.txt):

Input - C:\User\Admin\Documents\domains.txt

OR

Input - exit (this will add a summary to the log file if used)

## Best Practices

- This code works best when used with >100 domains at a time. You may experience longer loading times if using longer lists of domains.
- If using on an organizational level, you may run into security concerns if using to check certifications for domains that are outside of your network
