#!/usr/bin/env python3
"""
Convert markdown research file to PDF
"""

from fpdf import FPDF
import re

def markdown_to_pdf(input_md, output_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    with open(input_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Basic markdown to PDF conversion
    pdf.multi_cell(0, 10, content)
    pdf.output(output_pdf)
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python convert_to_pdf.py input.md output.pdf")
        sys.exit(1)
    markdown_to_pdf(sys.argv[1], sys.argv[2])
