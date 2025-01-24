import os
from flask import Flask, render_template, request, jsonify

# Configurações da aplicação
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 

# Definindo onde arquivos de upload devem ser armazenados
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Definindo tamanho máximo permitido para uploads
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Criando aplicação e definindo diretórios importantes
app = Flask(__name__, 
    template_folder='app/templates',
    static_folder='app/static',
)

# Função para verificar se o arquivo é permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----- Página principal -----
@app.route('/')
def home():
    return render_template('home.html')

# ----- Página de segmentação por limiarização -----
@app.route('/threshold')
def threshold():
    return render_template('threshold.html') 

# Definindo rota que só aceita requisições do tipo POST para upload de arquivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if file not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de arquivo não suportado. Apenas PNG e JPG são permitidos.'}), 400

    # Salvar o arquivo na pasta "uploads"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Cria a pasta, se não existir
    file.save(filepath)
    return jsonify({'success': 'Upload realizado com sucesso!', 'filepath': filepath}), 200   

# Inicializador da aplicação 
if __name__ == '__main__':
    app.run(debug=True)