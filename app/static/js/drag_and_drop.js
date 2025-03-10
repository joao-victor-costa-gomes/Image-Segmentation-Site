const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const uploadForm = document.getElementById('upload-form');

// Evita o comportamento padrão para eventos de arrastar e soltar
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
    dropArea.addEventListener(event, e => e.preventDefault());
});

// Adiciona classe quando a imagem é arrastada sobre a área
dropArea.addEventListener('dragover', () => {
    dropArea.classList.add('dragover');
});

// Remove a classe quando a imagem sai da área
dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
});

// Quando o arquivo é solto na área
dropArea.addEventListener('drop', (e) => {
    dropArea.classList.remove('dragover');

    // Obtém o arquivo solto e atribui ao input
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        uploadForm.submit(); // Envia o formulário automaticamente
    }
});

// Envia automaticamente ao selecionar o arquivo via clique
fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        uploadForm.submit();
    }
});


