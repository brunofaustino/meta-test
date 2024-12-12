import json
import pandas as pd
import argparse
from typing import List, Dict, Any

pd.set_option('display.max_columns', None)

def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {filepath} was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding the JSON file: {filepath}")

def filter_data_by_customer(data: List[Dict[str, Any]], customer_id: str) -> List[Dict[str, Any]]:
    return [entry for entry in data if entry.get("customer") == customer_id]

def process_sessions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sessions = {}

    for entry in data:
        customer = entry.get("customer")
        flow = entry.get("flow")
        session = entry.get("session")
        timestamp = entry.get("timestamp")
        content = entry.get("content", {})

        if not customer or not flow or not session or not timestamp:
            continue  # Ignore invalid entries

        # Initialize the session if needed
        if session not in sessions:
            sessions[session] = {
                "customer": customer,
                "flow": flow,
                "session": session,
                "first_answer_dt": None,
                "last_answer_dt": None,
                "answers": {}
            }

        # Update timestamps of first and last interaction
        if any(content.values()):
            if sessions[session]["first_answer_dt"] is None or timestamp < sessions[session]["first_answer_dt"]:
                sessions[session]["first_answer_dt"] = timestamp
            if sessions[session]["last_answer_dt"] is None or timestamp > sessions[session]["last_answer_dt"]:
                sessions[session]["last_answer_dt"] = timestamp

            # Update answers
            sessions[session]["answers"].update(content)

    report = []
    for session_data in sessions.values():
        row = {
            "customer": session_data["customer"],
            "flow": session_data["flow"],
            "session": session_data["session"],
            "first_answer_dt": session_data["first_answer_dt"],
            "last_answer_dt": session_data["last_answer_dt"],
        }
        row.update(session_data["answers"])
        report.append(row)

    return report

def generate_report(json_files: List[str], customer_filter: str) -> pd.DataFrame:
    all_data = []
    for filepath in json_files:
        all_data.extend(load_json_file(filepath))

    filtered_data = filter_data_by_customer(all_data, customer_filter)
    report = process_sessions(filtered_data)
    return pd.DataFrame(report)

def main():
    parser = argparse.ArgumentParser(description="Generate a report for a specific customer.")
    parser.add_argument("--customer", type=str, required=True, help="Customer ID to filter the report.")
    parser.add_argument("--files", nargs='+', required=True, help="List of JSON files to process.")
    args = parser.parse_args()

    try:
        report_df = generate_report(args.files, args.customer)
        print(report_df)
    except Exception as e:
        print(f"Error generating the report: {e}")

if __name__ == "__main__":
    main()
