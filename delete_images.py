# Isso é só para deletar as imagens das pastas "processed" e "uploads" antes de enviar pro Github

import os

def clear_image_folders(upload_folder='uploads', processed_folder='processed'):
    allowed_extensions = {'.png', '.jpg', '.jpeg'}

    for folder in [upload_folder, processed_folder]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in allowed_extensions:
                    os.remove(file_path)
            print(f"Todos os arquivos de imagem foram removidos da pasta '{folder}'.")
        else:
            print(f"A pasta '{folder}' não existe.")

if __name__ == "__main__":
    clear_image_folders()