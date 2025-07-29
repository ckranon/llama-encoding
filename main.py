# llama-encoding/main.py

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm.auto import tqdm # For progress bars
import csv # Import csv module

def main():
    # --- Configuration ---
    MODEL_NAME = "allenai/Llama-3.1-Tulu-3-8B"
    DATA_DIR = "data" # Directory where extracted texts are stored
    OUTPUT_DIR = "inference_results" # Directory to save inference outputs
    CSV_OUTPUT_FILENAME = "inference_results.csv" # Name of the CSV output file

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Load Model and Tokenizer ---
    print(f"Loading model: {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    # Ensure pad_token is set for batching, if not already
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load model with float16 (FP16) and without quantization
    # Note: FP16 requires more VRAM than 8-bit or 4-bit quantization.
    # Ensure your A100 has sufficient memory for this model at FP16.
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16, # Changed to FP16
        device_map="auto", # Automatically maps model layers to available devices (e.g., GPU)
        # Removed load_in_8bit and load_in_4bit for no quantization
    )
    print("Model loaded successfully.")

    # --- Process Data and Perform Inference ---
    text_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    total_files = len(text_files)
    print(f"Found {total_files} text files in '{DATA_DIR}'.")

    # Prepare list to hold data for CSV
    csv_data = []
    # Add header row to CSV data
    csv_data.append(["prompt_id", "model_output"])

    for filename in tqdm(text_files, desc="Processing files"):
        file_id = os.path.splitext(filename)[0] # Get ID from filename (e.g., "123" from "123.txt")
        file_path = os.path.join(DATA_DIR, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract the response text (skip "Text ID: X" and "Response:\n")
            lines = content.split('\n')
            if len(lines) >= 2 and lines[1].startswith("Response:"):
                prompt_text = "\n".join(lines[2:]) # Everything after "Response:\n"
            else:
                prompt_text = content # Fallback if format is unexpected
            
            # Construct a simple instruction-following prompt
            instruction_prompt = f"Analyze the key themes and overall sentiment of the following parliamentary speech:\n\n{prompt_text}\n\nKey themes and sentiment analysis:"

            inputs = tokenizer(instruction_prompt, return_tensors="pt", padding=True, truncation=True, max_length=model.config.max_position_embeddings).to(model.device)

            # Generate response
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=1, # Changed to 1
                    num_return_sequences=1,
                    do_sample=True,
                    top_p=0.9,
                    temperature=1.0, # Changed to 1.0 (float)
                    eos_token_id=tokenizer.eos_token_id,
                    pad_token_id=tokenizer.pad_token_id # Important for batching
                )

            # Decode the generated text
            generated_text = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
            
            # Add to CSV data
            csv_data.append([file_id, generated_text.strip()])

        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            csv_data.append([file_id, f"Error: {e}"]) # Log error in CSV

    # --- Save all results to a single CSV file ---
    csv_output_path = os.path.join(OUTPUT_DIR, CSV_OUTPUT_FILENAME)
    with open(csv_output_path, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_data)

    print(f"\nInference complete. Results saved to '{csv_output_path}'.")

if __name__ == "__main__":
    main()
