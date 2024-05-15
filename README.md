<h3>Sistema de Cadastro de Usuários, utilizando Ajax e FastAPI</h3>

<h4>Run Back-End</h4>

FastAPI3

uvicorn main:app --reload
<br>
<br>
<h4>Run Front-End</h4>

cd FastAPI3Front

pip install waitress

waitress-serve --listen=127.0.0.1:8001 server:app
