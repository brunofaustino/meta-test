import argparse
import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def filter_data_by_date(df: pd.DataFrame, reference_date: pd.Timestamp, months: int) -> pd.DataFrame:
    start_date = reference_date - pd.DateOffset(months=months)
    return df[df['month'] >= start_date]

def calculate_averages(group: pd.DataFrame, reference_date: pd.Timestamp) -> dict:
    group = group.sort_values(by='month', ascending=False)

    last_3_months = filter_data_by_date(group, reference_date, 3)
    last_6_months = filter_data_by_date(group, reference_date, 6)

    avg_3_months = last_3_months['invoice'].mean().round(2) if len(last_3_months) >= 3 else None
    avg_6_months = last_6_months['invoice'].mean().round(2) if len(last_6_months) >= 6 else None

    return {
        'customer': group['customer'].iloc[0],
        'account': group['account'].iloc[0],
        'avg_invoices_last_3_months': avg_3_months,
        'avg_invoices_last_6_months': avg_6_months
    }

def process_invoices(file_path: str, reference_date: str) -> pd.DataFrame:
    df_invoices = load_data(file_path)

    df_invoices['month'] = pd.to_datetime(df_invoices['month'])

    reference_date = pd.Timestamp(reference_date)

    df_filtered = df_invoices[df_invoices['month'] < reference_date]

    results = [
        calculate_averages(group, reference_date)
        for _, group in df_filtered.groupby(['customer', 'account'])
    ]

    return pd.DataFrame(results)

def main():
    parser = argparse.ArgumentParser(description="Process invoices and calculate averages.")
    parser.add_argument('file_path', type=str, help="Path to the invoices CSV file.")
    parser.add_argument('reference_date', type=str, help="Reference date in YYYY-MM-DD format.")
    parser.add_argument('--output', type=str, help="Output file path (optional).", default=None)

    args = parser.parse_args()

    file_path = args.file_path
    reference_date = args.reference_date

    averages_df = process_invoices(file_path, reference_date)

    if args.output:
        averages_df.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")
    else:
        print(averages_df)

if __name__ == "__main__":
    main()