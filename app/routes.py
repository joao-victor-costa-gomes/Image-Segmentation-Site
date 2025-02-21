import os
from flask import Blueprint, render_template, request, current_app, send_from_directory, redirect, url_for
from app.services import save_uploaded_image, ensure_folder_exists

from app.services import apply_threshold, apply_canny_edge, apply_region_based, apply_clustering_based, apply_color_based, apply_watershed

# Criando um Blueprint contendo todas essas rotas abaixo
main = Blueprint('main', __name__)

@main.route('/')
def home_page():
    return render_template('home.html')

# Rota para servir os arquivos da pasta uploads/
@main.route('/uploads/<filename>')
def uploaded_file_path(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# Rota para servir os arquivos da pasta processed/
@main.route('/processed/<filename>')
def processed_file_path(filename):
    return send_from_directory(current_app.config['PROCESSED_FOLDER'], filename)


@main.route('/threshold', methods=['GET', 'POST'])
def threshold_page():
    filename = None
    segmented_filenames = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            filename = save_uploaded_image(file)  

        if 'apply_threshold' in request.form:
            # PEGANDO PARÂMETROS
            filename = request.form.get('filename')
            threshold_value = request.form.get('threshold_value', type=int)
            block_size = request.form.get('block_size', type=int)
            c_value = request.form.get('c_value', type=int)

            if filename is not None:
                # APLICANDO MÉTODO DE SEGMENTAÇÃO
                segmented_filenames = apply_threshold(filename, threshold_value, block_size, c_value)

                if segmented_filenames:
                    ensure_folder_exists(current_app.config['PROCESSED_FOLDER'])  

    return render_template('threshold.html', filename=filename, segmented_filenames=segmented_filenames)


@main.route('/canny_edge', methods=['GET', 'POST'])
def canny_edge_page():
    filename = None
    segmented_filenames = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            filename = save_uploaded_image(file)  

        if 'apply_canny_edge' in request.form:
            # PEGANDO PARÂMETROS
            filename = request.form.get('filename')
            min_val = request.form.get('min_val', type=int)
            max_val = request.form.get('max_val', type=int)

            if filename and min_val is not None:
                # APLICANDO MÉTODO DE SEGMENTAÇÃO
                segmented_filenames = apply_canny_edge(filename, min_val, max_val)

                if segmented_filenames:
                    ensure_folder_exists(current_app.config['PROCESSED_FOLDER'])  

    return render_template('edge_based.html', filename=filename, segmented_filenames=segmented_filenames)


@main.route('/region_based', methods=['GET', 'POST'])
def region_based_page():
    filename = None
    segmented_filenames = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            filename = save_uploaded_image(file)  

        if 'apply_region_based' in request.form:
            # PEGANDO PARÂMETROS
            filename = request.form.get('filename')
            num_regions = request.form.get('num_regions', type=int)

            x = request.form.get('seed_point_x', type=int)
            y = request.form.get('seed_point_y', type=int)
            threshold = request.form.get('threshold', type=int)

            if filename is not None:
                # APLICANDO MÉTODO DE SEGMENTAÇÃO
                segmented_filenames = apply_region_based(filename, (x, y), threshold)

                if segmented_filenames:
                    ensure_folder_exists(current_app.config['PROCESSED_FOLDER'])  

    return render_template('region_based.html', filename=filename, segmented_filenames=segmented_filenames)


@main.route('/clustering_based', methods=['GET', 'POST'])
def clustering_based_page():
    filename = None
    segmented_filenames = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            filename = save_uploaded_image(file)  

        if 'apply_clustering_based' in request.form:
            # PEGANDO PARÂMETROS
            filename = request.form.get('filename')
            k = request.form.get('k', type=int)
            attempts = request.form.get('attempts', type=int)

            if filename is not None:
                # APLICANDO MÉTODO DE SEGMENTAÇÃO
                segmented_filenames = apply_clustering_based(filename, k, attempts)

                if segmented_filenames:
                    ensure_folder_exists(current_app.config['PROCESSED_FOLDER'])  

    return render_template('clustering_based.html', filename=filename, segmented_filenames=segmented_filenames)


@main.route('/color_based', methods=['GET', 'POST'])
def color_based_page():
    filename = None
    segmented_filenames = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            filename = save_uploaded_image(file)  

        if 'apply_color_based' in request.form:
            # PEGANDO PARÂMETROS
            filename = request.form.get('filename')
            h_min = request.form.get('h_min', type=int)
            h_max = request.form.get('h_max', type=int)
            s_min = request.form.get('s_min', type=int)
            s_max = request.form.get('s_max', type=int)
            v_min = request.form.get('v_min', type=int)
            v_max = request.form.get('v_max', type=int)

            if filename is not None:
                # APLICANDO MÉTODO DE SEGMENTAÇÃO
                segmented_filenames = apply_color_based(filename, (h_min, s_min, v_min), (h_max, s_max, v_max))

                if segmented_filenames:
                    ensure_folder_exists(current_app.config['PROCESSED_FOLDER'])  

    return render_template('color_based.html', filename=filename, segmented_filenames=segmented_filenames)

@main.route('/watershed', methods=['GET', 'POST'])
def watershed_page():
    filename = None
    segmented_filenames = None

    if request.method == 'POST':
        if 'image' in request.files:
            file = request.files['image']
            filename = save_uploaded_image(file)  

        if 'apply_watershed' in request.form:
            # PEGANDO PARÂMETROS
            filename = request.form.get('filename')

            if filename is not None:
                # APLICANDO MÉTODO DE SEGMENTAÇÃO
                segmented_filenames = apply_watershed(filename)

                if segmented_filenames:
                    ensure_folder_exists(current_app.config['PROCESSED_FOLDER'])  

    return render_template('watershed.html', filename=filename, segmented_filenames=segmented_filenames)