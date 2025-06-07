from flask import Flask, render_template, request, flash
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Autenticação com Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

app.secret_key = 'sedel123'

#Virtual
#credenciais_dict = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
#creds = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, scope
# Local
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)
sheet = client.open("FormularioUsuarios").sheet1  # Nome da planilha

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        if nome and email and telefone:
            sheet.append_row([nome, email, telefone])
            flash("Dados enviados com sucesso!", "sucesso")
        else:
            flash("Erro: preencha todos os campos!", "erro")

    return render_template('formulario.html')


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)