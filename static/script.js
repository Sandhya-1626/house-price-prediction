document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result');
    const priceDisplay = document.getElementById('price-display');
    const resetBtn = document.getElementById('reset-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const area = document.getElementById('area').value;
        const bedrooms = document.getElementById('bedrooms').value;
        const bathrooms = document.getElementById('bathrooms').value;

        // Simple validation visualization
        const button = form.querySelector('button');
        const originalText = button.querySelector('span').innerText;
        button.querySelector('span').innerText = 'Calculating...';
        button.disabled = true;

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ area, bedrooms, bathrooms }),
            });

            const data = await response.json();

            if (response.ok) {
                // Determine currency formatting (assuming generic or USD for now, but INR is likely based on user data location, I'll use generic with commas)
                const formattedPrice = new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD',
                    maximumFractionDigits: 0
                }).format(data.price);
                
                priceDisplay.innerText = formattedPrice;
                
                // Hide form, show result
                form.style.display = 'none';
                resultContainer.classList.remove('hidden');
                // Trigger reflow
                void resultContainer.offsetWidth; 
                resultContainer.classList.add('show');
            } else {
                alert('Error: ' + (data.error || 'Something went wrong'));
            }
        } catch (error) {
            alert('Error connecting to server. Make sure it is running.');
            console.error(error);
        } finally {
            button.querySelector('span').innerText = originalText;
            button.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        resultContainer.classList.remove('show');
        setTimeout(() => {
            resultContainer.classList.add('hidden');
            form.style.display = 'block';
            form.reset();
        }, 300);
    });
});
