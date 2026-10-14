from flask import Flask, request, render_template, redirect, make_response
import uuid
import html
import bleach

app = Flask(__name__)

users_db = {"hacker": "password123", "vittima": "12345"}
active_sessions = {}
messages = []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if users_db.get(u) == p:
            sid = str(uuid.uuid4())
            active_sessions[sid] = u
            resp = make_response(redirect('/'))
            
            # 1. GENERAZIONE DELLA SESSIONE: Imposta l'identificativo unico nel browser.
            # Se decommentiamo 'httponly=True', blocchiamo l'accesso a questa variabile tramite JavaScript,
            # rendendo inutile il payload dell'attaccante ('document.cookie' restituirà vuoto).
            
            resp.set_cookie('session_id', sid)#httponly=True blocco i cookie
            return resp
    return render_template('login.html')



@app.route('/', methods=['GET', 'POST'])
def forum():
     # 2. VERIFICA SESSIONE: Controlla se il browser possiede un cookie di sessione valido.
    user = active_sessions.get(request.cookies.get('session_id'))
    if not user: return redirect('/login')
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg: 
            # 3. IL PUNTO CRITICO DELLA VULNERABILITÀ STORED XSS:
            # Poiché le funzioni di pulizia (html.escape o bleach) sono commentate, il testo viene 
            # memorizzato nel server esattamente come inserito (incluso eventuale codice JavaScript).
            
            #cleaned_msg = html.escape(msg)
            #testo_sicuro = bleach.clean(msg)
            messages.append({"user": user, "content": msg})
        return redirect('/')
    return render_template('forum.html', user=user, messages=messages)


# 4. SIMULAZIONE DEL FIREWALL TRAMITE INTERCETTAZIONE DELLE RISPOSTE (Middleware) CSP 
@app.after_request
def firewall_simulation(response):
    # 5. REGOLA DEL FIREWALL SUL TRAFFICO IN USCITA DAL BROWSER:
    # Questa stringa vieta esplicitamente al browser di fare chiamate verso porte non autorizzate.
    # Non essendoci la porta 9090, il browser stesso bloccherà la fetch() sul nascere.
    
    csp_rules = "default-src * 'unsafe-inline'; connect-src https://* http://localhost:8080;"
    
    # 6. ATTIVAZIONE CSP: Applica la regola inserendola negli header di risposta HTTP.
    response.headers['Content-Security-Policy'] = csp_rules
    return response




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
   
    
    
    
