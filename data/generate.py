import csv, random
random.seed(42)
rows=[]
for i in range(250):
    rows.append({
        'cart_id':f'CART-{i:04d}','customer_id':f'CUST-{random.randint(1,120):04d}',
        'cart_value':round(random.uniform(300,8000),2),'minutes_idle':random.randint(0,360),
        'prior_orders':random.randint(0,8),'discount_sensitivity':round(random.random(),3),
        'product_affinity':round(random.random(),3),'payment_failures_30d':random.choice([0,0,0,0,1,1,2,3]),
        'inventory_risk':round(random.random(),3)})
with open('data/synthetic_carts.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(len(rows))
