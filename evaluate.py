import csv, json
from app.models import CartEvent
from app.engine import decide, score_intent

rows=[]
with open('data/synthetic_carts.csv') as f:
    for r in csv.DictReader(f):
        r['cart_value']=float(r['cart_value']); r['minutes_idle']=int(r['minutes_idle']); r['prior_orders']=int(r['prior_orders']); r['discount_sensitivity']=float(r['discount_sensitivity']); r['product_affinity']=float(r['product_affinity']); r['payment_failures_30d']=int(r['payment_failures_30d']); r['inventory_risk']=float(r['inventory_risk']); rows.append(CartEvent(**r))

def pseudo(e):
    return ((sum(map(ord,e.cart_id))*37+e.minutes_idle*11+e.prior_orders*17)%1000)/1000

def baseline_prob(e):
    freshness=max(0.05,1-e.minutes_idle/420)
    return min(.75,(.05+.32*score_intent(e))*freshness)

baseline_conv=agent_conv=0
baseline_rev=agent_rev=0.0
incremental_recovered=0.0
auto_eligible=0; action_wins=0; gated=0; coupons=0; stopped=0
for e in rows:
    d=decide(e); p0=baseline_prob(e); b=pseudo(e) < p0
    baseline_conv += int(b); baseline_rev += e.cart_value if b else 0
    if d.action in {'none','human_review'}:
        a=b
    else:
        auto_eligible += 1; p1=min(.95,p0+d.expected_uplift); a=pseudo(e) < p1
        action_wins += int(a and not b); incremental_recovered += e.cart_value if (a and not b) else 0
    agent_conv += int(a); agent_rev += e.cart_value if a else 0
    gated += int(d.approval_required); coupons += int(d.action=='offer_coupon'); stopped += int(d.action=='none')

res={'records':len(rows),'baseline_conversions':baseline_conv,'agent_policy_conversions':agent_conv,'conversion_uplift_pct':round((agent_conv-baseline_conv)/max(baseline_conv,1)*100,2),'baseline_revenue_inr':round(baseline_rev,2),'agent_policy_revenue_inr':round(agent_rev,2),'revenue_uplift_pct':round((agent_rev-baseline_rev)/max(baseline_rev,1)*100,2),'incremental_recovered_revenue_inr':round(incremental_recovered,2),'auto_eligible_records':auto_eligible,'incremental_conversion_wins':action_wins,'approval_gated_actions':gated,'coupon_actions':coupons,'stopping_rule_actions':stopped,'note':'Deterministic synthetic simulation for reproducible evaluation; not a production uplift claim.'}
print(json.dumps(res,indent=2))
with open('docs/evaluation.json','w') as f: json.dump(res,f,indent=2)
