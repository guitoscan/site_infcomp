#!/bin/python3

from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from config import email, senha


app = Flask(__name__)

app.secret_key = "super secret key"

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": email,
    "MAIL_PASSWORD": senha
}

app.config.update(mail_settings)
mail = Mail(app)


class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome,
        self.email = email,
        self.mensagem = mensagem

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/studies")
def studies():
    return render_template("studies.html")

@app.route("/project")
def project():
    return render_template("project.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/send', methods=['GET','POST'])
def send():
    if request.method == 'POST':
        formContato = Contato(
            request.form['nome'],
            request.form['email'],
            request.form['message']
        )

        msg = Message(
            subject = f'{formContato.nome} te enviou uma mensagem',
            sender = app.config.get("MAIL_USERNAME"),
            recipients = ['guitoscansilva@gmail.com'],
            body = f'''

            {formContato.nome}, email {formContato.email}, enviou uma
            mensagem pelo site

            segue a mensagem:

            {formContato.mensagem}

            '''
        )

        mail.send(msg)
        flash("Mensagem enviada com sucesso!")
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port = "5000", ssl_context='adhoc')           
