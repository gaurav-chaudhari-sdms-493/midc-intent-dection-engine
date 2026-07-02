import os
from imap_tools import MailBox, AND
from typing import List, Dict, Any

# --- Environment Variables ---
# Expected .env keys:
# IMAP_HOST="your.imap.host"
# IMAP_USER="your_email@example.com"
# IMAP_PASSWORD="your_email_password"

def fetch_new_emails() -> List[Dict[str, Any]]:
    """
    Fetches new (unseen) emails from an IMAP server.

    Connects to the IMAP server using credentials from environment variables.
    For each unseen email, it extracts the sender, subject, text content,
    and attachments. After processing, fetched emails are marked as seen.

    Returns:
        A list of dictionaries, where each dictionary represents an email
        with the following structure:
        {
            "from": str,
            "subject": str,
            "text": str,
            "attachments": list[bytes]
        }
        Returns an empty list if no new emails are found or if there's
        an error connecting to the IMAP server.
    """
    imap_host = os.getenv("IMAP_HOST")
    imap_user = os.getenv("IMAP_USER")
    imap_password = os.getenv("IMAP_PASSWORD")

    if not all([imap_host, imap_user, imap_password]):
        print("Error: IMAP_HOST, IMAP_USER, or IMAP_PASSWORD environment variables not set.")
        return []

    new_emails: List[Dict[str, Any]] = []

    try:
        with MailBox(imap_host).login(imap_user, imap_password) as mailbox:
            # Search for unseen emails
            for msg in mailbox.fetch(AND(seen=False), mark_seen=True): # mark_seen=True will set \Seen flag
                email_text_content = msg.text or msg.html or "" # Prefer text, fallback to html, then empty
                
                attachments_data: List[bytes] = []
                for att in msg.attachments:
                    attachments_data.append(att.payload)

                new_emails.append({
                    "from": msg.from_,
                    "subject": msg.subject,
                    "text": email_text_content,
                    "attachments": attachments_data
                })
        print(f"Fetched {len(new_emails)} new emails.")
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

    return new_emails

if __name__ == "__main__":
    print("--- Fetching New Emails Example ---")
    print("Ensure IMAP_HOST, IMAP_USER, and IMAP_PASSWORD are set in your environment.")
    print("This example will attempt to connect to your IMAP server and fetch unseen emails.")
    print("Emails fetched will be marked as 'seen'.")

    # To run this example, you need to set the environment variables:
    # export IMAP_HOST="your.imap.host"
    # export IMAP_USER="your_email@example.com"
    # export IMAP_PASSWORD="your_email_password"

    # fetched_emails = fetch_new_emails()
    # if fetched_emails:
    #     for i, email in enumerate(fetched_emails):
    #         print(f"\n--- Email {i+1} ---")
    #         print(f"From: {email['from']}")
    #         print(f"Subject: {email['subject']}")
    #         print(f"Text (first 200 chars): {email['text'][:200]}...")
    #         print(f"Attachments count: {len(email['attachments'])}")
    # else:
    #     print("No new emails fetched or an error occurred.")
    print("\nExample usage is commented out. Uncomment to run with your environment variables set.")
