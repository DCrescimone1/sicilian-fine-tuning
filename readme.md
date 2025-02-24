# Guide to Fine-Tuning ChatGPT with Sicilian Dataset

## File Structure
Based on your screenshot, you already have the necessary files:

- **CSV data file**: `Napizia-sc...-scores.csv`
- **Script files**: 
  - `convert_dataset.py` - Converts CSV to JSONL format
  - `split_dataset.py` - Splits dataset into training and validation sets
- **Generated files**:
  - `sicilian_tra...to_scn.jsonl` - English to Sicilian translations
  - `sicilian_tra...to_en.jsonl` - Sicilian to English translations
  - `sicilian_tra...n_train.jsonl` - Training dataset
  - `sicilian_tra...ion_val.jsonl` - Validation dataset

## Step-by-Step Instructions

### 1. Update and Run the Conversion Script

I've provided updated code for `convert_dataset.py` that matches your file structure. 

Run the script in Terminal:
```
cd /path/to/Napizia-sc...LLB.en-scn
python convert_dataset.py
```

This will generate/update:
- `sicilian_tra...to_scn.jsonl` (English to Sicilian)
- `sicilian_tra...to_en.jsonl` (Sicilian to English)

### 2. Run the Split Dataset Script

I've also updated `split_dataset.py` to match your file structure.

Run the script:
```
python split_dataset.py
```

This will generate/update:
- `sicilian_tra...n_train.jsonl` (Training set)
- `sicilian_tra...ion_val.jsonl` (Validation set)

### 3. Upload to ChatGPT for Fine-Tuning

1. Go to the OpenAI fine-tuning interface
2. Click "Create" to start a new fine-tuning job
3. For training data:
   - Select "Upload new"
   - Upload `sicilian_tra...n_train.jsonl`
4. For validation data:
   - Select "Upload new"
   - Upload `sicilian_tra...ion_val.jsonl`
5. Configure settings:
   - Method: Supervised
   - Base Model: gpt-4o-mini-2024-07-18
   - Suffix: sicilian-translator
   - Batch size: 4
   - Epochs: 3 (if available)
   - Learning rate multiplier: 1.5 (if available)
6. Click "Create" to start the fine-tuning

## Notes

- You can fine-tune two different models:
  - One for English-to-Sicilian translation (using `sicilian_tra...to_scn.jsonl`)
  - One for Sicilian-to-English translation (using `sicilian_tra...to_en.jsonl`)
  
- The files in your directory with truncated names match the expected output files from the scripts.

- If the scripts fail, check that the file paths exactly match your actual files.