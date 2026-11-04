from __future__ import annotations

from abc import ABC, abstractmethod


class Produto(ABC):

    def __init__(self, nome: str, preco: float):
        if not nome or not nome.strip():
            raise ValueError("Nome do produto não pode ser vazio.")
        if preco <= 0:
            raise ValueError("Preço deve ser maior que zero.")
        self._nome = nome.strip()
        self._preco = preco
        self._codigo: int | None = None
        self._disponivel = True

    @property
    def codigo(self) -> int | None:
        return self._codigo

    def definir_codigo(self, codigo: int) -> None:
        if self._codigo is not None:
            raise ValueError("Produto já tem código.")
        self._codigo = codigo

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Preço deve ser maior que zero.")
        self._preco = valor

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    def marcar_indisponivel(self) -> None:
        self._disponivel = False

    def marcar_disponivel(self) -> None:
        self._disponivel = True

    @abstractmethod
    def categoria(self) -> str: ...

    @abstractmethod
    def detalhe(self) -> str: ...

    @abstractmethod
    def taxa_embalagem(self) -> float: ...

    def preco_final(self) -> float:
        return round(self._preco + self.taxa_embalagem(), 2)

    def __str__(self) -> str:
        situacao = "" if self._disponivel else " (indisponível)"
        return (f"[{self.codigo}] {self.categoria()} {self.nome} - {self.detalhe()} - "
                f"R$ {self.preco_final():.2f}{situacao}")


class Prato(Produto):
    def __init__(self, nome: str, preco: float, serve_pessoas: int = 1):
        super().__init__(nome, preco)
        if serve_pessoas < 1:
            raise ValueError("O prato deve servir pelo menos 1 pessoa.")
        self.serve_pessoas = serve_pessoas

    def categoria(self) -> str:
        return "Prato"

    def detalhe(self) -> str:
        return f"serve {self.serve_pessoas} pessoa(s)"

    def taxa_embalagem(self) -> float:
        return 2.0


class Bebida(Produto):
    def __init__(self, nome: str, preco: float, volume_ml: int):
        super().__init__(nome, preco)
        if volume_ml <= 0:
            raise ValueError("Volume deve ser maior que zero.")
        self.volume_ml = volume_ml

    def categoria(self) -> str:
        return "Bebida"

    def detalhe(self) -> str:
        return f"{self.volume_ml} ml"

    def taxa_embalagem(self) -> float:
        return 0.5


class Sobremesa(Produto):
    def __init__(self, nome: str, preco: float, gelada: bool = False):
        super().__init__(nome, preco)
        self.gelada = gelada

    def categoria(self) -> str:
        return "Sobremesa"

    def detalhe(self) -> str:
        return "gelada" if self.gelada else "temperatura ambiente"

    def taxa_embalagem(self) -> float:
        return 2.5 if self.gelada else 1.0  
