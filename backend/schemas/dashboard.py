from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .building import Building
from .product import Product
from .order import OrderDetail
from .dispatch import DispatchBatchDetail, DispatchBatchSummary, PurchaseSummary


class SubmissionDeadlineAlert(BaseModel):
    deadline_at: datetime
    note: Optional[str] = None
    state: str
    pending_orders_count: int


class AdminDashboard(BaseModel):
    buildings: List[Building]
    pedidos_activos: int
    pedidos_en_transito: int
    historial_pedidos: List[OrderDetail]
    pedidos_despachados: List[OrderDetail]
    submission_deadline: Optional[SubmissionDeadlineAlert] = None


class CostoPorEdificio(BaseModel):
    building_name: str
    gasto_total: float


class PedidosPorEdificio(BaseModel):
    building_name: str
    total_pedidos: int


class ManagerDashboard(BaseModel):
    pedidos_submitted: int
    total_edificios_activos: int
    costo_despachado_mes: float
    total_productos: int
    lotes_pendientes: List[DispatchBatchDetail]
    alertas_stock: List[Product]
    compras_recientes: List[PurchaseSummary]
    pedidos_por_edificio: List[PedidosPorEdificio]
    chart_edificios_labels: List[str]
    chart_edificios_data: List[int]
    chart_productos_labels: List[str]
    chart_productos_data: List[int]
    submission_deadline: Optional[SubmissionDeadlineAlert] = None


class SuperadminDashboard(BaseModel):
    total_pedidos_pendientes: int
    total_edificios_activos: int
    costo_despachado_mes: float
    total_productos: int
    alertas_stock: List[Product]
    costos_por_edificio: List[CostoPorEdificio]
    pedidos_por_edificio: List[PedidosPorEdificio]
    chart_edificios_labels: List[str]
    chart_edificios_data: List[int]
    chart_productos_labels: List[str]
    chart_productos_data: List[int]
    lotes_recientes: List[DispatchBatchSummary]
