from pydantic import BaseModel, Field
from typing import Literal

class CartEvent(BaseModel):
    cart_id: str
    customer_id: str
    cart_value: float = Field(gt=0)
    minutes_idle: int = Field(ge=0)
    prior_orders: int = Field(ge=0)
    discount_sensitivity: float = Field(ge=0, le=1)
    product_affinity: float = Field(ge=0, le=1)
    payment_failures_30d: int = Field(ge=0)
    inventory_risk: float = Field(ge=0, le=1)

class Decision(BaseModel):
    cart_id: str
    action: Literal['none','recommend_product','send_reminder','offer_coupon','human_review']
    reason: str
    expected_uplift: float
    bounded: bool
    approval_required: bool
    confidence: float

class Outcome(BaseModel):
    cart_id: str
    converted: bool
    recovered_revenue: float
    action: str
