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
      id_cliente = request.form.get('cliente')
      for tipoNota in arrayTipoNota:
            if request.form.get(f'checkbox_card_{tipoNota}') != None:
                tabelas += f"const {tipoNota.upper()}_TABLE = '{tipoNota}'; \n"
                  
      
      return f"""
      
<?php
    use Illuminate\\Database\\Migrations\\Migration; 
    use Illuminate\\Database\\Schema\\Blueprint;
    use Illuminate\\Support\\Facades\\Schema;
    use Illuminate\\Support\\Facades\\DB;

    class ScriptLeg123ExclusaoNotasCliente123 extends Migration 
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