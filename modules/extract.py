# llama-encoding/modules/extract.py

'''
Dependencies

    psycopg2 -> needed to access postgres database

'''

import psycopg2
from dotenv import load_env
import os

def main():
    load_env()
    
    name = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    pwd = os.getenv('DB_PASS')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')


    # Connect to an existing database
    with psycopg.connect("dbname=test user=postgres") as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

        cur.execute("""
                SELECT 
                    prompts.id AS prompt_id,
                    responses.response_text
                FROM 
                    gpt_o4_prompts AS prompts
                LEFT JOIN 
                    gpt_o4_raw_outputs AS responses
                ON 
                    prompts.id = CAST(responses.response_id AS INTEGER);
                    """)
        rows = cur.fetchall()
        print(f"Retrieved {len(rows)} rows.")
        
        for row in rows:
            prompt_id, response_text = row
            file_path = os.path.join(DATA_DIR, f"{prompt_id}.txt")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Text ID: {prompt_id}\n")
                f.write(f"Response:\n{response_text or '[NO RESPONSE]'}")

        cur.close()
        conn.close()



if __name__ == "__main__":
    main()
