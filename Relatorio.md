# Relatório da construção da página

Neste documento pretendo apresentar em detalhes o processo de construção dessa página

---

- [Relatório da construção da página](#relatório-da-construção-da-página)
  - [Introdução](#introdução)
  - [Criação da página com Flask](#criação-da-página-com-flask)
  - [Construção da página](#construção-da-página)
  - [Upload do site](#upload-do-site)
    - [SSH e SCP](#ssh-e-scp)
    - [Envio de chave para o servidor](#envio-de-chave-para-o-servidor)
  - [Debugging](#debugging)
  - [Provisionamento do servidor](#provisionamento-do-servidor)
    - [WSGI](#wsgi)
    - [Gunicorn](#gunicorn)
    - [Nginx](#nginx)
  - [Deploy e problemas...](#deploy-e-problemas)
  - [Conclusão e comentários](#conclusão-e-comentários)
    - [Conclusão](#conclusão)
    - [Comentários](#comentários)

---


## Introdução

A primeira decisão tomada foi de que o site funcionaria com Flask. A escolha desse framework possibilitaria o uso de python e facilitaria a criação de apps dentro do próprio site, que também servirá, num futuro próximo, como meu portfólio pessoal.

O uso de flask demanda de um serviço de computação em nuvem visto que a página deve ser acessada externamente. Para hospedar a página foi necessária a criação de um servidor específico. O serviço escolhido para este trabalho foi o da **Linode** pois oferecia $100 por dois meses para o uso de suas ferramentas de computação em nuvem, tempo suficiente para a entrega do trabalho. Também será necessário criar um servidor *WSGI* que possa rodar o flask *"em produção"*, fora do modo *debug*

O layout da página foi escolhido através de pesquisas na internet. Um dos requisitos é que a página não fosse um "poster estático", então optei por um layout multi-páginas, o que demandou um pouco de estudo a respeito de HTML e CSS para ajustes no modelo escolhido.

Por fim, finalizando o desafio, a página foi provisionada no servidor na nuvem e poderá ser acessada até a avaliação por parte do professor, mas seu projeto está salvo e disponível em um [repositório no Github](https://github.com/guitoscan/site_infcomp)

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

## Upload do site

Após a construção do *front-end* estar pronto, era necessário providenciar um local para publicar a página. 

O primeiro passo foi adquirir um domínio (www.guitoscansilva.site) na plataforma ***GoDaddy*** e em seguida criar uma conta na **Linode**, plataforma que fornece o serviço de computação em nuvem (e ofereceu US$100 para utilizar seus serviços por 60 dias). Na ***GoDaddy*** redirecionei os servidores de DNS para os servidores da **Linode** apenas por precaução.

### SSH e SCP

Para acessar a máquina remota criada na **Linode** foi necessário utilizar SSH. Após as configurações básicas do python para rodar o site em ambiente de teste foi necessário fazer o upload dos arquivos para o servidor e neste caso foi utilizado o SCP (porque vacilei nesse momento e já poderia estar utilizando o github).

Apenas como anedota, me habituei a utilizar o "ESC" + :wq" do VIM devido as correções que tive que fazer no códigos do servidor. 

### Envio de chave para o servidor

Outro ponto que vale destacar foi o envio da minha chave pública para o servidor.

Utilizei a mesma chave criada par o Github e enviei para o servidor usando o comando:

> ssh-copy-id [user]@[ip-address]

Ficou mais fácil logar no servidor através da chave =D

## Debugging

Neste momento o site já rodava em modo de Debugging no servidor. Já era possível acessar e testar as páginas e os links através da porta 5000 (o Flask provisiona um servidor para testes utilizando os IPs locais e externo da máquina, mas "printa" em vermelho durante a execução que não deve ser usado em produção. O servidor de testes do Flask não é escalável e, principalmente, não é seguro). 

Com o site funcionando, inclusive o disparo de emails para contato, é possível provisionar um servidor para publicar a página.



## Provisionamento do servidor

Verificando próprio output do Flask e pesquisando alguns tutoriais na rede, optei por utilizar a "trinca" WSGI + Gunicorn + Nginx para publicar a página

### WSGI

Também chamada de "Uisgui", segundo a [wikipédia](https://pt.wikipedia.org/wiki/Web_Server_Gateway_Interface), o WSGI é um protocolo de interface entre servidores web e aplicações web desenvolvida para Python, ou seja, no caso da página é ele quem faz a interface entre o código e o servidor web (que será o Gunicorn). 

O código escrito para o arquivo .py é bem simples  

```python
from WebPage import app

if __name__ == "__main__":
    app.run()

```

### Gunicorn

O Gunicorn (*"Green Unicorn"*) é um servidor web baseado em Python. No caso do site ele é o responsável por receber as requisições via HTTP e, através da WSGI, entregar à aplicação em Flask, assim como retorna as informações da aplicação via HTTP.

Para utilizar no projeto foi necessária a criação de um ambiente em Python com todas as bibliotecas necessárias, além da criação de um *service* no servidor para manter o Gunicorn sempre operacional.



```bash
[Unit]
Description=Gunicorn instance to serve site Flask app
After=network.target

[Service]
User=guilherme
Group=www-data
WorkingDirectory=/home/guilherme/site_infcomp/site
Enviroment="PATH=/home/guilherme/env/producao/bin"
ExecStart=/home/guilherme/env/producao/bin/gunicorn --workers 3 --bind unix:site.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target

```

### Nginx

O Nginx também é um servidor web, mas neste caso é utilizado como um "proxy reverso", fazendo a interface entre a internet e o Gunicorn 

O Nginx foi instalado no servidor e criado um arquivo de configuração em /etc/nginx/sites-avaliable/

Como é possível perceber, neste arquivo é configurado o endereço da página

```bash
server {
	listen 80;
	server_name guitoscansilva.site www.guitoscansilva.site;

	location / {
		include proxy_params;
		proxy_pass http://unix:/home/guilherme/site_infcomp/site/site.sock;
	}
}

```



## Deploy e problemas...

O deploy ocorreu quase como esperado. Neste ponto já estava utilizando o github para realizar alterações nos código (como pode ser visto nesse repositório), mas houve um problema o qual não foi possível encontrar solução em tempo hábil.

O site originalmente deveria contar com um campo para "Contato", onde o visitante poderia preencher seus dados e enviar uma mensagem, mas depois do deploy essa funcão simplesmente parou de funcionar.

Devido ao prazo apertado a solução foi retirar essa função do site, que provavelmente irá figurar numa nova versão da página.

> O código para a função de email segue no repositório, mas os blocos de código relativos a ela estão comentados. 



## Conclusão e comentários

### Conclusão 

O objetivo deste projeto era apresentar uma página web funcional e que aplicasse os diversos conhecimentos adquiridos através da aulas de Estrutura de Computadores II. Como é possível verificar abaixo, quase todos, senão todos, os tópicos foram abordados na construção da página:

- Criação de um servidor na nuvem
- Acesso e transferência de arquivos ao servidor remoto
  - SSH e SCP via IP e domínio
- Operações via terminal 
- Criação de um repositório no Github 
  - com chave SSH
- Criação de um domínio e alteração do DNS
- Criação de uma estrutura para servidor HTTP
  - WSIG + Gunicorn + Gninx
- Criação de uma aplicação em Flask (Python)

Quanto ao resultado do projeto, o site se encontra funcional e navegável e será mantido online até a avaliação.

### Comentários

Abaixo estão alguns pontos para melhoria numa possível nova versão do site:

- Implementar a função de contato (Flask)
- Melhorar o layout de algumas páginas (CSS + HTML)
- Adicionar mais animações (JavaScript)
- Melhorar a segurança da página (Flask + Servidores Web)