with open('sales.txt', mode='r', encoding='utf-8') as f:
    lines = f.readlines()
    print('날짜      이름    상품명   갯수    판매금액')

    employee_totals = {}
    total_sales = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        date, name, product, qty, price = line.split(",")
        qty = int(qty)
        price = int(price)
        amount = qty * price

        print(f'{date} {name} {product} {qty}개 {amount}원')
        employee_totals[name] = employee_totals.get(name, 0) + amount

        total_sales += amount

        top_employee = max(employee_totals, key=employee_totals.get)
        top_amount = employee_totals[top_employee]

print(f"\n전체 판매 금액 : {total_sales:,}원")
print(f"판매왕 : {top_employee}")

with open("sales_report.txt", "w", encoding="utf-8") as f:
    f.write("직원별 판매 실적\n\n")
    for name, amount in employee_totals.items():
        f.write(f"{name}: {amount:,}원\n")
    f.write(f"\n전체 판매 금액: {total_sales:,}원\n")
    f.write(f"판매왕: {top_employee} ({top_amount:,}원)\n")
