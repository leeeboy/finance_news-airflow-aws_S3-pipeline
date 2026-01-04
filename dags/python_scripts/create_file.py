from datetime import datetime, timezone
import pandas as pd
import logging

def write_excel(data):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_name = f"finance-news-{timestamp}.xlsx"
    file_path = f"/tmp/{file_name}"
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    logging.info("filename is f{file_name}")
    return [file_path, file_name]