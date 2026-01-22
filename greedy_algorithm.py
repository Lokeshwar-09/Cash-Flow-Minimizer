# greedy_algorithm.py
from collections import defaultdict

def greedy_minimize(transactions):
    """
    Greedy method: sort debtors and creditors → match largest possible amounts
    """
    net = defaultdict(int)
    for payer, payee, amt in transactions:
        net[payer] -= amt
        net[payee] += amt

    # debtors (owe money → negative), creditors (to receive → positive)
    debtors = [(p, b) for p, b in net.items() if b < 0]
    creditors = [(p, b) for p, b in net.items() if b > 0]

    # sort: most negative first, largest positive first
    debtors.sort(key=lambda x: x[1])
    creditors.sort(key=lambda x: x[1], reverse=True)

    result = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        debtor, d_amt = debtors[i]
        creditor, c_amt = creditors[j]

        pay = min(-d_amt, c_amt)

        if pay > 0:
            result.append((debtor, creditor, pay))

        # update remaining
        debtors[i] = (debtor, d_amt + pay)
        creditors[j] = (creditor, c_amt - pay)

        if debtors[i][1] >= 0:
            i += 1
        if creditors[j][1] <= 0:
            j += 1

    return result