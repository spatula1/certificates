document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('badgesButton')?.addEventListener('click', function() {
    window.location.href = '/badges';
    });

    document.getElementById('certificatesButton')?.addEventListener('click', function() {
        window.location.href = '/certificates';
    });

    document.getElementById('progressReportsButton')?.addEventListener('click', function() {
        window.location.href = '/progress-reports';
    });

    document.getElementById('returnHomeButton')?.addEventListener('click', function() {
        window.location.href = '/';
    });

    document.getElementById('certificate-mini').addEventListener('submit', function(event) {
        event.preventDefault();
        handleFormSubmission(this, '/upload-mini-class');
    });

    document.getElementById('certificate-full').addEventListener('submit', function(event) {
        event.preventDefault();
        handleFormSubmission(this, '/upload-full-class');
    });

    document.getElementById('certificate-both').addEventListener('submit', function(event) {
        event.preventDefault();
        handleFormSubmission(this, '/upload-both-classes');
    });
});

function handleFormSubmission(form, url) {
    const formData = new FormData(form);

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            const downloadLink = document.getElementById('download-link');
            const downloadUrl = document.getElementById('download-url');
            downloadUrl.href = data.download_url;
            downloadLink.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
