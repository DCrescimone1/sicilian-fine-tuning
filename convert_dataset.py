import csv
import json
import os
import gzip
import logging

# Configure logging for terminal output only
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Only log to console/terminal
    ]
)

def process_csv_file(input_csv_path, output_en_to_scn_path, output_scn_to_en_path):
    """Process the CSV file and convert to JSONL format for both translation directions."""
    try:
        logging.info(f"Starting to process CSV file: {input_csv_path}")
        
        # Check if input file exists
        if not os.path.exists(input_csv_path):
            logging.error(f"Input file not found: {input_csv_path}")
            return False
        
        # Determine whether the file is gzipped
        is_gzipped = input_csv_path.endswith('.gz')
        logging.info(f"Input file is gzipped: {is_gzipped}")
        
        # Initialize counters
        total_rows = 0
        en_to_scn_count = 0
        scn_to_en_count = 0
        
        # Open output files
        with open(output_en_to_scn_path, 'w', encoding='utf-8') as en_to_scn_file, \
             open(output_scn_to_en_path, 'w', encoding='utf-8') as scn_to_en_file:
            
            logging.info(f"Opened output files: {output_en_to_scn_path} and {output_scn_to_en_path}")
            
            # Open and process the input file
            if is_gzipped:
                with gzip.open(input_csv_path, 'rt', encoding='utf-8') as csvfile:
                    # Use tab as delimiter instead of comma
                    reader = csv.reader(csvfile, delimiter='\t')
                    logging.info("Opened gzipped CSV file with tab delimiter")
                    total_rows, en_to_scn_count, scn_to_en_count = process_rows(reader, en_to_scn_file, scn_to_en_file)
            else:
                with open(input_csv_path, 'r', encoding='utf-8') as csvfile:
                    # Use tab as delimiter instead of comma
                    reader = csv.reader(csvfile, delimiter='\t')
                    logging.info("Opened regular CSV file with tab delimiter")
                    total_rows, en_to_scn_count, scn_to_en_count = process_rows(reader, en_to_scn_file, scn_to_en_file)
                    
        logging.info(f"Processing complete. Processed {total_rows} total rows.")
        logging.info(f"Created {en_to_scn_count} English to Sicilian examples.")
        logging.info(f"Created {scn_to_en_count} Sicilian to English examples.")
        
        # Check if output files have content
        en_to_scn_size = os.path.getsize(output_en_to_scn_path)
        scn_to_en_size = os.path.getsize(output_scn_to_en_path)
        
        logging.info(f"Output file sizes: EN->SCN: {en_to_scn_size} bytes, SCN->EN: {scn_to_en_size} bytes")
        
        if en_to_scn_size == 0 or scn_to_en_size == 0:
            logging.warning("One or both output files are empty!")
        
        return True
    
    except Exception as e:
        logging.error(f"Error processing CSV file: {str(e)}")
        return False

def process_rows(reader, en_to_scn_file, scn_to_en_file):
    """Process each row of the CSV file and write to output files."""
    total_rows = 0
    en_to_scn_count = 0
    scn_to_en_count = 0
    
    # Check if the CSV has a header
    has_header = True  # Assume there's a header by default
    
    try:
        for i, row in enumerate(reader):
            if i == 0:
                # Log the first row to help identify if it's a header
                logging.info(f"First row: {row}")
                
                # Try to detect if this is a header
                if len(row) >= 2:
                    # If first two columns look like 'id', 'source', 'target', etc., it's likely a header
                    if any(col.lower() in ['id', 'source', 'target', 'english', 'sicilian', 'en', 'scn'] for col in row[:3]):
                        logging.info("Header detected, skipping first row")
                        continue
                    else:
                        logging.info("No header detected, processing all rows")
                        has_header = False
                        
            total_rows += 1
            
            # Log every 10000 rows to show progress
            if total_rows % 10000 == 0:
                logging.info(f"Processed {total_rows} rows so far")
            
            try:
                # For tab-delimited files, we expect at least 2 columns
                # From the logs, it appears columns 0 and 1 contain English and Sicilian text
                if len(row) >= 2:
                    english_text = row[0].strip()
                    sicilian_text = row[1].strip()
                    
                    # Skip empty translations
                    if not english_text or not sicilian_text:
                        logging.warning(f"Skipping row {total_rows} due to empty text: {row}")
                        continue
                    
                    # Create the JSON objects for both directions
                    en_to_scn_obj = {
                        "messages": [
                            {"role": "system", "content": "You are a helpful translator that translates from English to Sicilian."},
                            {"role": "user", "content": f"Translate this English text to Sicilian: {english_text}"},
                            {"role": "assistant", "content": sicilian_text}
                        ]
                    }
                    
                    scn_to_en_obj = {
                        "messages": [
                            {"role": "system", "content": "You are a helpful translator that translates from Sicilian to English."},
                            {"role": "user", "content": f"Translate this Sicilian text to English: {sicilian_text}"},
                            {"role": "assistant", "content": english_text}
                        ]
                    }
                    
                    # Write to output files
                    json.dump(en_to_scn_obj, en_to_scn_file, ensure_ascii=False)
                    en_to_scn_file.write('\n')
                    en_to_scn_count += 1
                    
                    json.dump(scn_to_en_obj, scn_to_en_file, ensure_ascii=False)
                    scn_to_en_file.write('\n')
                    scn_to_en_count += 1
                else:
                    # Modified to only log once per 1000 issues to reduce log spam
                    if total_rows % 1000 == 0:
                        logging.warning(f"Row {total_rows} does not have enough columns: {row}")
            
            except Exception as e:
                logging.error(f"Error processing row {total_rows}: {str(e)}")
                if total_rows % 1000 == 0:  # Reduce log spam
                    logging.error(f"Problematic row: {row}")
                
    except Exception as e:
        logging.error(f"Error during row processing: {str(e)}")
    
    return total_rows, en_to_scn_count, scn_to_en_count

def main():
    """Main function to run the conversion process."""
    logging.info("Starting conversion process")
    
    # Try different possible file paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"Base directory: {base_dir}")
    
    # List all potential CSV input files (check both gzipped and non-gzipped)
    potential_input_files = [
        os.path.join(base_dir, "Napizia-scored-NLLB.en-scn", "Napizia-scored-NLLB-en-scn_50k-w-scores.csv.gz"),
        os.path.join(base_dir, "Napizia-scored-NLLB.en-scn", "Napizia-scored-NLLB-en-scn_all-w-scores.csv"),
        os.path.join("Napizia-scored-NLLB.en-scn", "Napizia-scored-NLLB-en-scn_50k-w-scores.csv.gz"),
        os.path.join("Napizia-scored-NLLB.en-scn", "Napizia-scored-NLLB-en-scn_all-w-scores.csv"),
        os.path.join(base_dir, "Napizia-scored-NLLB-en-scn_50k-w-scores.csv.gz"),
        os.path.join(base_dir, "Napizia-scored-NLLB-en-scn_all-w-scores.csv")
    ]
    
    # Output file paths
    output_en_to_scn = os.path.join(base_dir, "sicilian_translation_en_to_scn.jsonl")
    output_scn_to_en = os.path.join(base_dir, "sicilian_translation_scn_to_en.jsonl")
    
    # List all files in base directory and Napizia subdirectory for debugging
    logging.info("Listing files in base directory:")
    for file in os.listdir(base_dir):
        logging.info(f"  {file}")
    
    napizia_dir = os.path.join(base_dir, "Napizia-scored-NLLB.en-scn")
    if os.path.exists(napizia_dir):
        logging.info(f"Listing files in {napizia_dir}:")
        for file in os.listdir(napizia_dir):
            logging.info(f"  {file}")
    else:
        logging.warning(f"Napizia directory not found: {napizia_dir}")
    
    # Try each potential input file
    success = False
    for input_file in potential_input_files:
        if os.path.exists(input_file):
            logging.info(f"Found input file: {input_file}")
            if process_csv_file(input_file, output_en_to_scn, output_scn_to_en):
                success = True
                break
    
    if not success:
        logging.error("Could not find or process any suitable input CSV file!")
        logging.error("Please check that one of these files exists:")
        for file in potential_input_files:
            logging.error(f"  - {file}")

if __name__ == "__main__":
    main()