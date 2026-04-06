from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CsvUpload(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    products_created: int
    products_updated: int

    model_config = ConfigDict(from_attributes=True)
