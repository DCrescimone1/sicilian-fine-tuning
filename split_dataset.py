import json
import os
import random
import logging

# Configure logging for terminal output only
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Only log to console/terminal
    ]
)

def split_dataset(input_file, train_file, val_file, val_split=0.1, seed=42):
    """
    Split a JSONL dataset into training and validation sets.
    
    Args:
        input_file: Path to the input JSONL file
        train_file: Path for the output training file
        val_file: Path for the output validation file
        val_split: Fraction of data to use for validation (default: 0.1)
        seed: Random seed for reproducibility (default: 42)
    """
    try:
        logging.info(f"Starting to split dataset: {input_file}")
        
        # Check if input file exists
        if not os.path.exists(input_file):
            logging.error(f"Input file not found: {input_file}")
            return False
        
        # Check file size
        input_size = os.path.getsize(input_file)
        logging.info(f"Input file size: {input_size} bytes")
        
        if input_size == 0:
            logging.error(f"Input file {input_file} is empty")
            return False
        
        # Set random seed for reproducibility
        random.seed(seed)
        
        # Read all examples from the input file
        logging.info(f"Reading examples from {input_file}")
        examples = []
        with open(input_file, 'r', encoding='utf-8') as f:
            line_count = 0
            for line in f:
                line_count += 1
                try:
                    # Verify valid JSON
                    json_obj = json.loads(line)
                    examples.append(line)
                    if line_count <= 3:  # Log first few examples
                        logging.info(f"Example {line_count}: {line[:100]}...")
                except json.JSONDecodeError as e:
                    logging.error(f"JSON decode error in line {line_count}: {e}")
                    logging.error(f"Problematic line: {line[:100]}...")
                
                # Show progress for large files
                if line_count % 10000 == 0:
                    logging.info(f"Read {line_count} lines so far")
        
        logging.info(f"Read {len(examples)} valid examples from {input_file}")
        
        # Check if we have any examples
        if not examples:
            logging.error(f"No valid examples found in {input_file}")
            return False
        
        # Shuffle the data
        logging.info("Shuffling examples")
        random.shuffle(examples)
        
        # Calculate split point
        val_size = int(len(examples) * val_split)
        train_size = len(examples) - val_size
        
        logging.info(f"Splitting into {train_size} training examples and {val_size} validation examples")
        
        # Split the data
        train_data = examples[val_size:]
        val_data = examples[:val_size]
        
        # Write training data
        logging.info(f"Writing training data to {train_file}")
        with open(train_file, 'w', encoding='utf-8') as f:
            for line in train_data:
                f.write(line)
        
        # Write validation data
        logging.info(f"Writing validation data to {val_file}")
        with open(val_file, 'w', encoding='utf-8') as f:
            for line in val_data:
                f.write(line)
        
        # Verify the output files have content
        train_size = os.path.getsize(train_file)
        val_size = os.path.getsize(val_file)
        
        logging.info(f"Output file sizes: Training: {train_size} bytes, Validation: {val_size} bytes")
        
        if train_size == 0 or val_size == 0:
            logging.warning("One or both output files are empty!")
        else:
            logging.info("Dataset split successfully completed")
        
        return True
    
    except Exception as e:
        logging.error(f"Error splitting dataset: {str(e)}")
        return False

def main():
    """Main function to run the dataset splitting process."""
    logging.info("Starting dataset splitting process")
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"Base directory: {base_dir}")
    
    # List all files in the directory for debugging
    logging.info("Files in the base directory:")
    for file in os.listdir(base_dir):
        file_size = os.path.getsize(os.path.join(base_dir, file))
        logging.info(f"  {file} ({file_size} bytes)")
    
    # Process English to Sicilian dataset
    en_to_scn_input = os.path.join(base_dir, "sicilian_translation_en_to_scn.jsonl")
    train_output = os.path.join(base_dir, "sicilian_translation_train.jsonl")
    val_output = os.path.join(base_dir, "sicilian_translation_val.jsonl")
    
    if os.path.exists(en_to_scn_input):
        logging.info(f"Found English to Sicilian input file: {en_to_scn_input}")
        split_dataset(en_to_scn_input, train_output, val_output)
    else:
        logging.warning(f"English to Sicilian input file not found: {en_to_scn_input}")
        
        # Try alternate input sources
        alternate_inputs = [
            os.path.join(base_dir, "sicilian_translation_scn_to_en.jsonl"),
            # Add any other potential input files here
        ]
        
        for alt_input in alternate_inputs:
            if os.path.exists(alt_input):
                logging.info(f"Found alternate input file: {alt_input}")
                if split_dataset(alt_input, train_output, val_output):
                    break
        else:
            logging.error("No valid input files found to process!")

if __name__ == "__main__":
    main()