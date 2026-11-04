
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from delivery.frete import CalculadoraFrete
    from delivery.pessoa import Cliente, Entregador
    from delivery.produto import Produto


class StatusPedido(Enum):
    ABERTO = "Aberto"                   
    AGUARDANDO = "Aguardando restaurante"
    EM_PREPARO = "Em preparo"
    A_CAMINHO = "A caminho"
    ENTREGUE = "Entregue"
    CANCELADO = "Cancelado"


class ItemPedido:


    def __init__(self, produto: Produto, quantidade: int):
        self._produto = produto
        self._quantidade = quantidade
        self._preco_unitario = produto.preco_final()

    @property
    def produto(self) -> Produto:
        return self._produto

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @property
    def preco_unitario(self) -> float:
        return self._preco_unitario

    def aumentar(self, quantidade: int) -> None:
        self._quantidade += quantidade

    def subtotal(self) -> float:
        return round(self._preco_unitario * self._quantidade, 2)

    def __str__(self) -> str:
        return (f"{self.quantidade}x {self.produto.nome} "
                f"(R$ {self.preco_unitario:.2f}) = R$ {self.subtotal():.2f}")


class Pedido:


    PODE_CANCELAR = (StatusPedido.ABERTO, StatusPedido.AGUARDANDO, StatusPedido.EM_PREPARO)

    def __init__(self, numero: int, cliente: Cliente):
        self._numero = numero
        self._cliente = cliente
        self._itens: list[ItemPedido] = []
        self._status = StatusPedido.ABERTO
        self._entregador: Entregador | None = None
        self._frete = 0.0
        cliente.adicionar_pedido(self)

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def itens(self) -> list[ItemPedido]:
        return list(self._itens)

    @property
    def status(self) -> StatusPedido:
        return self._status

    @property
    def entregador(self) -> Entregador | None:
        return self._entregador

    @property
    def frete(self) -> float:
        return self._frete

    # ----- montar o pedido -----
    def adicionar_item(self, produto: Produto, quantidade: int = 1) -> ItemPedido:
        self._exigir(StatusPedido.ABERTO, "Só dá para mudar itens de um pedido aberto.")
        if quantidade < 1:
            raise ValueError("Quantidade deve ser pelo menos 1.")
        if not produto.disponivel:
            raise ValueError(f"{produto.nome} está indisponível.")
        for item in self._itens:
            if item.produto is produto:      
                item.aumentar(quantidade)
                return item
        item = ItemPedido(produto, quantidade)
        self._itens.append(item)
        return item

    def remover_item(self, produto: Produto) -> None:
        self._exigir(StatusPedido.ABERTO, "Só dá para mudar itens de um pedido aberto.")
        for item in self._itens:
            if item.produto is produto:
                self._itens.remove(item)
                return
        raise ValueError(f"{produto.nome} não está no pedido.")

    def subtotal(self) -> float:
        return round(sum(i.subtotal() for i in self._itens), 2)

    def total(self) -> float:
        return round(self.subtotal() + self._frete, 2)

    def finalizar(self, calculadora: CalculadoraFrete) -> None:
        """Fecha o pedido. Usa a calculadora só aqui dentro (DEPENDÊNCIA)."""
        self._exigir(StatusPedido.ABERTO, "Esse pedido já foi finalizado.")
        if not self._itens:
            raise ValueError("Pedido sem itens.")
        self._frete = calculadora.calcular(self)
        self._status = StatusPedido.AGUARDANDO

    def iniciar_preparo(self) -> None:
        self._exigir(StatusPedido.AGUARDANDO, "Só dá para preparar um pedido aguardando.")
        self._status = StatusPedido.EM_PREPARO

    def enviar(self, entregador: Entregador) -> None:
        self._exigir(StatusPedido.EM_PREPARO, "Só dá para enviar um pedido em preparo.")
        entregador.ocupar()
        self._entregador = entregador
        self._status = StatusPedido.A_CAMINHO

    def confirmar_entrega(self) -> None:
        self._exigir(StatusPedido.A_CAMINHO, "Só dá para entregar um pedido a caminho.")
        self._entregador.liberar()
        self._status = StatusPedido.ENTREGUE

    def cancelar(self) -> None:
        if self._status not in self.PODE_CANCELAR:
            raise ValueError(f"Pedido {self._status.value.lower()} não pode ser cancelado.")
        self._status = StatusPedido.CANCELADO

    def resumo(self) -> str:
        linhas = [f"Pedido #{self.numero} - {self.cliente.nome} - {self.status.value}"]
        linhas += [f"  {item}" for item in self._itens]
        linhas.append(f"  Subtotal: R$ {self.subtotal():.2f}")
        linhas.append(f"  Frete:    R$ {self.frete:.2f}")
        linhas.append(f"  Total:    R$ {self.total():.2f}")
        if self._entregador:
            linhas.append(f"  Entregador: {self._entregador.nome} ({self._entregador.veiculo})")
        return "\n".join(linhas)

    def _exigir(self, status: StatusPedido, mensagem: str) -> None:
        if self._status != status:
            raise ValueError(mensagem)

    def __str__(self) -> str:
        return f"Pedido #{self.numero} - {self.cliente.nome} - {self.status.value} - R$ {self.total():.2f}"
