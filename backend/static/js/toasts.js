document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll(".toast.auto-remove");
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.remove();
        }, 5000);
    });
});

function removeToast(element) {
    element.classList.add('fast:fade-out');
    setTimeout(() => {
        element.remove();
    }, 300);
}
