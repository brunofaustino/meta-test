from services.invoice_processor import InvoiceProcessor
from services.chatbot_report import ChatbotReport
from utils.file_reader import list_json_files

import os

def main():
    # Processamento de Invoices
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    processor = InvoiceProcessor(os.path.join(data_dir, "invoices.csv"))
    avg_invoices = processor.calculate_average([3, 6])
    print("Média de faturamento:")
    print(avg_invoices)

    # Consolidação de relatórios de chatbot
    json_files = list_json_files("data/")
    chatbot_data = ChatbotReport.consolidate_reports(json_files)
    print("\nRelatório Consolidado de Chatbot:")
    for session in chatbot_data:
        print(session)

if __name__ == "__main__":
    main()
