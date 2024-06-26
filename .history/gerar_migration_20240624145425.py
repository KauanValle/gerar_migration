from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('gerar_migration_html.html')

@app.route('/teste')
def teste():
      nome = request.form.get('numero_card')
      return nome;


if __name__ == "__main__":
	app.run()