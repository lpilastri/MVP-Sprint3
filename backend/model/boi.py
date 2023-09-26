from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from  model import Base , Peso
from datetime import datetime
from typing import Union

class Boi(Base):
    __tablename__ = 'boi'
 
    brinco = Column("brinco", Integer, primary_key=True)
    raca =  Column(String(140))
    comentario = Column(String(140))
    data_aquisicao = Column(DateTime, default=datetime.now())
    # Definição do relacionamento entre o Bois e o peso.
    pesos = relationship("Peso")

    def __init__(self, brinco:Integer, raca:String, comentario:String, data_aquisicao:Union[DateTime, None] = None):
        """
        Cadastra um boi

        Arguments:
            Brinco: Numero do Brinco do Boi 
            Raça: Raça do Boi.
            Data_Aquisição: Data da aquisição do Boi 
        """
        self.brinco = brinco
        self.raca = raca
        self.comentario = comentario
        
        # se não for informada, será o data exata da inserção no banco
        if data_aquisicao:
            self.data_aquisicao = data_aquisicao

    def adiciona_peso(self, peso:Peso):
        """ Adiciona uma nova pesagem para o Boi
        """
        self.pesos.append(peso)