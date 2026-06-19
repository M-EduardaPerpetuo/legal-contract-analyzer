from pydantic import BaseModel, Field
from typing import List

class AnaliseContratual(BaseModel):
    resumo_executivo: str = Field(
        description="Resumo claro e objetivo do propósito do contrato."
    )
    nivel_de_risco: int = Field(
        description="Score de 1 (Risco Baixo) a 5 (Risco Crítico)."
    )
    clausulas_criticas: List[str] = Field(
        description="Lista de cláusulas que representam risco legal, financeiro ou ambiguidade."
    )
    partes_envolvidas: List[str] = Field(
        description="Nomes das empresas envolvidas no acordo."
    )
    parecer_sugerido: str = Field(
        description="Sugestão consultiva da IA sobre a aprovação ou revisão."
    )