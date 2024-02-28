from pydantic import BaseModel, Field
from typing import Optional


class UsuarioSchema(BaseModel):

    id: Optional[int] = None
    nombre: str = Field(min_length=3, max_length=40)
    apellidos: str = Field(min_length=3, max_length=40)
    edad: int = Field(ge=18, le=99)
    email: str
    telefono: str = Field(min_length=9, max_length=20)
    dni: str = Field(min_length=8, max_length=20)
    direccion: str = Field(min_length=10)
    ciudad: str = Field(min_length=3, max_length=30)
    provincia: str = Field(min_length=3, max_length=30)
