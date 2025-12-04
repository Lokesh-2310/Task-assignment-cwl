// Flip card on click (for better mobile experience; hover works on desktop)
document.querySelectorAll('.flip-card').forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('flipped');
    });
});

// Close flip on outside click (optional enhancement)
document.addEventListener('click', (e) => {
    if (!e.target.closest('.flip-card')) {
        document.querySelectorAll('.flip-card').forEach(card => {
            card.classList.remove('flipped');
        });
    }
});
