document.querySelectorAll('.register-login-href').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault(); // ❌ This stops the page from opening the new URL!
    });
});

function loadAndPlay(videoId, title) {
            const playerContainer = document.getElementById('player-container');
            const videoPlayer = document.getElementById('video-player');
            const nowPlaying = document.getElementById('now-playing');
            const loadingMsg = document.getElementById('loading-msg');

            loadingMsg.style.display = 'block';
            nowPlaying.innerText = 'Extracting ad-free stream: ' + title;
            playerContainer.style.display = 'block';
            playerContainer.scrollIntoView({ behavior: 'smooth' });

            // Fetch direct stream URL from Python backend
            fetch('/search/get_stream/?id=' + videoId)
                .then(res => res.json())
                .then(data => {
                    loadingMsg.style.display = 'none';
                    if (data.stream_url) {
                        nowPlaying.innerText = '▶ Playing: ' + title;
                        videoPlayer.src = data.stream_url;
                        videoPlayer.play();
                    } else {
                        alert('Error: Could not extract stream URL.');
                    }
                })
                .catch(err => {
                    loadingMsg.style.display = 'none';
                    alert('Error connecting to backend server.');
                });
        }