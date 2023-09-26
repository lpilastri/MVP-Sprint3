from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base

class Peso(Base):
    __tablename__ = 'peso'

    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())
    data_pesagem = Column(String(10))
    # Definição do relacionamento entre o Boi e o Brinco.
    brinco_referencia = Column(Integer, ForeignKey("boi.brinco"), nullable=False)

    def __init__(self, valor:float, data_pesagem:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Pesagem

        Arguments:
            valor: peso em Kgs.
            data_insercao: data de quando o peso foi inserido à base
            data_pesagem: data da pesagem, informada pelo usuario
        """
        self.valor = valor
        self.data_pesagem = data_pesagem
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

