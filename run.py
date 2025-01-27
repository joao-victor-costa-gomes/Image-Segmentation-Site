import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename

# Criando aplicação e definindo diretórios importantes
app = Flask(__name__, 
    template_folder='app/templates',
    static_folder='app/static',
)

# Configurações da aplicação
class Config:
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 
    SECRET_KEY = 'secret_key'

app.config.from_object(Config)

# Função para verificar se o arquivo é permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# ----- Página principal -----
@app.route('/')
def home():
    return render_template('home.html')

# ----- Página de segmentação por limiarização -----
@app.route('/threshold', methods=['GET', 'POST'])
def threshold():
    if request.method == 'POST':

        # Para a imagem enviada
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado!', 'error')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Nenhuma imagem selecionada para upload!', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f') # Timestamp com data, hora e milissegundos
            file_extension = os.path.splitext(file.filename)[1]  # Extrai a extensão original
            filename = f"{timestamp}{file_extension}"  # Combina o timestamp com a extensão
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Para valor de threshold enviado
            threshold_value = request.form.get('threshold-value', None)
            print(f"Imagem '{filename}' enviada com sucesso!")
            print(f"Valor do Threshold recebido: {threshold_value}")

            return render_template('threshold.html', filename=filename)

        else:
            flash('Tipos permitidos: png, jpg, jpeg', 'error')
            return redirect(request.url)

    return render_template('threshold.html')       

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('O arquivo enviado excede o limite permitido de 16 MB!', 'error')
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # print('displaying: ' + filename)
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


# Inicializador da aplicação 
if __name__ == '__main__':
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    app.run(debug=True)