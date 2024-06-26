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
      arrayTipoNota = ['nfe', 'nfce', 'nfse', 'mdfe', 'cte', 'compras'];
      tabelas = ''
      intervalo = ''
      id_cliente = request.form.get('cliente')
      numero_card = request.form.get('numero_card')

      for tipoNota in arrayTipoNota:
            if request.form.get(f'checkbox_card_{tipoNota}') != None:
                tabelas += f"const {tipoNota.upper()}_TABLE = '{request.form.get(f'checkbox_card_{tipoNota}')}'; \n"
                if request.form.get(f'intervalo_notas_{tipoNota}') == 'intervalo':
                       inicio = request.form.get(f"input_inicio_{tipoNota}")
                       fim = request.form.get(f"input_fim_{tipoNota}")
                       intervalo += f"const {tipoNota}_INTERVAL = [{inicio}, {fim}];"
      
      return f"""
      
<?php
    use Illuminate\\Database\\Migrations\\Migration; 
    use Illuminate\\Database\\Schema\\Blueprint;
    use Illuminate\\Support\\Facades\\Schema;
    use Illuminate\\Support\\Facades\\DB;

    class ScriptLeg{numero_card}ExclusaoNotasCliente{id_cliente} extends Migration 
    {{ 
        const CLIENTE = {id_cliente};
        {tabelas}
        const NFE_INTERVAL = [1, 10];

        public function up(){{ 
            // NFE
            DB::table(self::NFE_TABLE)
                ->where('id_empresa', '=', self::CLIENTE)
                ->whereBetween('id_pedido', self::NFE_INTERVAL)
                ->update(['lixeira' => 'Sim']);
        }}

        public function down()
        {{
            //NFE
            DB::table(self::NFE_TABLE)
                ->where('id_empresa', '=', self::CLIENTE)
                ->whereBetween('id_pedido', self::NFE_INTERVAL)
                ->update(['lixeira' => 'Nao']);                        
        }}
    }}
   
    """

if __name__ == "__main__":
	app.run()