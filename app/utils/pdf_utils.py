import subprocess
import logging
import os
from pathlib import Path
from weasyprint import HTML, CSS

def get_pdf2htmlex_path():
    current_dir = Path(__file__).parent.parent.parent  
    pdf2html_path = current_dir / 'pdf2htmlEX' / 'pdf2htmlEX.exe'
    return str(pdf2html_path)

def pdf_to_html(pdf_path, output_html_path):
    try:
        pdf2html_exe = get_pdf2htmlex_path()
        subprocess.run([pdf2html_exe, pdf_path, output_html_path], check=True)
        logging.debug(f"Converted PDF to HTML: {output_html_path}")
        
        with open(output_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return html_content
    except Exception as e:
        logging.error(f"Error converting PDF to HTML: {e}")
        raise

def html_to_pdf(html_content, output_pdf_path):
    try:
        css = CSS(string='''
            @page { size: A3; margin: 1cm; }
            body { font-family: Arial, sans-serif; }
            h1, h2, h3, h4, h5, h6 { font-weight: bold; }
            p { margin: 0.5cm 0; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #000; padding: 0.5cm; text-align: left; }
            img { max-width: 100%; height: auto; }
            .pdf-content { margin: 0 auto; max-width: 800px; }
        ''')
        HTML(string=html_content).write_pdf(output_pdf_path, stylesheets=[css])
        logging.debug(f"Converted HTML to PDF: {output_pdf_path}")
    except Exception as e:
        logging.error(f"Error converting HTML to PDF: {e}")
        raise