import sqlite3
import pandas as pd
import os

def main():
    # install openpyxl
    # Path to database
    db_path = r"_PATH_"

    # Connect to the database (creates it if it doesn’t exist)
    conn = sqlite3.connect(db_path)

    # Folder where your Excel files are stored
    xlsx_folder = r"_PATH_"

    # Find all Excel files
    xlsx_files = [f for f in os.listdir(xlsx_folder) if f.lower().endswith('.xlsx')]

    for xlsx_file in xlsx_files:
        file_path = os.path.join(xlsx_folder, xlsx_file)

        # List all sheet names in the workbook
        xls = pd.ExcelFile(file_path)
        print(f"\nProcessing {xlsx_file}")

        for sheet in xls.sheet_names:
            # Load sheet
            df = pd.read_excel(file_path, header=1, sheet_name=sheet)

            if df.empty:
                print(f"  Skipping empty sheet: {sheet}")
                continue

            # Make a safe table name: file name
            table_name = os.path.splitext(xlsx_file)[0]
            table_name = table_name.replace(" ", "_").replace("-", "_")

            # Save to SQLite
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"  → Loaded {len(df)} rows into {table_name}")

    # Show all tables created
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    print("\nTables created:\n", tables)

    conn.close()

if __name__ == "__main__":
    main()