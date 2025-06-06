from flask import Flask, render_template, request
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
credenciais_dict = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("FormularioUsuarios").sheet1  # Nome da planilha


@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        sheet.append_row([nome, email, telefone])
        return "Dados enviados com sucesso!"

    return render_template('formulario.html')


if __name__ == '__main__':
    app.run(debug=True)
