import imaplib
import email
import json
import os

# These will be stored safely in GitHub Secrets later
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS') 

def fetch_lic_emails():
    # Connect to Gmail/Email provider
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    # Search for LIC related emails
    result, data = mail.search(None, '(FROM "licindia.com")')
    
    bill_list = []
    
    for num in data[0].split():
        result, msg_data = mail.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Simple logic to extract Date and Subject (where amount usually is)
        bill_list.append({
            "date": msg['Date'],
            "subject": msg['Subject'],
            "status": "Paid"
        })

    # Save to a JSON file that our HTML will read
    with open('bills.json', 'w') as f:
        json.dump(bill_list, f, indent=4)

if __name__ == "__main__":
    fetch_lic_emails()
