from pydantic import BaseModel
from typing import Optional

class ImageFrame(BaseModel):
    id: int
    depth: float
    image_base64: Optional[str] = None