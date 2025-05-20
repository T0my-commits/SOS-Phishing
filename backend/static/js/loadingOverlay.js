// Function to show the loading overlay
function showLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'flex';  // Show overlay with spinner
}

// Optional: Hide the overlay after some time for demo purposes
setTimeout(() => {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'none';  // Hide overlay after delay
}, 5000);
