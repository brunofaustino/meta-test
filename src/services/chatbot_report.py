import json
from datetime import datetime


class ChatbotReport:
    @staticmethod
    def consolidate_reports(json_files):
        consolidated_data = []

        for file_path in json_files:
            with open(file_path, "r") as file:
                data = json.load(file)
                sessions = {}

                for record in data:
                    customer = record["customer"]
                    flow = record["flow"]
                    session = record["session"]
                    timestamp = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))

                    if session not in sessions:
                        sessions[session] = {
                            "customer": customer,
                            "flow": flow,
                            "session": session,
                            "first_answer_dt": timestamp,
                            "last_answer_dt": timestamp,
                            **record["content"]  # Adiciona respostas de usuários
                        }
                    else:
                        sessions[session]["last_answer_dt"] = max(sessions[session]["last_answer_dt"], timestamp)
                        sessions[session].update({k: v for k, v in record["content"].items() if v})

                consolidated_data.extend(sessions.values())

        return consolidated_data
