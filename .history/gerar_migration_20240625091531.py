from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('gerar_migration_html.html')

@app.route('/gerar-migration', methods=['POST'])
def gerarMigration():
    arquivo = open("./migrations/script/teste4.php", 'w')

    caminho_pasta = 'C:\Users\kauan\OneDrive\Documentos\Python\gerar_migration\migrations\script'
    arquivos = [os.path.join(caminho_pasta, f) for f in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, f))]
    if not arquivos:
        print("A pasta está vazia.")
    else:
        # Encontrar o arquivo mais recente
        ultimo_arquivo = max(arquivos, key=os.path.getmtime)

        # Exibir o caminho do último arquivo
        print(f"O último arquivo é: {ultimo_arquivo}")

        # Aqui, vamos supor que o arquivo é um texto e queremos editá-lo
        # Abrir o arquivo para leitura e escrita ('r+' permite ler e escrever)
        with open(ultimo_arquivo, 'r+') as arquivo:
            # Voltar para o início do arquivo para escrever o novo conteúdo
            arquivo.seek(0)

            # Editar o conteúdo (neste exemplo, adicionando uma linha ao final)
            novo_conteudo = gerarMigration()
            
            # Escrever o novo conteúdo
            arquivo.write(novo_conteudo)

            # Truncar o restante do arquivo se necessário
            arquivo.truncate()

            print("O arquivo foi editado com sucesso.")
    return redirect('/')


def gerarMigration():
      arrayTipoNota = ['nfe', 'nfce', 'nfse', 'mdfe', 'cte', 'compras'];
      tabelas = ''
      intervalo = ''
      id_cliente = request.form.get('cliente')
      numero_card = request.form.get('numero_card')
      codigo_up = ''
      codigo_down = ''

      for tipoNota in arrayTipoNota:
            if request.form.get(f'checkbox_card_{tipoNota}') != None:
                tabelas += f"const {tipoNota.upper()}_TABLE = '{request.form.get(f'checkbox_card_{tipoNota}')}'; \n        "
                if request.form.get(f'intervalo_notas_{tipoNota}') == 'intervalo':
                    inicio = request.form.get(f"input_inicio_{tipoNota}")
                    fim = request.form.get(f"input_fim_{tipoNota}")
                    intervalo += f"const {tipoNota.upper()}_INTERVAL = [{inicio}, {fim}]; \n        "

                    codigo_up += f"""
                    DB::table(self::{tipoNota.upper()}_TABLE)
                        ->where('id_empresa', '=', self::CLIENTE)
                        ->whereBetween('id_pedido', self::{tipoNota.upper()}_INTERVAL)
                        ->update(['lixeira' => 'Sim']);
                    """

                    codigo_down += f"""
                    DB::table(self::{tipoNota.upper()}_TABLE)
                        ->where('id_empresa', '=', self::CLIENTE)
                        ->whereBetween('id_pedido', self::{tipoNota.upper()}_INTERVAL)
                        ->update(['lixeira' => 'Nao']);          
                    """
                if request.form.get(f'intervalo_notas_{tipoNota}') == 'unica':
                    unica = request.form.get(f"input_unica_{tipoNota}")
                    intervalo += f"const {tipoNota.upper()}_ID = {unica};"
                    codigo_up += f"""
                    DB::table(self::{tipoNota.upper()}_TABLE)
                        ->where('id_empresa', '=', self::CLIENTE)
                        ->where('id_pedido', self::{tipoNota.upper()}_ID)
                        ->update(['lixeira' => 'Sim']);
                    """

                    codigo_down += f"""
                    DB::table(self::{tipoNota.upper()}_TABLE)
                        ->where('id_empresa', '=', self::CLIENTE)
                        ->where('id_pedido', self::{tipoNota.upper()}_ID)
                        ->update(['lixeira' => 'Nao']);          

                    """
                if request.form.get(f'intervalo_notas_{tipoNota}') == 'todas':
                    codigo_up += f"""
                    DB::table(self::{tipoNota.upper()}_TABLE)
                        ->where('id_empresa', '=', self::CLIENTE)
                        ->update(['lixeira' => 'Sim']);
                    """
                    codigo_down += f"""
                    DB::table(self::{tipoNota.upper()}_TABLE)
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

if __name__ == "__main__":
	app.run()