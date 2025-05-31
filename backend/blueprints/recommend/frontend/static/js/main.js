const recommendedVideoCCIDs = {{ recommended_video_ccids | tojson }};

function generateVideoLinks() {
    const videoContainer = document.getElementById('video-container');
    recommendedVideoCCIDs.forEach((ccid) => {
        const videoLink = document.createElement('a');
        videoLink.href = `https://www.xuetangx.com/api/v1/lms/service/playurl/${ccid}/?appid=10000`;
        videoLink.textContent = `观看视频 ${ccid}`;
        videoLink.target = '_blank';
        videoContainer.appendChild(videoLink);
        videoContainer.appendChild(document.createElement('br'));
    });
}

document.addEventListener('DOMContentLoaded', generateVideoLinks);