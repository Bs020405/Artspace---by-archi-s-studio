# Continue with Google — setup (ARTSPACE by Archi's Studio)

## 1. Files kahan rakhni hain
Apne project folder me (jahan `app.py` hai):

| File | Kaam |
|---|---|
| `app.py` | purani app.py ki jagah (sirf Google/Flask-Login/.env wale hisse badle hain) |
| `templates/base.html` | purani base.html ki jagah (Google button + avatar) |
| `.env` | aapki secret settings (Google keys, SECRET_KEY) — **kisi ko share nahi karni** |
| `.env.example` | bina secret wala sample (share kar sakte ho) |
| `.gitignore` | `.env`, `razorpay_secret.txt`, `*.xlsx` ko GitHub se bahar rakhta hai |
| `requirements.txt` | zaruri packages (agar aapki pehle se hai to usme ye lines jod do) |

## 2. Packages install karo
```
pip install -r requirements.txt
```
Naye packages: **Authlib**, **Flask-Login**, **python-dotenv** (+ requests).

## 3. Google Cloud Console me ye hona chahiye
(APIs & Services → Credentials → aapka OAuth client)
- **Authorised redirect URI:** `http://127.0.0.1:5000/login/google/callback`  (bilkul yahi)
- **Authorised JavaScript origin:** `http://127.0.0.1:5000`
- **OAuth consent screen** "Testing" me ho to **Test users** me wo Gmail ids jodo jinse login test karna hai.

## 4. Chalao
```
python app.py
```
Console me `[INFO] Google sign-in enabled` dikhna chahiye. Browser me **http://127.0.0.1:5000** kholo
(agar `localhost:5000` khologe to app khud `127.0.0.1` par bhej dega, kyunki Google me wahi registered hai).

## 5. Local test (aap khud karo, 2 minute)
1. `/login` kholo → upar **Continue with Google** button dikhna chahiye (`/register` par bhi).
2. Button dabao → Google account chuno → seedha **/dashboard** khulna chahiye, header me aapka naam (+ photo).
3. `users.xlsx` kholo: nayi row me **Full Name, Email, Google ID, Profile Picture** bhare hone chahiye
   (Excel band karke kholna, app chalte waqt file lock ho sakti hai).
4. **Logout** dabao, phir dobara Google se login karo → **nayi row nahi banni chahiye** (duplicate nahi).
5. Jis email se pehle password se account banaya tha, usi se Google login karo → wahi account khulega
   (usme bas Google ID/photo judega, naam aur password waise hi rahenge).

## 6. Live (internet par) jaate waqt
1. Google me redirect URI jodo: `https://tumhara-domain.com/login/google/callback`
2. `.env` me: `GOOGLE_REDIRECT_URI=https://tumhara-domain.com/login/google/callback` aur `SESSION_COOKIE_SECURE=1`
3. OAuth consent screen ko **Publish** karo (warna sirf Test users login kar paate hain).
4. `SECRET_KEY` lamba random rakho (abhi `.env` me ek random key bani hui hai).

## 7. Security
- **Client Secret sirf `.env` me hai** aur sirf server (app.py) use karta hai — kisi HTML/JavaScript me nahi jaata.
- `.env` aur Google ki `client_secret_....json` file ko GitHub/WhatsApp/chat me mat bhejo; JSON file project folder se hata do.
- Ye secret chat me share hua hai, isliye live jaane se pehle Google Console me naya secret banao
  (Credentials → client → "Add secret", purana disable) aur `.env` me `GOOGLE_CLIENT_SECRET` badal do.
- Session cookie: HttpOnly + SameSite=Lax; login ke baad naya session banta hai; logout se poora session saaf.

## 8. Dikkat aaye to
| Error | Matlab / hal |
|---|---|
| `redirect_uri_mismatch` | Google me URI bilkul `http://127.0.0.1:5000/login/google/callback` hona chahiye; site `127.0.0.1:5000` par kholo |
| `Access blocked / app not verified` | consent screen Testing me hai → apna Gmail Test users me jodo |
| `Google sign-in is OFF` (console) | `.env` app.py ke bagal me hai? `pip install -r requirements.txt` chala? |
| "users.xlsx is locked" | Excel me khuli file band karo |
| Login ke baad wapas login page | `SECRET_KEY` badal gayi ya cookie block — dobara try karo |

## 9. app.py me kya badla (baaki sab waisa hi)
- Upar: `.env` load hona (python-dotenv) + safe session-cookie settings.
- `users.xlsx` me 2 nayi columns: **Google ID**, **Profile Picture** (purani file/rows waise hi rehti hain, header apne aap jud jaate hain).
- Naya section (logout route ke baad): Authlib OAuth, Flask-Login, `/login/google`, `/login/google/callback`.
- Razorpay, payments, invoice, orders, cart, bookings, admin — **koi badlav nahi**.
