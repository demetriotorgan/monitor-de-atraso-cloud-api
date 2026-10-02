from pydantic import BaseModel,Field
from datetime import datetime


class AtrasoCreate(BaseModel):
    aluno_id: int
    motivo: str = Field(min_length=1)

class AtrasoResponse(BaseModel):
    id: int
    aluno_id:int
    data_hora:datetime
    motivo:str
    status_notificacao: str

class AtrasoUpdate(BaseModel):
    aluno_id: int | None = None
    motivo: str | None = Field(default=None, min_length=1)
    
class TesteWhatsapp(BaseModel):
    number: str = Field(min_length=1)
    text: str = Field(min_length=1)
    
class AlunoCreate(BaseModel):
 nome: str = Field(min_length=1)
 serie: str = Field(min_length=1)
 responsavel: str = Field(min_length=1)
 telefone_responsavel: str = Field(min_length=1) 

class AlunoResponse(BaseModel):
    id:int
    nome:str
    serie:str
    responsavel:str
    telefone_responsavel:str

class AlunoUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1)
    serie: str | None = Field(default=None, min_length=1)
    responsavel: str | None = Field(default=None, min_length=1)
    telefone_responsavel: str | None = Field(default=None, min_length=1)