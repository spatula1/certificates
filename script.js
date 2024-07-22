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
});