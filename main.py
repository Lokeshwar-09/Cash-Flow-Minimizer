# main.py
import matplotlib.pyplot as plt
import networkx as nx
from greedy_algorithm import greedy_minimize
from graph_flow_algorithm import graph_flow_minimize

def draw_debts(transactions, title):
    if not transactions:
        print(f"[{title}] No transactions")
        return

    G = nx.DiGraph()
    for a, b, amt in transactions:
        G.add_edge(a, b, weight=amt)

    pos = nx.spring_layout(G, seed=42)  # fixed seed for nicer layout
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=2200, font_size=10, font_weight='bold',
            arrows=True, arrowstyle='->', arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    plt.title(title)
    plt.axis('off')
    plt.show()


# ────────────────────── MAIN PROGRAM ──────────────────────

print("=== Cash Flow Minimization Project ===")
print("Enter transactions one by one")
print("Format : payer payee amount")
print("Examples:")
print("  Alice Bob 1200")
print("  Bob Charlie 500")
print("When finished type: done\n")

transactions = []

while True:
    line = input("→ ").strip()
    if line.lower() in ['done', 'd', 'exit', 'q']:
        break

    parts = line.split()
    if len(parts) != 3:
        print("Invalid format → use: Name1 Name2 123")
        continue

    payer, payee, amt_str = parts
    try:
        amount = int(amt_str)
        if amount <= 0:
            print("Amount must be positive")
            continue
        transactions.append((payer, payee, amount))
    except ValueError:
        print("Amount must be a number")
        continue

if not transactions:
    print("\nNo transactions entered. Goodbye.")
else:
    print("\n" + "="*50)
    print("INPUT TRANSACTIONS")
    print("="*50)
    for a, b, amt in transactions:
        print(f"{a:10} owes {b:10} ₹{amt:>6}")

    # Greedy
    greedy_result = greedy_minimize(transactions)
    print("\n" + "="*50)
    print("GREEDY ALGORITHM RESULT")
    print("="*50)
    if not greedy_result:
        print("No payments needed (already balanced)")
    else:
        for a, b, amt in greedy_result:
            print(f"{a:10} → {b:10} : ₹{amt:>6}")
    print(f"→ Reduced to {len(greedy_result)} transactions")

    # Graph Flow
    flow_result = graph_flow_minimize(transactions)
    print("\n" + "="*50)
    print("GRAPH FLOW ALGORITHM RESULT")
    print("="*50)
    if isinstance(flow_result, tuple) and len(flow_result) == 2:  # error case
        print(flow_result[1])
    elif not flow_result:
        print("Result will be displayed in the other window")
    else:
        for a, b, amt in flow_result:
            print(f"{a:10} → {b:10} : ₹{amt:>6}")
        print(f"→ Reduced to {len(flow_result)} transactions")

    # Visualizations
    print("\nShowing graphs... (close each window to continue)")
    draw_debts(transactions, "Original Debts")
    draw_debts(greedy_result, "After Greedy Minimization")
    draw_debts(flow_result, "After Graph Flow Minimization")

print("\nThank you for using the Cash Flow Minimizer!")