from flask import Blueprint, render_template

# Criando um Blueprint para as rotas da aplicação 
# Blueprints são uma maneira de deixar o projeto mais modularizado
main = Blueprint('main', __name__)

# Definindo a rota principal para a página home
@main.route('/')
def home_page():
    return render_template('home.html')

# Definindo a rota /threshold para a página threshold
@main.route('/threshold')
def threshold_page():
    return render_template('threshold.html')