mybook project
==============

mybook é um projeto Flask que fornece interfaces REST para salvar, listar e excluir detalhes de um usuário do Facebook.

instalação
==========

1. clone e instalação das dependências

```bash
$ git clone https://github.com/abnerpc/mybook.git
$ cd mybook
$ pip install -r requirements.txt
```

2. run

```bash
$ python run.py
```


como usar
=========

1. salvar detalhes de um usuário

> pode ser usado o username do usuário

```bash
curl -X POST -F facebookId=abnerpc http://localhost:5000/api/person/
```

> ou o facebook Id

```bash
curl -X POST -F facebookId=725876734 http://localhost:5000/api/person/
```

2. listar os detalhes salvos

```bash
curl http://localhost:5000/api/person/
```

> limitando a quantidade de resultados

```bash
curl "http://localhost:5000/api/person/?limit=2"
```

3. excluir um detalhe

```bash
curl -X DELETE http://localhost:5000/api/person/abnerpc
```


![python](docs/python_powered.png)
&nbsp;
![flask](docs/flask_powered.png)
