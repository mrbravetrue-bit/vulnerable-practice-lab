# Vulnerable Practice Lab

A small, self-contained Flask app for practicing web application security —
same educational concept as DVWA/WebGoat/Juice Shop, built from scratch to
show the underlying mechanics. Every lab has a **vulnerable** version and a
**secure** version of the exact same feature, so you can compare the two
directly and see exactly what one line of code changes.

![python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)
![flask](https://img.shields.io/badge/flask-3.x-black?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

> ⚠️ **This app is intentionally insecure in its "vulnerable" mode routes.**
> Run it **only on `localhost`**, on a machine you control, disconnected
> from any untrusted network. **Never deploy this to a public server or
> expose it to the internet.** It exists purely to demonstrate, in a
> controlled local environment, how two classic vulnerability classes work
> and how to fix them.

## Labs included

| Lab | Vulnerability | Route |
|---|---|---|
| Login form | SQL Injection (auth bypass) | `/login/vulnerable` vs `/login/secure` |
| Guestbook | Stored Cross-Site Scripting (XSS) | `/guestbook/vulnerable` vs `/guestbook/secure` |

See **[WALKTHROUGH.md](./WALKTHROUGH.md)** for step-by-step exploitation
instructions and explanations of each fix.

## Quick start

```bash
cd src
pip install -r ../requirements.txt
python3 app.py
# open http://127.0.0.1:5000
```

The database resets to clean seed data every time the app starts, so you
can experiment freely.

## Why this project

Most portfolio projects show only one side of security — either "I can
find bugs" or "I can build secure systems." This one shows both at once:
the exact same feature, implemented two ways, so the reviewer can see you
understand *why* the fix works, not just that a scanner would flag it.

## Roadmap / ideas for v2

- [ ] Add a Command Injection lab (subprocess with unsanitized input)
- [ ] Add an IDOR (Insecure Direct Object Reference) lab
- [ ] Add a CSRF lab (missing token vs Flask-WTF protection)
- [ ] Dockerize for fully isolated local execution

## License

MIT
