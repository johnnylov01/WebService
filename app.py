from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__)

canciones = [
    {"titulo": "Hotel California", "artista": "Eagles"},
    {"titulo": "Bohemian Rhapsody", "artista": "Queen"},
    {"titulo": "Stairway to Heaven", "artista": "Led Zeppelin"},
    {"titulo": "Imagine", "artista": "John Lennon"},
    {"titulo": "Hey Jude", "artista": "The Beatles"},
    {"titulo": "Smells Like Teen Spirit", "artista": "Nirvana"},
    {"titulo": "Billie Jean", "artista": "Michael Jackson"},
    {"titulo": "Knockin' on heaven's door", "artista": "Bob Dylan"},
    {"titulo": "Superstition", "artista": "Stevie Wonder"},
    {"titulo": "I Want to Break Free", "artista": "Queen"},
    {"titulo": "Sweet Child o' Mine", "artista": "Guns N' Roses"},
    {"titulo": "Back in Black", "artista": "AC/DC"},
    {"titulo": "Born to Run", "artista": "Bruce Springsteen"},
    {"titulo": "Like a Rolling Stone", "artista": "Bob Dylan"},
    {"titulo": "Wonderwall", "artista": "Oasis"},
    {"titulo": "Rolling in the Deep", "artista": "Adele"},
    {"titulo": "Uptown Funk", "artista": "Mark Ronson ft. Bruno Mars"}
]

# Template HTML con interfaz moderna
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Práctica 6: Servicio Web</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 600px;
            width: 100%;
            backdrop-filter: blur(10px);
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        
        .button-group {
            display: flex;
            gap: 20px;
            margin-bottom: 40px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            min-width: 200px;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255, 107, 107, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(45deg, #3742fa, #2f3542);
        }
        
        .btn-secondary:hover {
            box-shadow: 0 10px 25px rgba(55, 66, 250, 0.4);
        }
        
        .search-container {
            margin-bottom: 30px;
        }
        
        .search-input {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 50px;
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
            margin-bottom: 15px;
        }
        
        .search-input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .result-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-top: 30px;
            opacity: 0;
            transform: translateY(20px);
            animation: slideIn 0.5s ease forwards;
        }
        
        @keyframes slideIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .song-title {
            font-size: 1.8em;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .artist-name {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .loading {
            display: none;
            margin-top: 20px;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .music-icon {
            font-size: 3em;
            margin-bottom: 20px;
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="music-icon">🎵</div>
        <h1>Práctica 6: Servicio web</h1>
        <p class="subtitle">Recomendación de canciones aleatorias</p>
        
        <div class="button-group">
            <button class="btn" onclick="getRandomRecommendation()">
                Recomendación Aleatoria
            </button>
            <button class="btn btn-secondary" onclick="showAllSongs()">
                Ver Todas las Canciones
            </button>
        </div>
        
        <div class="search-container">
            <input type="text" 
                   class="search-input" 
                   placeholder="Buscar por artista (ej: Queen, Beatles, Bob Dylan...)"
                   id="artistInput"
                   onkeypress="handleKeyPress(event)">
            <button class="btn btn-secondary" onclick="searchByArtist()">
                🔍 Buscar por Artista
            </button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Buscando la canción perfecta...</p>
        </div>
        
        <div id="result"></div>
    </div>

    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').innerHTML = '';
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
        
        function displayResult(data) {
            hideLoading();
            const resultDiv = document.getElementById('result');
            
            if (data.error) {
                resultDiv.innerHTML = `
                    <div class="error">
                        <h3>❌ ${data.error}</h3>
                        <p>Intenta con otro artista</p>
                    </div>
                `;
            } else if (Array.isArray(data)) {
                let html = '<div class="result-card"><h3>🎵 Todas las Canciones</h3><br>';
                data.forEach(song => {
                    html += `<div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                        <strong>${song.titulo}</strong> - ${song.artista}
                    </div>`;
                });
                html += '</div>';
                resultDiv.innerHTML = html;
            } else {
                resultDiv.innerHTML = `
                    <div class="result-card">
                        <div class="song-title">🎵 ${data.titulo}</div>
                        <div class="artist-name">🎤 ${data.artista}</div>
                    </div>
                `;
            }
        }
        
        function getRandomRecommendation() {
            showLoading();
            setTimeout(() => {
                fetch('/api/recomendacion')
                    .then(response => response.json())
                    .then(data => displayResult(data))
                    .catch(error => {
                        hideLoading();
                        displayResult({error: 'Error al obtener recomendación'});
                    });
            }, 800);
        }
        
        function searchByArtist() {
            const artist = document.getElementById('artistInput').value.trim();
            if (!artist) {
                alert('Por favor, ingresa el nombre de un artista');
                return;
            }
            
            showLoading();
            setTimeout(() => {
                fetch(`/api/recomendacion/${encodeURIComponent(artist)}`)
                    .then(response => response.json())
                    .then(data => displayResult(data))
                    .catch(error => {
                        hideLoading();
                        displayResult({error: 'Error al buscar por artista'});
                    });
            }, 800);
        }
        
        function showAllSongs() {
            showLoading();
            setTimeout(() => {
                fetch('/api/canciones')
                    .then(response => response.json())
                    .then(data => displayResult(data))
                    .catch(error => {
                        hideLoading();
                        displayResult({error: 'Error al obtener canciones'});
                    });
            }, 800);
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                searchByArtist();
            }
        }
        
        // Animación de entrada
        window.addEventListener('load', function() {
            document.querySelector('.container').style.opacity = '0';
            document.querySelector('.container').style.transform = 'translateY(50px)';
            document.querySelector('.container').style.transition = 'all 0.8s ease';
            
            setTimeout(() => {
                document.querySelector('.container').style.opacity = '1';
                document.querySelector('.container').style.transform = 'translateY(0)';
            }, 100);
        });
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

# API endpoints
@app.route("/api/recomendacion")
def recomendacion():
    cancion = random.choice(canciones)
    return jsonify(cancion)

@app.route("/api/recomendacion/<artista>")
def obtener_cancion_por_artista(artista):
    resultado = [c for c in canciones if c["artista"].lower() == artista.lower()]
    
    if resultado:
        return jsonify(random.choice(resultado))
    else:
        return jsonify({"error": "No se encontraron canciones de ese artista"}), 404

@app.route("/api/canciones")
def todas_las_canciones():
    return jsonify(canciones)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
