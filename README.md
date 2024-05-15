Sistema de Cadastro de Usuários, utilizando Ajax e FastAPI

Run Back-End

FastAPI3

uvicorn main:app --reload

Run Front-End

cd FastAPI3Front

pip install waitress

waitress-serve --listen=127.0.0.1:8001 server:app
