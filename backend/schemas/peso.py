from pydantic import BaseModel
from typing import List
from model.peso import Peso


class PesoSchema(BaseModel):
    """ Define como um novo cadastro de peso a ser inserido deve ser representado
    """
    brinco_referencia: int = 1
    valor: float = 450
    data_pesagem: str = "10/11/2022"
    
class PesoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no numero do brinco.
    """
    id: int = 1
    
class PesoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str    
    
class ListagemPesoSchema(BaseModel):
    """ Define como uma listagem de Bois será retornada.
    """
    peso:List[PesoSchema]
    
def apresenta_pesos(pesos: List[Peso]):
    """ Retorna uma representação de Venda seguindo o schema definido em
        VendaViewSchema.
    """
    result = []
    for peso in pesos:
        result.append({
            "id": peso.id,
            "brinco": peso.brinco_referencia,
            "peso": peso.valor,
            "data_pesagem": peso.data_pesagem,
        })

    return {"pesos": result}