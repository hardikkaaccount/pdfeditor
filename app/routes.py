from flask import Blueprint, render_template, request, redirect, url_for, send_file, current_app
from werkzeug.utils import secure_filename
import os
import logging
from .utils.pdf_utils import pdf_to_html, html_to_pdf

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.error("No file part in the request")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            logging.error("No selected file or file type not allowed")
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        output_html_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'output.html')
        try:
            file.save(file_path)
            html_content = pdf_to_html(file_path, output_html_path)
            return render_template('editor.html', content=html_content)
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            return redirect(request.url)
    return render_template('upload.html')

@bp.route('/export', methods=['POST'])
def export_file():
    html_content = request.form['editor']
    output_pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'output.pdf')
    try:
        logging.debug(f"Exporting HTML content to PDF: {html_content[:100]}...") 
        html_to_pdf(html_content, output_pdf_path)
        logging.debug(f"PDF successfully created at: {output_pdf_path}")
        return send_file(output_pdf_path, as_attachment=True)
    except Exception as e:
        logging.error(f"Error exporting file: {e}")
        return redirect(url_for('main.index'))