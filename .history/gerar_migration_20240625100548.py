from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('gerar_migration_html.html')

@app.route('/gerar-migration', methods=['POST'])
def gerarMigration():
    gerarArquivoMigration()
    return redirect('/')


def gerarMigrationHtml():
      arrayTipoNota = ['nfe', 'nfce', 'nfse', 'mdfe', 'cte', 'compras'];
      id_cliente = request.form.get('cliente')
      numero_card = request.form.get('numero_card')
      tabelas = ''
      intervalo = ''\
      codigo_up = ''
      codigo_down = ''

      for tipoNota in arrayTipoNota:
            if request.form.get(f'checkbox_card_{tipoNota}') != None:
                tipoNotaUpper = tipoNota.upper()
                tabelas += f"const {tipoNotaUpper}_TABLE = '{request.form.get(f'checkbox_card_{tipoNota}')}'; \n        "
                if request.form.get(f'intervalo_notas_{tipoNota}') == 'intervalo':
                    inicio = request.form.get(f"input_inicio_{tipoNota}")
                    fim = request.form.get(f"input_fim_{tipoNota}")
                    intervalo += f"const {tipoNotaUpper}_INTERVAL = [{inicio}, {fim}]; \n        "
                    codigo_up += codigoUpIntervalo(tipoNotaUpper)
                    codigo_down += codigoDownIntervalo(tipoNotaUpper)

                if request.form.get(f'intervalo_notas_{tipoNota}') == 'unica':
                    unica = request.form.get(f"input_unica_{tipoNota}")
                    intervalo += f"const {tipoNotaUpper}_ID = {unica};"
                    codigo_up += codigoUpUnica(tipoNotaUpper)
                    codigo_down += codigoDownUnica(tipoNotaUpper)

                if request.form.get(f'intervalo_notas_{tipoNota}') == 'todas':
                    codigo_up += codigoUpTodas(tipoNotaUpper)
                    codigo_down += f"""
                    DB::table(self::{tipoNotaUpper}_TABLE)
                        ->where('id_empresa', '=', self::CLIENTE)
                        ->update(['lixeira' => 'Nao']);          
                    """
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
        {intervalo}
        public function up(){{ 
            {codigo_up}
        }}

        public function down()
        {{
            {codigo_down}              
        }}
    }}
   
    """

def gerarArquivoMigration():
    arquivo = open("./migrations/script/teste5.php", 'w')

    caminho_pasta = 'C:\\Users\\kauan\OneDrive\\Documentos\\Python\\gerar_migration\\migrations\\script'
    arquivos = [os.path.join(caminho_pasta, f) for f in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, f))]
    if not arquivos:
        print("A pasta está vazia.")
    else:
        ultimo_arquivo = max(arquivos, key=os.path.getmtime)
        print(f"O último arquivo é: {ultimo_arquivo}")

        with open(ultimo_arquivo, 'r+') as arquivo:
            arquivo.seek(0)
            novo_conteudo = gerarMigrationHtml()
            arquivo.write(novo_conteudo)
            arquivo.truncate()

def codigoUpUnica(tipoNotaUpper):
    return f"""
        DB::table(self::{tipoNotaUpper}_TABLE)
            ->where('id_empresa', '=', self::CLIENTE)
            ->where('id_pedido', self::{tipoNotaUpper}_ID)
            ->update(['lixeira' => 'Sim']);
        """
     
def codigoDownUnica(tipoNotaUpper):
    return f"""
        DB::table(self::{tipoNotaUpper}_TABLE)
            ->where('id_empresa', '=', self::CLIENTE)
            ->where('id_pedido', self::{tipoNotaUpper}_ID)
             ->update(['lixeira' => 'Nao']);          
        """

def codigoUpIntervalo(tipoNotaUpper):
    return f"""
        DB::table(self::{tipoNotaUpper}_TABLE)
            ->where('id_empresa', '=', self::CLIENTE)
            ->whereBetween('id_pedido', self::{tipoNotaUpper}_INTERVAL)
            ->update(['lixeira' => 'Sim']);
        """

def codigoDownIntervalo(tipoNotaUpper):
    return f"""
        DB::table(self::{tipoNotaUpper}_TABLE)
            ->where('id_empresa', '=', self::CLIENTE)
            ->whereBetween('id_pedido', self::{tipoNotaUpper}_INTERVAL)
            ->update(['lixeira' => 'Nao']);          
        """

def codigoUpTodas():
     

def codigoDownTodas():

if __name__ == "__main__":
	app.run()