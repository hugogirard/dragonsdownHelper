#!/usr/bin/env python3
"""
Convert Dragons Down PDF to Markdown
"""

import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        
        print(f"Total pages: {len(pdf_reader.pages)}")
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            print(f"Processing page {page_num}...")
            page_text = page.extract_text()
            text += f"\n\n--- Page {page_num} ---\n\n"
            text += page_text
        
        return text

def clean_text(text):
    """Clean and format the extracted text"""
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    # Remove multiple newlines
    text = re.sub(r'\n\n+', '\n\n', text)
    return text.strip()

def save_to_markdown(text, output_path):
    """Save text to markdown file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Dragons Down Cyclopedia\n\n")
        f.write(text)
    print(f"Markdown saved to: {output_path}")

def main():
    pdf_path = "docs/Dragons_Down_Cyclopedia.pdf"
    output_path = "docs/Dragons_Down_Cyclopedia.md"
    
    print("Starting PDF conversion...")
    text = extract_text_from_pdf(pdf_path)
    
    print("Cleaning text...")
    cleaned_text = clean_text(text)
    
    print("Saving to markdown...")
    save_to_markdown(cleaned_text, output_path)
    
    print("Done!")
    print(f"\nExtracted {len(cleaned_text)} characters")

if __name__ == "__main__":
    main()
