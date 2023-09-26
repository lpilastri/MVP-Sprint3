from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Boi, Peso                                              
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="MVP API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
boi_tag = Tag(name="Boi", description="Adição, visualização e remoção de bois à base")
peso_tag = Tag(name="Pesos", description="Adição de um peso à um boi cadastrado na base")
clima_tag = Tag(name="Clima", description="Apresenta inforções sobre o clima no dia atual")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/boi', tags=[boi_tag],
          responses={"200": BoiViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_boi(form: BoiSchema):
    """Adiciona um novo Boi à base de dados

    Retorna uma representação dos bois e pesos associados.
    """
    boi = Boi(            
        brinco=form.brinco,
        raca=form.raca,
        comentario=form.comentario)
    logger.debug(f"Adicionando boi com o brinco de identificação: '{boi.brinco}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando boi
        session.add(boi)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado boi de brinco: '{boi.brinco}'")
        return apresenta_boi(boi), 200

    except IntegrityError as e:
        # como a duplicidade do brinco é a provável razão do IntegrityError
        error_msg = "Brinco cadastrado ja foi utilizado :/"
        logger.warning(f"Erro ao adicionar Boi '{boi.brinco}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo boi :/"
        logger.warning(f"Erro ao adicionar boi '{boi.brinco}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/bois', tags=[boi_tag],
         responses={"200": ListagemBoiSchema, "404": ErrorSchema})
def get_bois():
    """Faz a busca por todos os Bois cadastrados

    Retorna uma representação da listagem de bois.
    """
    logger.debug(f"Coletando bois ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    bois = session.query(Boi).all()

    if not bois:
        # se não há bois cadastrados
        return {"bois": []}, 200
    else:
        logger.debug(f"%d bois econtrados" % len(bois))
        # retorna a representação do boi
        print(bois)
        return apresenta_bois(bois), 200


@app.get('/boi', tags=[boi_tag],
         responses={"200": BoiViewSchema, "404": ErrorSchema})
def get_boi(query: BoiBuscaSchema):
    """Faz a busca por um Boi a partir do brinco do mesmo

    Retorna uma representação dos Bois e Pesos associados.
    """
    boi_brinco = query.brinco
    logger.debug(f"Coletando dados sobre Boi #{boi_brinco}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    boi = session.query(Boi).filter(Boi.brinco == boi_brinco).first()

    if not boi:
        # se o boi não foi encontrado
        error_msg = "Boi não encontrado na base :/"
        logger.warning(f"Erro ao buscar brinco '{boi_brinco}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Boi econtrado: '{boi.brinco}' '{boi.raca}' ")
        # retorna a representação do Boi
        return apresenta_boi(boi), 200


@app.delete('/boi', tags=[boi_tag],
            responses={"200": BoiDelSchema, "404": ErrorSchema})
def del_boi(query: BoiBuscaSchema):
    """Deleta um Boi a partir do brinco informado

    Retorna uma mensagem de confirmação da remoção.
    """
    boi_brinco = query.brinco
    logger.debug(f"Deletando dados sobre Boi #{boi_brinco}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Boi).filter(Boi.brinco == boi_brinco).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado Boi #{boi_brinco}")
        return {"mesage": "Boi removido", "brinco": boi_brinco}
    else:
        # se o Boi não foi encontrado
        error_msg = "Boi não encontrado na base :/"
        logger.warning(f"Erro ao deletar Boi #'{boi_brinco}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.put('/boi', tags = [boi_tag])
def put_boi(query: BoiBuscaSchema,form: BoiSchemaPut):
    """Mostra informações sobre o clima no dia atual
    """
    boi = Boi( 
        brinco=query.brinco,
        raca=form.raca,
        comentario=form.comentario)
    boi_brinco = query.brinco
    logger.debug(f"Alterando dados sobre Boi #{boi_brinco}")
    # criando conexão com a base
    session = Session()
    # fazendo a alteração
    existing_boi = session.query(Boi).filter(Boi.brinco == boi_brinco).one_or_none()

    if existing_boi:
        update_boi = boi
        existing_boi = update_boi
        session.merge(existing_boi)
        session.commit()
        return{"mesage": "Boi alterado", "brinco": boi_brinco}
    else:
        # se o Boi não foi encontrado
        error_msg = "Boi não encontrado na base :", boi_brinco
        logger.warning(f"Erro ao alterar Boi #'{boi_brinco}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.post('/peso', tags=[peso_tag],
          responses={"200": BoiViewSchema, "404": ErrorSchema})
def add_peso(form: PesoSchema):
    """Adiciona de um novo peso ao boi cadastrado na base identificado pelo brinco

    Retorna uma representação dos bois e pesos associados.
    """
    boi_brinco  = form.brinco_referencia
    logger.debug(f"Adicionando peso ao boi #{boi_brinco}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo boi
    boi = session.query(Boi).filter(Boi.brinco == boi_brinco).first()

    if not boi:
        # se o boi não for encontrado
        error_msg = "Boi não encontrado na base :/"
        logger.warning(f"Erro ao adicionar um peso ao boi '{boi_brinco}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o peso
    valor = form.valor
    data_pesagem = form.data_pesagem
    peso = Peso(valor,data_pesagem)

    # adicionando o peso ao boi
    boi.adiciona_peso(peso)
    session.commit()

    logger.debug(f"Adicionado peso ao boi #{boi_brinco}")

    # retorna a representação de Boi
    return apresenta_boi(boi), 200
    
    
@app.delete('/peso', tags=[peso_tag],
           responses={"200": PesoDelSchema, "404": ErrorSchema})
def delete_peso(query: PesoBuscaSchema):
    """Remove um peso de um boi cadastrado na base identificado pelo id

    Retorna uma mensagem de confirmação da remoção.
    """
    peso_id = query.id
    logger.debug(f"Deletando dados sobre o peso ID #{peso_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Peso).filter(Peso.id == peso_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletad Peso #{print}")
        return {"mesage": "Peso removido", "ID": peso_id}
    else:
        # se o peso não foi encontrada
        error_msg = "Peso não encontrada na base :/"
        logger.warning(f"Erro ao deletar peso #'{peso_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    
    
@app.get('/pesos', tags=[peso_tag],
         responses={"200": ListagemPesoSchema, "404": ErrorSchema})
def get_pesos():
    """Faz a busca por todas os Pesos cadastradas

    Retorna uma representação da listagem de pesos.
    """
    logger.debug(f"Coletando bois ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pesos = session.query(Peso).all()

    if not pesos:
        # se não há bois cadastrados
        return {"Bois": []}, 200
    else:
        logger.debug(f"%d Pesos cadastrados" % len(pesos))
        # retorna a representação de bois
        print(pesos)
        return apresenta_pesos(pesos), 200                                          
