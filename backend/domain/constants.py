class OrderStatus:
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    PROCESSING = "processing"
    PARTIALLY_DISPATCHED = "partially_dispatched"  # future-ready, accepted by DB constraint
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REJECTED = "rejected"  # explicit rejection state, accepted by DB constraint


class BatchStatus:
    # Lifecycle: PENDING (consolidated) → DISPATCHED (confirmed and shipped) | CANCELLED
    PENDING = "pending"
    DISPATCHED = "dispatched"
    CANCELLED = "cancelled"
