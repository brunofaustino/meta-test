from flask import Flask, request, jsonify
from services.invoice_processor import InvoiceProcessor
from services.chatbot_report import ChatbotReport
from utils.file_reader import list_json_files
import os

app = Flask(__name__)

# Configurações gerais
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")


# Rota para processar invoices
@app.route("/api/invoices", methods=["GET"])
def process_invoices():
    try:
        months = request.args.get("months", "3,6")
        months = [int(x) for x in months.split(",")]

        processor = InvoiceProcessor(os.path.join(DATA_DIR, "invoices.csv"))
        avg_invoices = processor.calculate_average(months)

        return jsonify(avg_invoices.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para consolidar relatórios de chatbot
@app.route("/api/chatbot", methods=["GET"])
def consolidate_chatbot_reports():
    try:
        json_files = list_json_files(DATA_DIR)
        chatbot_data = ChatbotReport.consolidate_reports(json_files)
        return jsonify(chatbot_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Teste básico
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API está funcionando"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)
