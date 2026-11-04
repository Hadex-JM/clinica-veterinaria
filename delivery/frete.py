from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from delivery.pedido import Pedido


class CalculadoraFrete:

    def __init__(self, taxa_fixa: float = 5.0, valor_por_km: float = 1.5,
                 gratis_acima_de: float = 100.0):
        self.taxa_fixa = taxa_fixa
        self.valor_por_km = valor_por_km
        self.gratis_acima_de = gratis_acima_de

    def calcular(self, pedido: Pedido) -> float:
        if pedido.subtotal() >= self.gratis_acima_de:
            return 0.0
        return round(self.taxa_fixa + pedido.cliente.distancia_km * self.valor_por_km, 2)