import pandas as pd
from src.services.invoice_processor import InvoiceProcessor

def test_calculate_average(tmp_path):
    # Cria um CSV temporário
    csv_content = """customer,account,month,invoice
    C1000,A1100,2019-12-01,100.0
    C1000,A1100,2019-11-01,50.0
    C1000,A1100,2019-10-01,20.0
    """
    csv_file = tmp_path / "invoices.csv"
    csv_file.write_text(csv_content)

    # Testa o processador
    processor = InvoiceProcessor(csv_file)
    result = processor.calculate_average([3]).round(2)
    assert result.iloc[0]["avg_invoices_last_3_months"] == 56.66  # Verifica a média
