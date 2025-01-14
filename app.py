from flask import Flask, render_template, request
import logging
import socket  # Para obter informações do servidor

# Configuração da aplicação Flask
app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal que exibe o formulário para conversão de unidades de medida.
    """
    # Obter informações do servidor
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    if request.method == 'GET':  
        # Exibe a página inicial com informações do servidor
        return render_template('index.html', hostname=hostname, ip_address=ip_address)
    else:
        # Capturar os valores enviados pelo formulário
        unidade_selecionada = request.form.get('selectTemp')
        valor_referencia = request.form.get('valorRef')

        try:
            # Tentar converter o valor para float
            valor_referencia = float(valor_referencia)
        except ValueError:
            # Retorna um erro caso o valor seja inválido
            return render_template(
                'index.html', 
                conteudo={'unidade': 'Inválido', 'valor': 'Entrada inválida. Por favor, insira um número válido.'}, 
                hostname=hostname, 
                ip_address=ip_address
            )

        # Lógica de conversão baseada na seleção do usuário
        if unidade_selecionada == '1':  # Metro para Quilômetros
            resultado = valor_referencia / 1000
            unidade = "quilômetros"
        elif unidade_selecionada == '2':  # Quilômetros para Metro
            resultado = valor_referencia * 1000
            unidade = "metros"
        elif unidade_selecionada == '3':  # Metro para Milhas
            resultado = valor_referencia / 1609.34
            unidade = "milhas"
        elif unidade_selecionada == '4':  # Milhas para Metro
            resultado = valor_referencia * 1609.34
            unidade = "metros"
        elif unidade_selecionada == '5':  # Metro para Pés
            resultado = valor_referencia * 3.28084
            unidade = "pés"
        elif unidade_selecionada == '6':  # Pés para Metro
            resultado = valor_referencia / 3.28084
            unidade = "metros"
        else:
            # Caso a opção selecionada seja inválida
            resultado = "Inválido"
            unidade = ""

        # Renderizar o resultado na página inicial
        return render_template(
            'index.html', 
            conteudo={'unidade': unidade, 'valor': resultado}, 
            hostname=hostname, 
            ip_address=ip_address
        )

if __name__ == '__main__':
    # Executa o servidor Flask na porta 5000 e em todos os endereços
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    # Configuração de logging para produção (Gunicorn)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

