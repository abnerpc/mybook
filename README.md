Mybook project
==============

Mybook é um projeto Flask que fornece interfaces REST para salvar, listar e excluir detalhes de um usuário do Facebook.


Instalação e execução
=====================

Clone e instalação das dependências

```bash
$ git clone https://github.com/abnerpc/mybook.git
$ cd mybook
$ pip install -r requirements.txt
```

Execute

```bash
$ python run.py
```


Como usar
=========

Salvar detalhes de um usuário

> pode ser usado o username do usuário

```bash
curl -X POST -F facebookId=abnerpc http://localhost:5000/api/person/
```

> ou o facebook Id

```bash
curl -X POST -F facebookId=725876734 http://localhost:5000/api/person/
```

Listar os detalhes salvos

```bash
curl http://localhost:5000/api/person/
```

> limitando a quantidade de resultados

```bash
curl "http://localhost:5000/api/person/?limit=2"
```

Excluir um detalhe

```bash
curl -X DELETE http://localhost:5000/api/person/abnerpc
```


![python](https://www.python.org/static/community_logos/python-logo.png)
&nbsp;
![flask](http://flask.pocoo.org/static/badges/flask-powered.png)
