document.getElementById('downloadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const urlInput = document.getElementById('urlInput').value;
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const submitBtn = this.querySelector('button[type="submit"]');
    const resultCard = document.getElementById('resultCard');
    const statusMessage = document.getElementById('statusMessage');

    // Reset state
    resultCard.style.display = 'none';
    statusMessage.textContent = '';
    statusMessage.className = 'text-center mt-3 text-info';
    
    // UI Loading state
    btnText.textContent = 'Đang xử lý...';
    btnLoader.classList.remove('d-none');
    submitBtn.disabled = true;
    statusMessage.textContent = 'Đang lấy thông tin video và chuyển đổi... Vui lòng đợi!';

    try {
        const response = await fetch('/api/download/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ url: urlInput })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // Success
            statusMessage.textContent = 'Thành công!';
            statusMessage.className = 'text-center mt-3 text-success';
            
            // Populate Result
            document.getElementById('thumbImg').src = data.thumbnail;
            document.getElementById('videoTitle').textContent = data.title;
            document.getElementById('videoDuration').textContent = data.duration;
            document.getElementById('downloadLink').href = data.download_url;
            
            resultCard.style.display = 'block';
        } else {
            // Error from API
            throw new Error(data.error || 'Có lỗi xảy ra.');
        }

    } catch (error) {
        console.error('Error:', error);
        statusMessage.textContent = 'Lỗi: ' + error.message;
        statusMessage.className = 'text-center mt-3 text-danger';
    } finally {
        // Reset Button
        btnText.innerHTML = 'Tải xuống ngay <i class="fas fa-download ms-2"></i>';
        btnLoader.classList.add('d-none');
        submitBtn.disabled = false;
    }
});

// Helper to get CSRF token (Django default)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
