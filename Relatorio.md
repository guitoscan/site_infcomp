# Relatório da construção da página

Neste documento pretendo apresentar em detalhes o processo de construção dessa página

---

- [Relatório da construção da página](#relatório-da-construção-da-página)
  - [Introdução](#introdução)
  - [Criação da página com Flask](#criação-da-página-com-flask)
  - [Construção da página](#construção-da-página)
  - [Criação do app de email](#criação-do-app-de-email)

---


## Introdução

A primeira decisão tomada é de que o site funcionaria com Flask. A escolha desse framework possibilitaria o uso de python e facilitaria a criação de apps dentro do próprio site, que também servirá, num futuro próximo, como meu portfólio pessoal.

O uso de flask demanda de um serviço de computação em nuvem visto que a página deve ser acessada externamente. Para hospedar a página foi necessária a criação de um servidor específico. O serviço escolhido para este trabalho foi o da **Linode**, que oferecia $100 por dois meses para o uso de suas ferramentas de computação em nuvem. Também será necessário criar um servidor *WSGI* que possa rodar o flask *"em produção"*, fora do modo *debug*

O layout da página foi escolhido através de pesquisas na internet. Um dos requisitos é que a página não fosse um "poster estático", então optei por um layout multi-páginas, o que demandou um pouco de estudo a respeito de HTML e CSS para ajustes no modelo escolhido.

Por fim, outros objetivo foi o de rotear via DNS o endereço de ip da máquina virtual criada através do domínio adquirido (www.guitoscansilva.site)

## Criação da página com Flask

O Flask é um framework de desenvolvimento web que gerencia os diversos arquivos referentes a página. Nele é possível utilizar em conjuntos arquivos típicamente web (HTML e formatações em CSS) com arquivos python e dessa forma embarcar aplicativos nas páginas.

Um diretório simples de flask conta com o arquivo .py e duas pastas, a *"template"* onde ficam as páginas em HTML e a *"static"* onde ficam os aquivos JS, CSS e as imagens.

Um arquivo simples em flask possui a estrutura abaixo:

```python

from flask import Flask, render_template, 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port = "5000")           

```
O arquivo final pode ser visto neste repositório com o nome **"WebPage.py"**

## Construção da página

A construção da página envolveu alterar alguns arquivos de HTML e CSS para que a formação ficasse de acordo com o desejado. 

Além disso houve a necessidade de adequar o modelo baixado ao formato de diretórios do Flask, e consequentemente alterar as referências dentro dos arquivos HTLM. 

Houve uma pequena dificuldade no começo, mas devido ao conhecimento básico com lógica de programação, a curva de aprendizagem foi bem inclinada e não houveram muitos problemas nesta etapa

## Criação do app de email

Esta etapa foi uma das mais sensíveis do processo. Dentro do arquivo Flask foi criada uma rota que dispara um email assim que o formulário de contato é preenchido. 

O Flask possui bibliotecas que dão suporte para essa tarefa, porém é necessário fornecer uma conta de email e uma senha para que o envio seja realizado.

Como a primeira versão dessa página ficará no ar por pouco tempo, a solução adotada foi colocar as variáveis "email" e "senha" em um arquivo "config.py" para ser acessado durante a execução do código. Também foi criada uma conta de email Gmail com *2fa* e uma *"senha de aplicativo"* que irá permitir o disparo. 

Neste respositório o arquivo "config.py" conta com valores genéricos, mas em produção os valores são os reais. 

```python

## config.py
## Inserir informações quando realizar o deploy

email = str('email@gmail.com') 
senha = str("AppPassword")

```
















