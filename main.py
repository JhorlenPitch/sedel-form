from flask import Flask, render_template, request, flash
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = 'sedel123'

# Escopo necessário para acessar o Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Autenticação com Google Sheets
try:
    if os.environ.get("GOOGLE_CREDENTIALS_JSON"):
        # Ambiente Render (credenciais via variável de ambiente)
        credenciais_dict = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, scope)
    else:
        # Ambiente local (arquivo físico)
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)

    client = gspread.authorize(creds)
    sheet = client.open("FormularioUsuarios").sheet1  # Nome da planilha

except Exception as e:
    raise RuntimeError(f"Erro na autenticação com Google Sheets: {e}")

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        campos = {
            'nome_atleta': request.form.get('nome_atleta'),
            'nome_responsavel': request.form.get('nome_responsavel'),
            'whatsapp_atleta': request.form.get('whatsapp_atleta'),
            'data_nascimento_atleta': request.form.get('data_nascimento_atleta'),
            'cpf_atleta': request.form.get('cpf_atleta'),
            'cep_atleta': request.form.get('cep_atleta'),
            'estado_atleta': request.form.get('estado_atleta'),
            'cidade_atleta': request.form.get('cidade_atleta'),
            'bairro_atleta': request.form.get('bairro_atleta'),
            'rua_atleta': request.form.get('rua_atleta'),
            'numero_atleta': request.form.get('numero_atleta'),
            'nucleo_atleta': request.form.get('nucleo_atleta'),
            'projeto': request.form.get('projeto')
        }

        if all(campo and campo.strip() != '' for campo in campos.values()):
            try:
                sheet.append_row(list(campos.values()))
                flash("✅ Cadastro enviado com sucesso!", "sucesso")
            except Exception as e:
                flash(f"❌ Erro ao enviar para planilha: {str(e)}", "erro")
        else:
            flash("❌ Por favor, preencha todos os campos obrigatórios.", "erro")

    return render_template('formulario_novo.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)