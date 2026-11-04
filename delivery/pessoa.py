from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from delivery.pedido import Pedido


class Pessoa(ABC):

    def __init__(self, nome: str, cpf: str, telefone: str):
        if not nome or not nome.strip():
            raise ValueError("Nome não pode ser vazio.")
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF deve ter 11 números.")
        if not telefone or not telefone.isdigit():
            raise ValueError("Telefone deve ter só números.")
        self._nome = nome.strip()
        self._cpf = cpf
        self._telefone = telefone

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def telefone(self) -> str:
        return self._telefone

    @abstractmethod
    def apresentar(self) -> str:
        pass

    def __str__(self) -> str:
        return self.apresentar()


class Cliente(Pessoa):

    def __init__(self, nome: str, cpf: str, telefone: str, endereco: str, distancia_km: float):
        super().__init__(nome, cpf, telefone)
        if not endereco or not endereco.strip():
            raise ValueError("Endereço não pode ser vazio.")
        if distancia_km < 0:
            raise ValueError("Distância não pode ser negativa.")
        self._endereco = endereco.strip()
        self._distancia_km = distancia_km
        self._pedidos: list[Pedido] = []

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def distancia_km(self) -> float:
        return self._distancia_km

    @property
    def pedidos(self) -> list[Pedido]:
        return list(self._pedidos)

    def adicionar_pedido(self, pedido: Pedido) -> None:
        if pedido not in self._pedidos:
            self._pedidos.append(pedido)

    def apresentar(self) -> str:
        return f"Cliente {self.nome} - {self.endereco} ({self.distancia_km} km)"


class Entregador(Pessoa):

    def __init__(self, nome: str, cpf: str, telefone: str, veiculo: str):
        super().__init__(nome, cpf, telefone)
        if not veiculo or not veiculo.strip():
            raise ValueError("Informe o veículo.")
        self._veiculo = veiculo.strip()
        self._disponivel = True

    @property
    def veiculo(self) -> str:
        return self._veiculo

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    def ocupar(self) -> None:
        if not self._disponivel:
            raise ValueError("Entregador já está ocupado.")
        self._disponivel = False

    def liberar(self) -> None:
        self._disponivel = True

    def apresentar(self) -> str:
        situacao = "disponível" if self._disponivel else "em entrega"
        return f"Entregador {self.nome} ({self.veiculo}) - {situacao}"
