#!/usr/bin/env python3
"""Convert Markdown to print-ready HTML (can be printed to PDF from browser)"""
import markdown
from pathlib import Path
import re

# Read the markdown file
md_file = Path('Project_Summary.md')
with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML with extensions for tables and code
html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'nl2br'])

# Create styled HTML document optimized for printing
html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S&P 500 Stock Regression Project</title>
    <style>
        @page {{
            size: letter;
            margin: 0.75in;
        }}
        
        @media print {{
            body {{
                margin: 0;
                padding: 0;
            }}
            .page-break {{
                page-break-before: always;
            }}
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Times New Roman', 'Times', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
            max-width: 100%;
            margin: 0;
            padding: 20px;
        }}
        
        h1 {{
            font-size: 18pt;
            font-weight: bold;
            margin-top: 0.5em;
            margin-bottom: 0.5em;
            page-break-after: avoid;
            border-bottom: 2px solid #000;
            padding-bottom: 0.3em;
        }}
        
        h2 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            page-break-after: avoid;
            border-bottom: 1px solid #666;
            padding-bottom: 0.2em;
        }}
        
        h3 {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 1em;
            margin-bottom: 0.5em;
            page-break-after: avoid;
        }}
        
        p {{
            margin-bottom: 0.8em;
            text-align: justify;
            orphans: 3;
            widows: 3;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #333;
            padding: 8px;
            text-align: left;
        }}
        
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            font-family: 'Courier New', 'Courier', monospace;
            font-size: 10pt;
            border: 1px solid #ddd;
            border-radius: 3px;
        }}
        
        pre {{
            background-color: #f4f4f4;
            padding: 12px;
            overflow-x: auto;
            font-size: 9pt;
            border: 1px solid #ddd;
            border-radius: 4px;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            border: none;
        }}
        
        ul, ol {{
            margin-bottom: 0.8em;
            padding-left: 2em;
        }}
        
        li {{
            margin-bottom: 0.4em;
        }}
        
        strong {{
            font-weight: bold;
        }}
        
        em {{
            font-style: italic;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid #666;
            margin: 1.5em 0;
        }}
        
        a {{
            color: #0000EE;
            text-decoration: underline;
        }}
        
        a:visited {{
            color: #551A8B;
        }}
        
        /* Fix for markdown tables */
        table thead {{
            display: table-header-group;
        }}
        
        table tfoot {{
            display: table-footer-group;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

# Write HTML file
html_file = Path('Project_Summary.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_document)

print(f"Created print-ready HTML: {html_file}")
print("\nTo create PDF:")
print("1. Open Project_Summary.html in your web browser")
print("2. Press Cmd+P (Mac) or Ctrl+P (Windows/Linux)")
print("3. Select 'Save as PDF' as the destination")
print("4. Click Save")
