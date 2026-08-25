from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)

def test_health(): assert c.get('/health').json()['status']=='ok'
def test_decision():
    p={'cart_id':'C42','customer_id':'U1','cart_value':2500,'minutes_idle':120,'prior_orders':3,'discount_sensitivity':.9,'product_affinity':.8,'payment_failures_30d':0,'inventory_risk':.1}
    r=c.post('/api/decide',json=p); assert r.status_code==200; j=r.json(); assert j['decision']['bounded'] is True; assert 'reason' in j['decision']; assert 'outcome' in j
