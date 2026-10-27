from typing import Literal
from pydantic import BaseModel, Field

class CasoNuevo(BaseModel):
    radicado: str = Field(min_length=3, max_length=80)
    escenario: Literal["ASIS", "TOBE"] = "TOBE"
    area_terreno_m2: float = Field(gt=0, le=1_000_000)
    area_construida_m2: float = Field(ge=0, le=1_000_000)
    uso: Literal["residencial", "comercial", "mixto"] = "residencial"
    chip: str | None = Field(default=None, max_length=50)

class CompletarTarea(BaseModel):
    actor: str = Field(default="estudiante", min_length=2, max_length=80)
    aprobado: bool = True
    observacion: str = Field(default="", max_length=500)
