# llama-encoding/modules/extract.py

'''
Dependencies

    psycopg -> needed to access postgres database

'''

import psycopg
from dotenv import load_dotenv # Corrected import
import os

def main():
    load_dotenv() # Corrected function call
    
    name = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    pwd = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    data_dir = os.getenv('DATA_DIR') # Assuming DATA_DIR is also an environment variable


    # Connect to an existing database
    try:
        with psycopg.connect(f"dbname={name} user={user} password={pwd} host={host} port={port}") as conn: # Corrected connection string

            # Open a cursor to perform database operations
            with conn.cursor() as cur:

                cur.execute("""
                            SELECT
                                prompts.id AS prompt_id,
                                prompts.text
                            FROM
                                gpt_o4_prompts AS prompts
                            INNER JOIN
                                gpt_o4_raw_outputs AS responses
                            ON
                                prompts.id = CAST(responses.request_id AS INTEGER)
                            ORDER BY
                                prompts.id ASC;
                            """)
                rows = cur.fetchall()
                print(f"Retrieved {len(rows)} rows.")
                
                for row in rows:
                    prompt_id, response_text = row
                    file_path = os.path.join(data_dir, f"{prompt_id}.txt") # Using data_dir variable

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"Text ID: {prompt_id}\n")
                        f.write(f"Response:\n{response_text or '[NO RESPONSE]'}")

            # No need to explicitly close cursor and connection with 'with' statements
            print("Data extraction complete.")

    except Exception as e:
        print(f"Error connecting to database or executing query: {e}")


if __name__ == "__main__":
    main()
