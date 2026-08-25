from .models import CartEvent, Decision, Outcome

MAX_COUPON_PCT = 10
MIN_COUPON_CART = 1200
MAX_IDLE_FOR_COUPON = 240


def score_intent(e: CartEvent) -> float:
    score = 0.30 * e.product_affinity
    score += 0.25 * min(e.prior_orders / 5, 1)
    score += 0.20 * max(0, 1 - e.minutes_idle / 360)
    score += 0.15 * (1 - min(e.payment_failures_30d / 3, 1))
    score += 0.10 * (1 - e.inventory_risk)
    return max(0.0, min(1.0, score))


def decide(e: CartEvent) -> Decision:
    intent = score_intent(e)
    if e.inventory_risk >= 0.90:
        return Decision(cart_id=e.cart_id, action='human_review', reason='High inventory uncertainty; automation gated.', expected_uplift=0.0, bounded=True, approval_required=True, confidence=0.98)
    if e.payment_failures_30d >= 3:
        return Decision(cart_id=e.cart_id, action='human_review', reason='Repeated payment failures; avoid automated monetary incentives.', expected_uplift=0.0, bounded=True, approval_required=True, confidence=0.95)
    if e.minutes_idle < 15:
        return Decision(cart_id=e.cart_id, action='recommend_product', reason='Active session with sufficient affinity; prioritize non-monetary cross-sell.', expected_uplift=0.03 + 0.05 * e.product_affinity, bounded=True, approval_required=False, confidence=round(intent, 3))
    if e.minutes_idle < 90:
        return Decision(cart_id=e.cart_id, action='send_reminder', reason='Cart shows medium abandonment risk; reminder is the least intrusive action.', expected_uplift=0.05 + 0.07 * intent, bounded=True, approval_required=False, confidence=round(intent, 3))
    if e.cart_value >= MIN_COUPON_CART and e.discount_sensitivity >= 0.6 and e.minutes_idle <= MAX_IDLE_FOR_COUPON:
        return Decision(cart_id=e.cart_id, action='offer_coupon', reason=f'High-value cart with discount sensitivity; coupon capped at {MAX_COUPON_PCT}% by policy.', expected_uplift=0.10 + 0.10 * intent, bounded=True, approval_required=True, confidence=round(intent, 3))
    if e.minutes_idle >= 240:
        return Decision(cart_id=e.cart_id, action='none', reason='Stopping rule reached: stale cart; no further automated contact.', expected_uplift=0.0, bounded=True, approval_required=False, confidence=round(1-intent, 3))
    return Decision(cart_id=e.cart_id, action='send_reminder', reason='Default bounded recovery step.', expected_uplift=0.04 + 0.05 * intent, bounded=True, approval_required=False, confidence=round(intent, 3))


def simulate_outcome(e: CartEvent, d: Decision) -> Outcome:
    base = 0.08 + 0.35 * score_intent(e)
    threshold = min(0.92, base + d.expected_uplift)
    pseudo = ((sum(map(ord, e.cart_id)) * 37 + e.minutes_idle * 11 + e.prior_orders * 17) % 1000) / 1000
    converted = pseudo < threshold and d.action not in {'none', 'human_review'}
    return Outcome(cart_id=e.cart_id, converted=converted, recovered_revenue=round(e.cart_value if converted else 0.0, 2), action=d.action)
