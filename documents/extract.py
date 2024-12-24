import PyPDF2
import pytesseract
from pytesseract import Output
from pdf2image import convert_from_path
import openai
import json
import anthropic

#from transformers import AutoTokenizer, AutoModelForCausalLM
#import torch
import json

# # Example: a smaller model to illustrate, but it may not perform well for complex extraction
# model_name = "microsoft/DialoGPT-small"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# Configure OpenAI API key here
# 

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # Read PDF text
        reader = PyPDF2.PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

# Function to extract text from scanned PDFs using OCR

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    ocr_text = ""
    for image in images:
        ocr_text += pytesseract.image_to_string(image, lang="eng")
    return ocr_text

# Function to call GPT model for structured field extraction
def extract_fields_with_ai(pdf_text):
    try:
        prompt = f"""
        Extract the following fields from the text below. Only return a JSON object mapping the fields below to values found (if any) and the confidence score for that value:
        Fields:
        - bill of lading number (string)
        - invoice number (string)
        - shipper name (string)
        - shipper address (string)
        - consignee name (string)
        - consignee address (string)
        - line items (array): each line item contains quantity (number), description (string), value (number), HTS code (string)
        - total value of goods (number)
        
        Text:
        {pdf_text}
        """
        response = openai.completions.create(
             model="gpt-3.5-turbo",
             prompt=prompt,
             max_tokens = 500
        )


        extracted_data = response['choices'][0]['text'].strip()
        return json.loads(extracted_data)

    except Exception as e:
        print(f"Error calling AI API: {e}")
        return None

# Anthropic

import anthropic
import json

def extract_fields_with_anthropic(pdf_text):
    try:
        # Prepare the prompt
        prompt = f"""
        Extract the following fields from the text below. Only return a JSON object mapping the fields below to values found (if any) and the confidence score for that value:
        Fields:
        - bill of lading number (string)
        - invoice number (string)
        - shipper name (string)
        - shipper address (string)
        - consignee name (string)
        - consignee address (string)
        - line items (array): each line item contains quantity (number), description (string), value (number), HTS code (string)
        - total value of goods (number)
        
        Text:
        {pdf_text}
        """

        # Create a client
        #
        #client = anthropic.Client()
        
        # Use Claude (e.g., 'claude-v1') or whichever model is available to you
        response = client.completions.create(
            model="claude-v1",
            prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
            max_tokens_to_sample=500,
            temperature=0.2
        )

        # The text field will contain the LLM's raw output
        print(response["completion"].strip())
        extracted_data_str = response["completion"].strip()
        return json.loads(extracted_data_str)
        
    except Exception as e:
        print(f"Error calling Anthropic API: {e}")
        return None

# #Hugging face
# def extract_fields_with_hf(pdf_text):
#     prompt = f"""
#     Extract the following fields from the text below. Only return a JSON object mapping the fields below to values found (if any) and the confidence score for that value:
#     Fields:
#     - bill of lading number (string)
#     - invoice number (string)
#     - shipper name (string)
#     - shipper address (string)
#     - consignee name (string)
#     - consignee address (string)
#     - line items (array): each line item contains quantity (number), description (string), value (number), HTS code (string)
#     - total value of goods (number)
    
#     Text:
#     {pdf_text}
#     """

#     input_ids = tokenizer.encode(prompt, return_tensors='pt')
#     # You can tweak max_length, temperature, etc.
#     outputs = model.generate(
#         input_ids,
#         max_length=512,
#         num_beams=1,
#         no_repeat_ngram_size=2
#     )
#     raw_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
#     # Attempt to parse as JSON (depends on the model's output)
#     try:
#         extracted_data = json.loads(raw_output)
#         return extracted_data
#     except json.JSONDecodeError:
#         print("Could not parse the model's output as JSON.")
#         return None


# Main function to process the PDF and extract fields
def process_pdf(pdf_path):
    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():  # Fallback to OCR if no text is found
        text = extract_text_with_ocr(pdf_path)
    
    # Step 2: Use AI to parse and identify fields
    extracted_data = extract_fields_with_anthropic(text)
    
    # Step 3: Add confidence values (default if missing)
    if extracted_data:
        for key, value in extracted_data.items():
            if isinstance(value, dict) and "confidence" not in value:
                value["confidence"] = -0.1  # Default confidence score

    return extracted_data

# Example usage
if __name__ == "__main__":
    pdf_file = "sample_shipping_doc.pdf"  # Replace with the path to your PDF
    extracted_data = process_pdf(pdf_file)
    print(json.dumps(extracted_data, indent=2))
