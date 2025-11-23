// Video Player JavaScript with Custom Controls

document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('video-player');
    const unmuteNotice = document.getElementById('unmute-notice');
    const playBtn = document.getElementById('play-btn');
    const backwardBtn = document.getElementById('backward-btn');
    const forwardBtn = document.getElementById('forward-btn');
    const volumeBtn = document.getElementById('volume-btn');
    const volumeSlider = document.getElementById('volume-slider');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const progressBar = document.getElementById('progress-bar');
    const progressFilled = document.getElementById('progress-filled');
    const currentTimeEl = document.getElementById('current-time');
    const totalTimeEl = document.getElementById('total-time');
    
    // Unmute on first user interaction
    let hasInteracted = false;
    function handleFirstInteraction() {
        if (!hasInteracted && video.muted) {
            hasInteracted = true;
            video.muted = false;
            if (unmuteNotice) {
                unmuteNotice.style.display = 'none';
            }
            updateVolumeButton();
        }
    }
    
    // Click unmute notice to unmute
    if (unmuteNotice) {
        unmuteNotice.addEventListener('click', function() {
            video.muted = false;
            unmuteNotice.style.display = 'none';
            updateVolumeButton();
            hasInteracted = true;
        });
    }
    
    // Hide notice when video is unmuted
    video.addEventListener('volumechange', function() {
        if (!video.muted && unmuteNotice) {
            unmuteNotice.style.display = 'none';
        }
        updateVolumeButton();
    });
    
    // Play/Pause button
    playBtn.addEventListener('click', function() {
        handleFirstInteraction();
        togglePlayPause();
    });
    
    // Backward 2 seconds button
    backwardBtn.addEventListener('click', function() {
        handleFirstInteraction();
        video.currentTime = Math.max(0, video.currentTime - 2);
        showSeekNotification('-2s');
    });
    
    // Forward 2 seconds button
    forwardBtn.addEventListener('click', function() {
        handleFirstInteraction();
        video.currentTime = Math.min(video.duration, video.currentTime + 2);
        showSeekNotification('+2s');
    });
    
    // Volume button
    volumeBtn.addEventListener('click', function() {
        video.muted = !video.muted;
        updateVolumeButton();
        if (unmuteNotice) {
            unmuteNotice.style.display = video.muted ? 'flex' : 'none';
        }
        hasInteracted = true;
    });
    
    // Volume slider
    volumeSlider.addEventListener('input', function() {
        handleFirstInteraction();
        video.volume = this.value / 100;
        if (this.value > 0) {
            video.muted = false;
        }
        updateVolumeButton();
    });
    
    // Fullscreen button
    fullscreenBtn.addEventListener('click', function() {
        handleFirstInteraction();
        toggleFullscreen();
    });
    
    // Progress bar click
    progressBar.addEventListener('click', function(e) {
        handleFirstInteraction();
        const rect = progressBar.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        video.currentTime = pos * video.duration;
    });
    
    // Update progress bar
    video.addEventListener('timeupdate', function() {
        const percent = (video.currentTime / video.duration) * 100;
        progressFilled.style.width = percent + '%';
        currentTimeEl.textContent = formatTime(video.currentTime);
    });
    
    // Update play button icon
    video.addEventListener('play', function() {
        playBtn.innerHTML = '<i class="fas fa-pause"></i>';
    });
    
    video.addEventListener('pause', function() {
        playBtn.innerHTML = '<i class="fas fa-play"></i>';
    });
    
    // Update duration when loaded
    video.addEventListener('loadedmetadata', function() {
        totalTimeEl.textContent = formatTime(video.duration);
        updateDuration();
        updateResolution();
    });
    
    // Update volume button icon
    function updateVolumeButton() {
        if (video.muted || video.volume === 0) {
            volumeBtn.innerHTML = '<i class="fas fa-volume-mute"></i>';
            volumeSlider.value = 0;
        } else if (video.volume > 0.5) {
            volumeBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
            volumeSlider.value = video.volume * 100;
        } else {
            volumeBtn.innerHTML = '<i class="fas fa-volume-down"></i>';
            volumeSlider.value = video.volume * 100;
        }
    }
    
    // Keyboard shortcuts with 2-second seeking
    document.addEventListener('keydown', function(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }
        
        switch(e.key.toLowerCase()) {
            case ' ':
            case 'k':
                e.preventDefault();
                handleFirstInteraction();
                togglePlayPause();
                break;
            case 'f':
                e.preventDefault();
                handleFirstInteraction();
                toggleFullscreen();
                break;
            case 'arrowleft':
                e.preventDefault();
                handleFirstInteraction();
                // 2 seconds backward (10 seconds with Shift)
                if (e.shiftKey) {
                    video.currentTime = Math.max(0, video.currentTime - 10);
                    showSeekNotification('-10s');
                } else {
                    video.currentTime = Math.max(0, video.currentTime - 2);
                    showSeekNotification('-2s');
                }
                break;
            case 'arrowright':
                e.preventDefault();
                handleFirstInteraction();
                // 2 seconds forward (10 seconds with Shift)
                if (e.shiftKey) {
                    video.currentTime = Math.min(video.duration, video.currentTime + 10);
                    showSeekNotification('+10s');
                } else {
                    video.currentTime = Math.min(video.duration, video.currentTime + 2);
                    showSeekNotification('+2s');
                }
                break;
            case 'arrowup':
                e.preventDefault();
                handleFirstInteraction();
                video.volume = Math.min(1, video.volume + 0.1);
                showVolumeNotification();
                break;
            case 'arrowdown':
                e.preventDefault();
                handleFirstInteraction();
                video.volume = Math.max(0, video.volume - 0.1);
                showVolumeNotification();
                break;
            case 'm':
                e.preventDefault();
                video.muted = !video.muted;
                if (unmuteNotice) {
                    unmuteNotice.style.display = video.muted ? 'flex' : 'none';
                }
                hasInteracted = true;
                break;
            case 'j':
                e.preventDefault();
                handleFirstInteraction();
                video.currentTime = Math.max(0, video.currentTime - 10);
                showSeekNotification('-10s');
                break;
            case 'l':
                e.preventDefault();
                handleFirstInteraction();
                video.currentTime = Math.min(video.duration, video.currentTime + 10);
                showSeekNotification('+10s');
                break;
        }
    });
    
    // Click on video to play/pause
    video.addEventListener('click', function() {
        handleFirstInteraction();
        togglePlayPause();
    });
    
    // Initial setup
    updateVolumeButton();
});

function togglePlayPause() {
    const video = document.getElementById('video-player');
    if (video.paused) {
        video.play();
    } else {
        video.pause();
    }
}

function toggleFullscreen() {
    const playerWrapper = document.querySelector('.player-wrapper');
    
    if (!document.fullscreenElement) {
        if (playerWrapper.requestFullscreen) {
            playerWrapper.requestFullscreen();
        } else if (playerWrapper.webkitRequestFullscreen) {
            playerWrapper.webkitRequestFullscreen();
        } else if (playerWrapper.msRequestFullscreen) {
            playerWrapper.msRequestFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

function updateDuration() {
    const video = document.getElementById('video-player');
    const durationText = document.getElementById('duration-text');
    
    if (durationText && video.duration && !isNaN(video.duration)) {
        const duration = formatTime(video.duration);
        durationText.textContent = duration;
    }
}

function updateResolution() {
    const video = document.getElementById('video-player');
    const resolutionText = document.getElementById('resolution-text');
    
    if (resolutionText) {
        if (video.videoWidth && video.videoHeight) {
            resolutionText.textContent = `${video.videoWidth} x ${video.videoHeight}`;
        } else {
            resolutionText.textContent = 'Unknown';
        }
    }
}

function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}:${pad(minutes)}:${pad(secs)}`;
    } else {
        return `${minutes}:${pad(secs)}`;
    }
}

function pad(num) {
    return num.toString().padStart(2, '0');
}

// Show seek notification
function showSeekNotification(text) {
    removeExistingNotifications();
    
    const notification = document.createElement('div');
    notification.className = 'seek-notification';
    notification.textContent = text;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 800);
}

// Show volume notification
function showVolumeNotification() {
    removeExistingNotifications();
    
    const video = document.getElementById('video-player');
    const notification = document.createElement('div');
    notification.className = 'volume-notification';
    
    const volumePercent = Math.round(video.volume * 100);
    const volumeIcon = video.muted ? '<i class="fas fa-volume-mute"></i>' : 
                       volumePercent > 50 ? '<i class="fas fa-volume-up"></i>' :
                       volumePercent > 0 ? '<i class="fas fa-volume-down"></i>' :
                       '<i class="fas fa-volume-off"></i>';
    
    notification.innerHTML = `
        ${volumeIcon}
        <div class="volume-bar">
            <div class="volume-fill" style="width: ${volumePercent}%"></div>
        </div>
        <span>${volumePercent}%</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 1000);
}

function removeExistingNotifications() {
    const existing = document.querySelectorAll('.seek-notification, .volume-notification');
    existing.forEach(el => el.remove());
}
