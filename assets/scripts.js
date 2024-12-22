async function startDownload() {
    const url = document.getElementById('youtubeUrl').value;
    const format = document.getElementById('format').value;

    if (!url) {
        alert("Please paste a YouTube URL!");
        return;
    }

    try {
        const response = await fetch('https://your-backend-service.onrender.com/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url, format })
        });

        if (!response.ok) {
            throw new Error('Download failed');
        }

        const data = await response.json();
        window.location.href = data.file_url;
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}
