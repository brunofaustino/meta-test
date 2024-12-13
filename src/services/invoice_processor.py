import pandas as pd
from datetime import datetime, timedelta


class InvoiceProcessor:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def calculate_average(self, months_window, reference_date="2020-01-01"):
        df = pd.read_csv(self.csv_path)

        df["month"] = pd.to_datetime(df["month"])
        reference_date = datetime.strptime(reference_date, "%Y-%m-%d")

        results = []
        for (customer, account), group in df.groupby(["customer", "account"]):
            for months in months_window:
                start_date = reference_date - timedelta(days=30 * months)
                filtered = group[(group["month"] >= start_date) & (group["month"] < reference_date)]

                avg_invoice = filtered["invoice"].mean() if not filtered.empty else None
                results.append({
                    "customer": customer,
                    "account": account,
                    f"avg_invoices_last_{months}_months": round(avg_invoice, 2) if avg_invoice else None
                })

        return pd.DataFrame(results)
