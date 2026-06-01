from decimal import Decimal


# =========================
# CALCULATE SUPPLIER BALANCE
# =========================
def calculate_supplier_balance(credits, payments):

    total_credit = sum(
        credit.total_cost
        for credit in credits
    )

    total_paid = sum(
        payment.amount_paid
        for payment in payments
    )

    return Decimal(total_credit - total_paid)