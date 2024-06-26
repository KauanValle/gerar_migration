from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('gerar_migration_html.html')

@app.route('/teste', methods=['POST'])
def teste():
      nome = request.form.get('numero_card')
      arquivo = open("teste.php", 'w')
      arquivo.write(gerarMigration())
      arquivo.close()
      return redirect('/')

def gerarMigration():
      return f'<?php
                use Illuminate\\Database\\Migrations\\Migration;
                use Illuminate\\Database\\Schema\\Blueprint;
                use Illuminate\\Support\\Facades\\Schema;
                use Illuminate\\Support\\Facades\\DB;
                class ScriptLeg123ExclusaoNotasCliente123 extends Migration 
                {{ const CLIENTE = 123;'

if __name__ == "__main__":
	app.run()