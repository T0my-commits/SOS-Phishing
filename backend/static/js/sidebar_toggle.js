// Toggle sidebar
document.querySelector('.burger-btn-sidebar').addEventListener('click', function() {
    // toggle sidebar
    document.querySelector('.sidebar').classList.toggle('sidebar-active');

    // toggle main container
    document.querySelector('#main-container').classList.toggle('main-container-full');
});
