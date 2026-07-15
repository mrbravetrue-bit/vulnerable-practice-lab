# Walkthrough

Guided exercises for both labs. Try the vulnerable version first, confirm
the exploit works, then try the same input against the secure version and
see it fail — then read *why*.

---

## Lab 1: SQL Injection (Login)

**URL:** `/login/vulnerable` vs `/login/secure`

### The vulnerability

The vulnerable route builds its SQL query like this:

```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```

Whatever the user types gets pasted directly into the SQL string. If the
input contains SQL syntax, it becomes part of the query itself.

### Try it

1. Go to `/login/vulnerable`
2. Username: `admin`
3. Password: `' OR '1'='1`
4. The resulting query becomes:
   ```sql
   SELECT * FROM users WHERE username='admin' AND password='' OR '1'='1'
   ```
   Because `'1'='1'` is always true, the `WHERE` clause matches every row —
   you're logged in without knowing the real password. The page shows you
   the exact query that ran, so you can see this happening.
5. Now try the exact same input against `/login/secure` — it fails.

### The fix

```python
conn.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (username, password),
)
```

With a parameterized query, the database driver treats `?` placeholders
and their values as strictly *data*, never as part of the SQL syntax — so
no input, however crafted, can change the query's structure.

---

## Lab 2: Stored XSS (Guestbook)

**URL:** `/guestbook/vulnerable` vs `/guestbook/secure`

### The vulnerability

The vulnerable template renders each message like this:

```jinja
{{ entry.message|safe }}
```

The `|safe` filter tells the template engine "trust this string completely,
render it as raw HTML." Since the message came from user input, an attacker
can submit HTML/JavaScript that will execute in every other visitor's
browser when they view the guestbook — this is "stored" because it's saved
to the database and served to everyone, not just the attacker.

### Try it

1. Go to `/guestbook/vulnerable`
2. Name: `visitor3`
3. Message: `<script>alert('stored XSS')</script>`
4. Submit, then reload the page — the alert fires. Any real visitor to this
   page would run that script in their browser session.
5. Try the same message on `/guestbook/secure` — it's displayed as literal
   text (`<script>alert(...)</script>` shown on screen, not executed).

### The fix

Just remove `|safe`:

```jinja
{{ entry.message }}
```

Jinja2 (Flask's template engine) auto-escapes output by default — angle
brackets and quotes get converted to HTML entities (`&lt;`, `&gt;`, etc.),
so injected markup is displayed as inert text instead of being parsed as
HTML/JS by the browser.

---

## Key takeaway

Both vulnerabilities follow the same root pattern: **untrusted input was
allowed to change how a downstream system (the SQL parser, the HTML
parser) interprets structure, instead of being treated purely as data.**
Parameterized queries and default output-escaping both work by preserving
that separation.
