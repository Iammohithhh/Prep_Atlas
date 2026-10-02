import csv
import os
from collections import Counter, defaultdict


def generate_files(input_file_name):
    total_qty = defaultdict(float)
    brand_orders = defaultdict(Counter)
    n = 0
    with open(input_file_name, newline='') as f:
        for row in csv.reader(f):
            if not row:
                continue
            _id, _area, product, qty, brand = row
            n += 1
            total_qty[product] += float(qty)
            brand_orders[product][brand] += 1        # popularity = number of orders, not quantity
    directory, base = os.path.split(input_file_name)
    with open(os.path.join(directory, '0_' + base), 'w', newline='') as f0, \
         open(os.path.join(directory, '1_' + base), 'w', newline='') as f1:
        w0, w1 = csv.writer(f0), csv.writer(f1)
        for product in total_qty:
            w0.writerow([product, total_qty[product] / n])   # average per order over ALL n orders
            w1.writerow([product, brand_orders[product].most_common(1)[0][0]])

# ---- tests
import tempfile
d = tempfile.mkdtemp()
p = os.path.join(d, 'input_example.csv')
open(p, 'w').write('ID1,Minneapolis,shoes,2,Air\nID2,Chicago,shoes,1,Air\nID3,Central Department Store,shoes,5,BonPied\nID4,Quail Hollow,forks,3,Pfitzcraft\n')
generate_files(p)
a = dict(l.strip().split(',') for l in open(os.path.join(d, '0_input_example.csv')))
b = dict(l.strip().split(',') for l in open(os.path.join(d, '1_input_example.csv')))
assert abs(float(a['shoes']) - 2) < 1e-3 and abs(float(a['forks']) - 0.75) < 1e-3
assert b == {'shoes': 'Air', 'forks': 'Pfitzcraft'}
print('ok')
