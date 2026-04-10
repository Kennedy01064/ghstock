from pydantic import BaseModel, Field

class StockTransferCreate(BaseModel):
    from_building_id: int = Field(..., description="Source building ID")
    to_building_id: int = Field(..., description="Target building ID")
    product_id: int = Field(..., description="ID of the product to transfer")
    quantity: int = Field(..., gt=0, description="Positive quantity to move")
