// Main JavaScript for Video Library Page

document.addEventListener('DOMContentLoaded', function() {
    loadVideos();
});

async function loadVideos() {
    const videoGrid = document.getElementById('video-grid');
    const videoCount = document.getElementById('video-count');
    const noVideos = document.getElementById('no-videos');

    try {
        const response = await fetch('/api/videos');
        const data = await response.json();

        if (data.success && data.videos.length > 0) {
            // Update count
            videoCount.textContent = `${data.count} video${data.count !== 1 ? 's' : ''}`;

            // Clear loading message
            videoGrid.innerHTML = '';

            // Create video cards
            data.videos.forEach((video, index) => {
                const card = createVideoCard(video, index);
                videoGrid.appendChild(card);
            });
        } else {
            // No videos found
            videoGrid.style.display = 'none';
            noVideos.style.display = 'block';
            videoCount.textContent = '0 videos';
        }
    } catch (error) {
        console.error('Error loading videos:', error);
        videoGrid.innerHTML = `
            <div class="loading">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Error loading videos. Please refresh the page.</p>
            </div>
        `;
    }
}

function createVideoCard(video, index) {
    const card = document.createElement('div');
    card.className = 'video-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    // Generate random gradient for thumbnail
    const gradients = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
        'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
    ];
    
    const gradient = gradients[index % gradients.length];
    
    card.innerHTML = `
        <div class="video-thumbnail" style="background: ${gradient};">
            <i class="fas fa-play-circle"></i>
        </div>
        <div class="video-details">
            <h3 class="video-title" title="${video.name}">${video.name}</h3>
            <div class="video-meta">
                <span class="meta-item">
                    <i class="fas fa-file-video"></i>
                    ${video.extension}
                </span>
                <span class="meta-item">
                    <i class="fas fa-hdd"></i>
                    ${video.size_mb} MB
                </span>
            </div>
        </div>
    `;
    
    // Add click event to play video
    card.addEventListener('click', () => {
        window.location.href = `/watch/${encodeURIComponent(video.filename)}`;
    });
    
    return card;
}

// Search functionality (future enhancement)
function searchVideos(query) {
    const cards = document.querySelectorAll('.video-card');
    const searchLower = query.toLowerCase();
    
    cards.forEach(card => {
        const title = card.querySelector('.video-title').textContent.toLowerCase();
        if (title.includes(searchLower)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
