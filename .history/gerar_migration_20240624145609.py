from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('gerar_migration_html.html')

@app.route('/teste', methods=['POST'])
def teste():
      nome = request.form.get('numero_card')
      print(nome)
      return redirect('/')


if __name__ == "__main__":
	app.run()