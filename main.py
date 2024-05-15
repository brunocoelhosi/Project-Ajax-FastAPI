from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import CONN, Pessoa, Tokens
from secrets import token_hex
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from hashlib import sha256 

app = FastAPI()


#origins = ["*"]
origins = ["http://127.0.0.1:8001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def conectaBanco():
    engine = create_engine(CONN, echo = True)
    Session = sessionmaker(bind = engine)
    return Session()

@app.post('/cadastro')
def cadastro(nome: str, usr: str, senha: str):

    senha = sha256(senha.encode()).hexdigest()

    session = conectaBanco()

    usuario = session.query(Pessoa).filter_by(usuario=usr, senha=senha).all()
    if len(usuario) == 0:
        x = Pessoa(nome = nome, usuario = usr, senha = senha)
        session.add(x)
        session.commit()
        return {'status': 0}
    elif len(usuario) > 0:
        return {'status': 2}


@app.post('/login')
def login(usr:str, senha:str):

    senha = sha256(senha.encode()).hexdigest()

    session = conectaBanco()

    usuario = session.query(Pessoa).filter_by(usuario=usr, senha=senha).all()
    if len(usuario)==0:
        return {'status': 5}
    while True:
        token = token_hex(50)
        tokenExiste = session.query(Tokens).filter_by(token=token).all()
        if len(tokenExiste) == 0:
            pessoaExiste = session.query(Tokens).filter_by(id_Pessoa=usuario[0].id).all()
            if len(pessoaExiste) == 0:
                novoToken = Tokens(id_Pessoa=usuario[0].id, token=token)
                session.add(novoToken)
            elif len(pessoaExiste) > 0:
                pessoaExiste[0].token = token
            
            session.commit()
            break
    #return token
    return{'status': 0}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, access_log=False)