from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Atraso(Base):
    __tablename__='atrasos'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    
    message: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
    aluno: Mapped[str] = mapped_column(
        String,
        nullable=False  
    )
    
    motivo: Mapped[str] = mapped_column(
        String,
        nullable=False
    )