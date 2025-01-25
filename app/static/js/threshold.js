async function uploadImage(event) {
    const file = event.target.files[0];

    if (!file) {
        return;
    }

    document.getElementById('feedback-message').innerText = 'Carregando...';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('feedback-message').innerText = result.success || 'Upload realizado com sucesso!';
        } else {
            document.getElementById('feedback-message').innerText = result.error || 'Erro no upload.';
        }
    } catch (error) {
        console.error('Erro ao enviar a imagem:', error);
        document.getElementById('feedback-message').innerText = 'Erro ao enviar a imagem.';
    }
}
