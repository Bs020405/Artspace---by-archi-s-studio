# Interior Company — Customer Portal

A customer registration/login system for your Interior Company website, built with
**Flask (Python) + HTML/CSS**, storing all customer data in **Excel files** (no
database needed) and **emailing you** (bhavyasoni0787@gmail.com) every time a
customer registers, books a consultation, or sends an inquiry.

## What it does

- ✅ Customer registration & login/logout (passwords are hashed, never stored in plain text)
- ✅ Customer profile — view & edit name, phone, address
- ✅ Book an interior-design consultation (service, date, time, address, notes)
- ✅ View consultation/booking history with a live status pill (Pending / Confirmed / In Progress / Completed / Cancelled)
- ✅ Send general inquiries (works for logged-in customers and guests)
- ✅ Every signup / booking / inquiry sends an email notification to `bhavyasoni0787@gmail.com`
- ✅ All customer, booking and inquiry data is saved to Excel (`data/users.xlsx`, `data/bookings.xlsx`, `data/inquiries.xlsx`)
- ✅ Same visual design as your original landing page (fonts, colors, layout)

## Project structure

```
interior-company/
├── app.py                  Flask backend (routes, Excel storage, email)
├── requirements.txt
├── data/                   Excel files are created here automatically
├── static/
│   └── style.css           Shared stylesheet (your original design + forms)
└── templates/
    ├── base.html            Shared nav + footer
    ├── index.html           Landing page (your original design)
    ├── register.html
    ├── login.html
    ├── dashboard.html        Profile + booking history + status
    ├── edit_profile.html
    ├── book_consultation.html
    └── inquiry.html
```

## 1. Install & run locally

```bash
cd interior-company
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser. That's it — the app will
create the Excel files in `data/` the first time it runs.

Without email set up (see step 2), the app still works perfectly — it just
prints the notification email to your terminal instead of sending it, so you
can develop/test freely.

## 2. Connect it to bhavyasoni0787@gmail.com (so you actually receive emails)

Gmail requires an **App Password** — a 16-character code, not your normal
Gmail password — to let a script send mail through your account.

1. Go to your Google Account → **Security**.
2. Turn on **2-Step Verification** (required before app passwords are available).
3. Go to **Security → App passwords** (search "App passwords" if you can't find it).
4. Create one named e.g. "Interior Company Website" and copy the 16-character code.
5. Set these two environment variables before running the app:

   **macOS/Linux:**
   ```bash
   export EMAIL_ADDRESS="bhavyasoni0787@gmail.com"
   export EMAIL_PASSWORD="the16characterapppassword"
   python app.py
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:EMAIL_ADDRESS="bhavyasoni0787@gmail.com"
   $env:EMAIL_PASSWORD="the16characterapppassword"
   python app.py
   ```

   You can use `bhavyasoni0787@gmail.com` itself as the sending account (so it
   emails itself), or create a separate Gmail account to send from — either
   way, notifications always land in `bhavyasoni0787@gmail.com` because that's
   hard-coded as `NOTIFY_EMAIL` in `app.py`.

That's the only setup needed — no other email service, API key, or paid tool.

## 3. Where the data goes

Every record is written to an Excel workbook the moment it's submitted:

| File | Contains |
|---|---|
| `data/users.xlsx` | Every registered customer (name, email, phone, address, hashed password, signup date) |
| `data/bookings.xlsx` | Every consultation booking (linked to the customer's email, service, date/time, address, notes, **status**) |
| `data/inquiries.xlsx` | Every inquiry message sent through the "Send Inquiry" form |

You can open these directly in Excel any time — even while the app is
running (close and reopen if it's locked for editing).

## 4. Updating a booking's status

To move a booking from **Pending** to **Confirmed / In Progress / Completed /
Cancelled**, open `data/bookings.xlsx`, find the row, and edit the **Status**
column, then save. The customer will see the updated status pill the next
time they open their dashboard — no restart needed.

Valid status values (for the colored pill to render correctly): `Pending`,
`Confirmed`, `In Progress`, `Completed`, `Cancelled`.

## 5. Redirects

- After registering → customer is logged in automatically and sent to the **landing page**.
- After logging in → sent to the landing page (or wherever they were headed, e.g. back to booking).
- After booking a consultation → sent to **My Account** (dashboard) to see it in their history.
- After sending an inquiry → sent back to the **landing page** with a confirmation message.

## 6. Deploying online (optional)

To make this live on the internet instead of just `127.0.0.1`, you can deploy
to a free/low-cost host such as **Render**, **PythonAnywhere**, or **Railway**.
General steps for any of them:

1. Push this folder to a GitHub repository.
2. Create a new "Web Service" / app on the host, pointing at that repo.
3. Set the start command to `python app.py` (or `gunicorn app:app` if the
   host asks for gunicorn — add `gunicorn` to `requirements.txt` in that case).
4. Add `EMAIL_ADDRESS` and `EMAIL_PASSWORD` as environment variables/secrets
   in the host's dashboard (same values as step 2 above).
5. Also set `SECRET_KEY` to a random string for security.

If you'd like, I can also walk you through deploying to a specific host —
just let me know which one you'd prefer.

## Notes on security

- Passwords are hashed with Werkzeug's `generate_password_hash` — they are
  never stored or emailed in plain text.
- `SECRET_KEY` in `app.py` defaults to a placeholder — set a real
  `SECRET_KEY` environment variable before putting this online.
- Excel is fine for a small/medium customer base. If you outgrow it later
  (thousands of bookings), the same routes can be pointed at a proper
  database (e.g. SQLite/PostgreSQL) with minimal changes — happy to help
  with that migration when the time comes.
