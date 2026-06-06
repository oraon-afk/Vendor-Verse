import csv, json
from collections import defaultdict

with open(r'kaggle_data/supply_chain_data.csv') as f:
    r = csv.DictReader(f)
    rows = list(r)

# Show 2 sample rows
for row in rows[:2]:
    print(json.dumps(row, indent=2))
    print('---')

# Per-supplier aggregation
stats = defaultdict(lambda: {
    'count': 0, 'defect_rates': [], 'lead_times': [], 'shipping_times': [],
    'shipping_costs': [], 'mfg_costs': [], 'revenue': [], 'sold': [],
    'stock': [], 'prod_vol': [], 'locations': set(), 'products': set(),
    'prices': [], 'order_qty': [], 'inspect_pass': 0, 'inspect_total': 0
})

for row in rows:
    s = row['Supplier name']
    d = stats[s]
    d['count'] += 1
    d['defect_rates'].append(float(row['Defect rates']))
    d['lead_times'].append(float(row['Lead times']))
    d['shipping_times'].append(float(row['Shipping times']))
    d['shipping_costs'].append(float(row['Shipping costs']))
    d['mfg_costs'].append(float(row['Manufacturing costs']))
    d['revenue'].append(float(row['Revenue generated']))
    d['sold'].append(int(row['Number of products sold']))
    d['stock'].append(float(row['Stock levels']))
    d['prod_vol'].append(int(row['Production volumes']))
    d['prices'].append(float(row['Price']))
    d['order_qty'].append(int(row['Order quantities']))
    d['locations'].add(row['Location'])
    d['products'].add(row['Product type'])
    if row['Inspection results'] == 'Pass':
        d['inspect_pass'] += 1
    d['inspect_total'] += 1

print('\n=== SUPPLIER AGGREGATION ===')
for name in sorted(stats):
    d = stats[name]
    avg = lambda lst: sum(lst)/len(lst)
    print(f"\n{name}: {d['count']} products")
    print(f"  locations={d['locations']}, products={d['products']}")
    print(f"  avg_defect={avg(d['defect_rates']):.2f}%")
    print(f"  avg_lead_time={avg(d['lead_times']):.1f} days")
    print(f"  avg_ship_time={avg(d['shipping_times']):.1f} days")
    print(f"  avg_ship_cost=${avg(d['shipping_costs']):.2f}")
    print(f"  avg_mfg_cost=${avg(d['mfg_costs']):.2f}")
    print(f"  avg_price=${avg(d['prices']):.2f}")
    print(f"  total_revenue=${sum(d['revenue']):,.0f}")
    print(f"  total_sold={sum(d['sold'])}")
    print(f"  avg_stock={avg(d['stock']):.1f}")
    print(f"  total_prod_vol={sum(d['prod_vol'])}")
    print(f"  total_order_qty={sum(d['order_qty'])}")
    print(f"  inspect_pass_rate={d['inspect_pass']/d['inspect_total']*100:.1f}%")
