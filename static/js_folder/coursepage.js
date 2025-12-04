document.addEventListener('DOMContentLoaded', function() {

    // Rating Stars
    const ratingElements = document.querySelectorAll('.rating-stars');
    ratingElements.forEach(el => {
        const rating = parseFloat(el.dataset.rating);
        const stars = el.querySelectorAll('i');
        stars.forEach((star, index) => {
            if (index < Math.floor(rating)) {
                star.classList.add('filled');
            }
        });
    });

    // Curriculum toggle
    const lessonsContainer = document.querySelector('.lessons-container');

    const lessonHeaders = document.querySelectorAll('.lesson-header');

    lessonHeaders.forEach(header => {
        header.addEventListener('click', function() {
            if (lessonsContainer.classList.contains('locked')) {
                alert("Enroll in the course to unlock the lessons!");
                return;
            }
            const lessonItem = this.closest('.lesson-item');
            lessonItem.classList.toggle('active');
        });
    });

});
