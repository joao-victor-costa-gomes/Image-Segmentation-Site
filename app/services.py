# FUNÇÕES IMPORTANTES

import os 
from datetime import datetime
from werkzeug.utils import secure_filename
from segmentation.thresholding import apply_binary_threshold

def verify_file_extension(filename, allowed_extensions):
    """Verifica se o arquivo possui extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, upload_folder):
    """Salva um arquivo enviado no diretório de uploads."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{timestamp}{file_extension}"
    filepath = os.path.join(upload_folder, secure_filename(filename))
    file.save(filepath)
    return filepath