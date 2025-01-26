import os
from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

# Criando aplicação e definindo diretórios importantes
app = Flask(__name__, 
    template_folder='app/templates',
    static_folder='app/static',
)

# Configurações da aplicação
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 

# Definindo onde arquivos de upload devem ser armazenados
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Definindo tamanho máximo permitido para uploads
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH   
app.secret_key = 'secret_key'

# Função para verificar se o arquivo é permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----- Página principal -----
@app.route('/')
def home():
    return render_template('home.html')

# ----- Página de segmentação por limiarização -----
@app.route('/threshold', methods=['GET', 'POST'])
def threshold():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado!', 'error')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Nenhuma imagem selecionada para upload!', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Imagem enviada com sucesso!', 'success')
            return redirect(url_for('threshold'))

        else:
            flash('Tipos permitidos: png, jpg, jpeg', 'error')
            return redirect(request.url)

    return render_template('threshold.html')       

# Inicializador da aplicação 
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)