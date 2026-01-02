from imapclient import IMAPClient
import pyzmail

IMAP_HOST = "imap.gmail.com"
IMAP_USER = "aw3146341@gmail.com"
IMAP_PASS = "uxym ftsr dvhb hzeq"

def fetch_latest_email():
    with IMAPClient(IMAP_HOST) as server:
        server.login(IMAP_USER, IMAP_PASS)
        server.select_folder("INBOX")

        messages = server.search(["ALL"])
        if not messages:
            return None

        latest_id = messages[-1]
        raw_msg = server.fetch([latest_id], ["RFC822"])[latest_id][b"RFC822"]

        return pyzmail.PyzMessage.factory(raw_msg)
