
from __future__ import annotations

from delivery.frete import CalculadoraFrete
from delivery.pedido import Pedido, StatusPedido
from delivery.pessoa import Cliente, Entregador
from delivery.produto import Produto


class Restaurante:

    def __init__(self, nome: str):
        self.nome = nome
        self._cardapio: list[Produto] = []
        self._clientes: list[Cliente] = []
        self._entregadores: list[Entregador] = []
        self._pedidos: list[Pedido] = []

    @property
    def clientes(self) -> list[Cliente]:
        return list(self._clientes)

    @property
    def entregadores(self) -> list[Entregador]:
        return list(self._entregadores)

    @property
    def pedidos(self) -> list[Pedido]:
        return list(self._pedidos)

    def cadastrar_cliente(self, cliente: Cliente) -> None:
        if self.buscar_cliente(cliente.cpf):
            raise ValueError("Já existe cliente com esse CPF.")
        self._clientes.append(cliente)

    def buscar_cliente(self, cpf: str) -> Cliente | None:
        return next((c for c in self._clientes if c.cpf == cpf), None)

    def cadastrar_entregador(self, entregador: Entregador) -> None:
        if any(e.cpf == entregador.cpf for e in self._entregadores):
            raise ValueError("Já existe entregador com esse CPF.")
        self._entregadores.append(entregador)

    def entregadores_disponiveis(self) -> list[Entregador]:
        return [e for e in self._entregadores if e.disponivel]

   
    def cadastrar_produto(self, produto: Produto) -> int:
        if produto in self._cardapio:
            raise ValueError("Produto já cadastrado.")
        produto.definir_codigo(len(self._cardapio) + 1)
        self._cardapio.append(produto)
        return produto.codigo

    def buscar_produto(self, codigo: int) -> Produto:
        produto = next((p for p in self._cardapio if p.codigo == codigo), None)
        if produto is None:
            raise ValueError(f"Produto {codigo} não existe.")
        return produto

    def alterar_preco(self, codigo: int, novo_preco: float) -> None:
        self.buscar_produto(codigo).preco = novo_preco

    def marcar_indisponivel(self, codigo: int) -> None:
        self.buscar_produto(codigo).marcar_indisponivel()

    def marcar_disponivel(self, codigo: int) -> None:
        self.buscar_produto(codigo).marcar_disponivel()

    # ----- caso de uso: ver cardápio -----
    def cardapio(self, so_disponiveis: bool = True) -> list[Produto]:
        return [p for p in self._cardapio if p.disponivel or not so_disponiveis]

    def listar_por_categoria(self, categoria: str) -> list[Produto]:
        return [p for p in self.cardapio() if p.categoria().lower() == categoria.lower()]

    def novo_pedido(self, cliente: Cliente) -> Pedido:
        if cliente not in self._clientes:
            raise ValueError("Cliente não cadastrado.")
        pedido = Pedido(len(self._pedidos) + 1, cliente)
        self._pedidos.append(pedido)
        return pedido

    def adicionar_ao_pedido(self, pedido: Pedido, codigo: int, quantidade: int = 1) -> None:
        self._conferir(pedido)
        pedido.adicionar_item(self.buscar_produto(codigo), quantidade)

    def remover_do_pedido(self, pedido: Pedido, codigo: int) -> None:
        self._conferir(pedido)
        pedido.remover_item(self.buscar_produto(codigo))

    def finalizar_pedido(self, pedido: Pedido) -> None:
        self._conferir(pedido)
        pedido.finalizar(CalculadoraFrete())  

    def iniciar_preparo(self, pedido: Pedido) -> None:
        self._conferir(pedido)
        pedido.iniciar_preparo()

    def enviar_pedido(self, pedido: Pedido, entregador: Entregador | None = None) -> Entregador:
        """Sem entregador escolhido, pega o primeiro disponível."""
        self._conferir(pedido)
        if entregador is None:
            livres = self.entregadores_disponiveis()
            if not livres:
                raise ValueError("Nenhum entregador disponível.")
            entregador = livres[0]
        elif entregador not in self._entregadores:
            raise ValueError("Entregador não cadastrado.")
        pedido.enviar(entregador)
        return entregador

    def confirmar_entrega(self, pedido: Pedido) -> None:
        self._conferir(pedido)
        pedido.confirmar_entrega()

    def cancelar_pedido(self, pedido: Pedido) -> None:
        self._conferir(pedido)
        pedido.cancelar()

    def buscar_pedido(self, numero: int) -> Pedido:
        pedido = next((p for p in self._pedidos if p.numero == numero), None)
        if pedido is None:
            raise ValueError(f"Pedido {numero} não existe.")
        return pedido

    def pedidos_por_status(self, status: StatusPedido) -> list[Pedido]:
        return [p for p in self._pedidos if p.status == status]

    def faturamento(self) -> float:
        return round(sum(p.total() for p in self.pedidos_por_status(StatusPedido.ENTREGUE)), 2)

    def _conferir(self, pedido: Pedido) -> None:
        if pedido not in self._pedidos:
            raise ValueError("Pedido não é deste restaurante.")
