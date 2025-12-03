#!/usr/bin/env python3
"""Convert HTML to PDF using Playwright"""
from playwright.sync_api import sync_playwright
from pathlib import Path

html_file = Path('Project_Summary.html')
pdf_file = Path('Project_Summary.pdf')

if not html_file.exists():
    print(f"Error: {html_file} not found. Run convert_to_pdf.py first.")
    exit(1)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load the HTML file
        page.goto(f'file://{html_file.absolute()}')
        
        # Generate PDF
        page.pdf(
            path=str(pdf_file),
            format='Letter',
            margin={'top': '0.75in', 'right': '0.75in', 'bottom': '0.75in', 'left': '0.75in'},
            print_background=True
        )
        
        browser.close()
        print(f"PDF created successfully: {pdf_file}")
except Exception as e:
    print(f"Error creating PDF: {e}")
    print("\nTrying to install playwright browsers...")
    import subprocess
    result = subprocess.run(['python3', '-m', 'playwright', 'install', 'chromium'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("Browsers installed. Please run this script again.")
    else:
        print("Could not install browsers automatically.")
        print("\nAlternative: Open Project_Summary.html in your browser and print to PDF")

