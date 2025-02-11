const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("file-input");

// Quando o usuário arrasta um arquivo para dentro
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.classList.add("dragover");
});

// Quando o usuário sai da área de drop
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("dragover");
});

// Quando o usuário solta o arquivo
dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("dragover");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
    }
});

// Agora toda a área é clicável
dropArea.addEventListener("click", () => {
    fileInput.click();
});