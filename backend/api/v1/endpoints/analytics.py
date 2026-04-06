import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Any

from backend import models, schemas
from backend.api import deps
from backend.core.config import settings

router = APIRouter()


DASHBOARD_CACHE_TTL_SECONDS = 15 * 60
_redis_client: Redis | None = None
_redis_disabled = False


def _get_redis_client() -> Redis | None:
    global _redis_client, _redis_disabled
    if _redis_disabled:
        return None
    if _redis_client is None:
        try:
            client = Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=0.2,
                socket_timeout=0.2,
                retry_on_timeout=False,
            )
            client.ping()
            _redis_client = client
        except RedisError:
            _redis_disabled = True
            return None
    return _redis_client


def _get_cached_dashboard(cache_key: str) -> Any | None:
    client = _get_redis_client()
    if client is None:
        return None
    try:
        cached_value = client.get(cache_key)
        return json.loads(cached_value) if cached_value else None
    except RedisError:
        return None


def _cache_dashboard(cache_key: str, schema: type[BaseModel], payload: Any) -> Any:
    serialized_payload = schema.model_validate(payload).model_dump(mode="json")
    client = _get_redis_client()
    if client is None:
        return serialized_payload
    try:
        client.setex(
            cache_key,
            DASHBOARD_CACHE_TTL_SECONDS,
            json.dumps(serialized_payload),
        )
    except RedisError:
        pass
    return serialized_payload


@router.get("/admin", response_model=schemas.dashboard.AdminDashboard)
def get_admin_dashboard(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Operations dashboard for Building Admins."""
    cache_key = f"analytics:admin:{current_user.role}:{current_user.id}"
    cached_payload = _get_cached_dashboard(cache_key)
    if cached_payload is not None:
        return cached_payload

    active_statuses = ["submitted", "processing", "dispatched"]

    if current_user.role == "superadmin":
        base_buildings = db.query(models.Building).all()
        building_ids = [b.id for b in base_buildings]
        pedidos_activos = db.query(models.Order).filter(
            models.Order.status.in_(["draft", "submitted", "processing"])
        ).count()
        pedidos_en_transito = db.query(models.Order).filter(
            models.Order.status.in_(["submitted", "processing"])
        ).count()
        historial_pedidos = db.query(models.Order).order_by(models.Order.created_at.desc()).limit(10).all()
        pedidos_despachados = db.query(models.Order).filter_by(status="dispatched").order_by(models.Order.created_at.desc()).all()
    else:
        base_buildings = db.query(models.Building).filter(models.Building.admin_id == current_user.id).all()
        building_ids = [b.id for b in base_buildings]
        pedidos_activos = db.query(models.Order).filter(
            models.Order.building_id.in_(building_ids),
            models.Order.status.in_(["draft", "submitted", "processing"])
        ).count()
        pedidos_en_transito = db.query(models.Order).filter(
            models.Order.building_id.in_(building_ids),
            models.Order.status.in_(["submitted", "processing"])
        ).count()
        historial_pedidos = db.query(models.Order).filter(
            models.Order.building_id.in_(building_ids)
        ).order_by(models.Order.created_at.desc()).limit(10).all()
        pedidos_despachados = db.query(models.Order).filter(
            models.Order.building_id.in_(building_ids),
            models.Order.status == "dispatched"
        ).order_by(models.Order.created_at.desc()).all()

    # Fix N+1: Use a single aggregated query for counts
    active_counts = db.query(
        models.Order.building_id,
        func.count(models.Order.id).label("count")
    ).filter(
        models.Order.status.in_(active_statuses)
    ).group_by(models.Order.building_id).all()
    active_counts_dict = {r.building_id: r.count for r in active_counts}

    buildings = []
    for building in base_buildings:
        buildings.append({
            "id": building.id,
            "name": building.name,
            "address": building.address,
            "departments_count": building.departments_count,
            "imagen_frontis": building.imagen_frontis,
            "admin_id": building.admin_id,
            "admin": building.admin,
            "active_orders_count": active_counts_dict.get(building.id, 0),
        })

    payload = {
        "buildings": buildings,
        "pedidos_activos": pedidos_activos,
        "pedidos_en_transito": pedidos_en_transito,
        "historial_pedidos": historial_pedidos,
        "pedidos_despachados": pedidos_despachados,
    }
    return _cache_dashboard(cache_key, schemas.dashboard.AdminDashboard, payload)


@router.get("/manager", response_model=schemas.dashboard.ManagerDashboard)
def get_manager_dashboard(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Warehouse operations dashboard."""
    cache_key = "analytics:manager"
    cached_payload = _get_cached_dashboard(cache_key)
    if cached_payload is not None:
        return cached_payload

    pedidos_submitted = db.query(models.Order).filter_by(status="submitted").count()
    lotes_pendientes = db.query(models.DispatchBatch).filter_by(status="pending").all()
    alertas_stock = db.query(models.Product).filter(
        models.Product.stock_actual <= models.Product.stock_minimo,
        models.Product.is_active == True
    ).order_by(models.Product.stock_actual.asc()).limit(8).all()
    
    compras_recientes = db.query(models.Purchase).order_by(models.Purchase.purchase_date.desc()).limit(5).all()

    payload = {
        "pedidos_submitted": pedidos_submitted,
        "lotes_pendientes": lotes_pendientes,
        "alertas_stock": alertas_stock,
        "compras_recientes": compras_recientes,
    }
    return _cache_dashboard(cache_key, schemas.dashboard.ManagerDashboard, payload)


@router.get("/superadmin", response_model=schemas.dashboard.SuperadminDashboard)
def get_superadmin_dashboard(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Full analytics dashboard for Superadmins."""
    if current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Not enough privileges")

    cache_key = "analytics:superadmin"
    cached_payload = _get_cached_dashboard(cache_key)
    if cached_payload is not None:
        return cached_payload

    total_pedidos_pendientes = db.query(models.Order).filter(
        models.Order.status.in_(["draft", "submitted"])
    ).count()

    total_edificios_activos = db.query(func.count(func.distinct(models.Order.building_id))).scalar() or 0

    now = datetime.now(timezone.utc)
    first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    costo_despachado_mes = db.query(
        func.coalesce(func.sum(models.DispatchBatchItem.total_quantity * models.Product.precio), 0)
    ).join(
        models.Product, models.DispatchBatchItem.product_id == models.Product.id
    ).join(
        models.DispatchBatch, models.DispatchBatchItem.batch_id == models.DispatchBatch.id
    ).filter(
        models.DispatchBatch.status == "dispatched",
        models.DispatchBatch.created_at >= first_of_month
    ).scalar() or 0

    total_productos = db.query(models.Product).filter_by(is_active=True).count()

    alertas_stock = db.query(models.Product).filter(
        models.Product.stock_actual <= models.Product.stock_minimo,
        models.Product.is_active == True
    ).order_by(models.Product.stock_actual.asc()).all()

    costos_por_edificio_raw = db.query(
        models.Building.name.label("building_name"),
        func.coalesce(func.sum(models.OrderItem.quantity * models.OrderItem.precio_unitario), 0).label("gasto_total")
    ).join(
        models.Order, models.Building.id == models.Order.building_id
    ).join(
        models.OrderItem, models.Order.id == models.OrderItem.order_id
    ).filter(
        models.Order.status.in_(["dispatched", "delivered"])
    ).group_by(models.Building.name).order_by(func.sum(models.OrderItem.quantity * models.OrderItem.precio_unitario).desc()).all()

    pedidos_por_edificio_raw = db.query(
        models.Building.name.label("building_name"),
        func.count(models.Order.id).label("total_pedidos")
    ).join(
        models.Order, models.Building.id == models.Order.building_id
    ).group_by(models.Building.name).order_by(func.count(models.Order.id).desc()).all()

    chart_edificios_labels = [r.building_name for r in pedidos_por_edificio_raw]
    chart_edificios_data = [r.total_pedidos for r in pedidos_por_edificio_raw]

    top_productos = db.query(
        models.Product.name.label("product_name"),
        func.sum(models.OrderItem.quantity).label("total_solicitado")
    ).join(
        models.OrderItem, models.Product.id == models.OrderItem.product_id
    ).group_by(models.Product.name).order_by(func.sum(models.OrderItem.quantity).desc()).limit(5).all()

    chart_productos_labels = [r.product_name for r in top_productos]
    chart_productos_data = [int(r.total_solicitado) for r in top_productos]

    lotes_recientes = db.query(models.DispatchBatch).order_by(
        models.DispatchBatch.created_at.desc()
    ).limit(5).all()

    payload = {
        "total_pedidos_pendientes": total_pedidos_pendientes,
        "total_edificios_activos": total_edificios_activos,
        "costo_despachado_mes": costo_despachado_mes,
        "total_productos": total_productos,
        "alertas_stock": alertas_stock,
        "costos_por_edificio": [{"building_name": r.building_name, "gasto_total": r.gasto_total} for r in costos_por_edificio_raw],
        "pedidos_por_edificio": [{"building_name": r.building_name, "total_pedidos": r.total_pedidos} for r in pedidos_por_edificio_raw],
        "chart_edificios_labels": chart_edificios_labels,
        "chart_edificios_data": chart_edificios_data,
        "chart_productos_labels": chart_productos_labels,
        "chart_productos_data": chart_productos_data,
        "lotes_recientes": lotes_recientes,
    }
    return _cache_dashboard(cache_key, schemas.dashboard.SuperadminDashboard, payload)
