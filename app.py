from flask import Flask, render_template, request, url_for, redirect
import google.generativeai as genai
from dotenv import load_dotenv
import os
import csv

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')


@app.route('/', methods=['GET'])
def home():
    return render_template('inicio.html')

@app.route('/equipe')
def equipe():
    return render_template('equipe.html')

@app.route('/fundamentos')
def fundamentos():
    return render_template('fundamentos.html')

@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    with open('bd_glossario.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for t in reader:
            glossario_de_termos.append(t)

    return render_template('dicionario.html', glossario=glossario_de_termos, editar_id=None)


@app.route('/novo_termo', methods=['GET'])
def novo_termo():
    return render_template('novo_termo.html')

@app.route('/criar_termo', methods=['POST'])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open('bd_glossario.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


    return render_template('novo_termo.html')

@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)

    # Remover a linha correspondente ao termo_id
    if 0 <= termo_id < len(linhas):
        del linhas[termo_id]

    with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(linhas)

    return redirect(url_for('glossario'))

@app.route('/editar_termo/<int:termo_id>', methods=['POST'])
def editar_termo(termo_id):
    novo_termo = request.form['termo']
    nova_definicao = request.form['definicao']

    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)

    if 0 <= termo_id < len(linhas):
        linhas[termo_id] = [novo_termo, nova_definicao]

    with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(linhas)

    return redirect(url_for('glossario'))

@app.route('/editar_linha/<int:termo_id>')
def editar_linha(termo_id):
    glossario_de_termos = []
    with open('bd_glossario.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for linha in reader:
            glossario_de_termos.append(linha)

    return render_template('dicionario.html', glossario=glossario_de_termos, editar_id=termo_id)



#Config Generative AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-2.0-flash')

@app.route('/perguntas', methods=['GET'])
def perguntas():
    return render_template('perguntas.html')

@app.route('/responder', methods=['POST'])
def responder():
    pergunta = request.form['pergunta']
    resposta = ""

    try:
        # Envia a pergunta para o modelo Gemini
        response = model.generate_content(pergunta)
        resposta = response.text
    except Exception as e:
        resposta = f"Erro ao gerar resposta: {str(e)}"

    return render_template('perguntas.html', resposta=resposta)

@app.route('/header')
def header():
    return render_template('header.html')

app.run(debug=True)
