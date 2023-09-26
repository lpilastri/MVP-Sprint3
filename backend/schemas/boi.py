from pydantic import BaseModel
from typing import Optional, List
from model.boi import Boi

from schemas import PesoSchema


class BoiSchema(BaseModel):
    """ Define como um novo boi adquirido deve ser representado
    """
    brinco: int = 1
    raca: str = "Nelore"
    comentario: str = "Boi adiquirido da fazenda x"

class BoiSchemaPut(BaseModel):
    """ Define como um novo boi adquirido deve ser representado
    """
    raca: str = "Nelore"
    comentario: str = "Boi adiquirido da fazenda x"

class BoiBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no brinco do boi.
    """
    brinco: int = 1


class ListagemBoiSchema(BaseModel):
    """ Define como uma listagem de bois será retornada.
    """
    bois:List[BoiSchema]


def apresenta_bois(bois: List[Boi]):
    """ Retorna uma representação do boi seguindo o schema definido em
        BoiViewSchema.
    """
    result = []
    for boi in bois:
        result.append({
            "brinco": boi.brinco,
            "raca": boi.raca,
            "comentario": boi.comentario,
        })

    return {"bois": result}


class BoiViewSchema(BaseModel):
    """ Define como um boi será retornado: Boi + Pesagens.
    """
    brinco: int = 1
    raça: str = "Nelore"
    comentario: Optional[str] = "Boi adiquirido da fazenda x"
    total_pesagens: int = 1
    pesos:List[PesoSchema]


class BoiDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_boi(boi: Boi):
    """ Retorna uma representação do boi seguindo o schema definido em
        BoiViewSchema.
    """
    return {
        "brinco": boi.brinco,
        "raca": boi.raca,
        "comentario": boi.comentario,
        "total_pesagens": len(boi.pesos),
        "pesos": [{"Valor": peso.valor} for peso in boi.pesos]
    }
