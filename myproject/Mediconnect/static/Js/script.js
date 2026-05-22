
    // <!-- Reviews Slider Script -->
        const slider = document.getElementById('reviews-slider');
        let scrollAmount = 0;
        const cardWidth = 318;  
        const totalCards = slider.children.length;

        function autoSlide() {
            scrollAmount += cardWidth;
            if (scrollAmount >= cardWidth * totalCards) {
                scrollAmount = 0; 
            }
            slider.style.transform = `translateX(-${scrollAmount}px)`;
        }

        setInterval(autoSlide, 3000); 