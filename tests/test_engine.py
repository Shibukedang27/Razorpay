from app.models import CartEvent
from app.engine import decide, score_intent

def ev(**kw):
    d=dict(cart_id='C1',customer_id='U1',cart_value=2000,minutes_idle=30,prior_orders=2,discount_sensitivity=.7,product_affinity=.8,payment_failures_30d=0,inventory_risk=.1); d.update(kw); return CartEvent(**d)

def test_score_bounded():
    assert 0 <= score_intent(ev()) <= 1

def test_high_inventory_gated():
    d=decide(ev(inventory_risk=.95)); assert d.action=='human_review' and d.approval_required

def test_repeated_payment_failure_gated():
    d=decide(ev(payment_failures_30d=3)); assert d.action=='human_review'

def test_coupon_requires_approval():
    d=decide(ev(minutes_idle=120,cart_value=3000,discount_sensitivity=.9)); assert d.action=='offer_coupon' and d.approval_required and d.bounded

def test_stale_cart_stops():
    d=decide(ev(minutes_idle=300,cart_value=500,discount_sensitivity=.1)); assert d.action=='none'
