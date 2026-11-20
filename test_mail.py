"""Real Brevo delivery test. Secrets are read from .env (nothing is hard-coded).

Run:   python test_mail.py someone@example.com
       (the address that should RECEIVE the test mail; it is separate from the sender)
"""
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

HOST, PORT = "smtp-relay.brevo.com", 587
LOGIN = os.environ.get("BREVO_SMTP_LOGIN", "").strip()
KEY = os.environ.get("BREVO_API_KEY", "").strip()          # the xsmtpsib- SMTP key
SENDER = os.environ.get("BREVO_SENDER_EMAIL", "").strip()  # verified Brevo sender
to = sys.argv[1].strip() if len(sys.argv) > 1 else ""

print("SMTP host :", HOST, PORT)
print("SMTP login:", LOGIN or "MISSING")
print("SMTP key  :", (KEY[:9] + "...") if KEY else "MISSING")
print("Sender    :", SENDER or "MISSING")
print("Recipient :", to or "MISSING (pass it: python test_mail.py you@example.com)")

if not (LOGIN and KEY and SENDER and to):
    sys.exit("\nFill in the MISSING items above and run again.")
if not KEY.startswith("xsmtpsib-"):
    sys.exit("\nBREVO_API_KEY must be the SMTP key (starts with xsmtpsib-).")

msg = EmailMessage()
msg["Subject"] = "Artspace test e-mail"
msg["From"] = f"Artspace by Archi's Studio <{SENDER}>"
msg["To"] = to
msg.set_content("If you can read this, Brevo SMTP sending works.")

try:
    with smtplib.SMTP(HOST, PORT, timeout=20) as s:
        s.starttls()
        s.login(LOGIN, KEY)
        s.send_message(msg, from_addr=SENDER, to_addrs=[to])
    print(f"\nACCEPTED by Brevo -> check {to} (also Spam), and Brevo > Transactional > Logs")
except Exception as e:  # noqa: BLE001
    print("\nFAILED ->", repr(e))