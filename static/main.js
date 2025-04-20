async function fetchPosts() {
    const res = await fetch('/api/posts');
    const posts = await res.json();
    const postsDiv = document.getElementById('posts');
    postsDiv.innerHTML = '';
    posts.forEach(post => {
        const div = document.createElement('div');
        div.className = 'post';
        div.innerHTML = `<span class="text">${escapeHTML(post.text)}</span><span class="timestamp">${formatTime(post.timestamp)}</span>`;
        postsDiv.appendChild(div);
    });
}

function escapeHTML(str) {
    return str.replace(/[&<>]/g, tag => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[tag]));
}

function formatTime(ts) {
    const d = new Date(ts);
    return d.toLocaleString('nl-NL', { hour12: false });
}

document.getElementById('postForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('text').value;
    if (!text.trim()) return;
    await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    document.getElementById('text').value = '';
    fetchPosts();
});

// COUNTDOWN TO KINGS DAY
const kingsday = new Date('2025-04-26T00:00:00+02:00');
const countdownDiv = document.getElementById('countdown');
const progressBar = document.getElementById('progress-bar');
const progressBarBg = document.getElementById('progress-bar-bg');
const startDate = new Date('2025-04-21T00:00:00+02:00'); // now

function updateCountdown() {
    const now = new Date();
    const diff = kingsday - now;
    if (diff <= 0) {
        countdownDiv.textContent = "Het is Koningsdag! ";
        progressBar.style.width = '100%';
        return;
    }
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);
    const seconds = Math.floor((diff / 1000) % 60);
    countdownDiv.textContent = `Nog ${days} dagen, ${hours} uur, ${minutes} min, ${seconds} sec tot Koningsdag!`;
    // Progress bar
    const total = kingsday - startDate;
    const elapsed = now - startDate;
    let percent = Math.max(0, Math.min(100, (elapsed / total) * 100));
    progressBar.style.width = percent + '%';
}
if (countdownDiv && progressBar) {
    updateCountdown();
    setInterval(updateCountdown, 1000);
}

window.onload = () => {
    fetchPosts();
    setInterval(fetchPosts, 2000); // Poll every 2 seconds for new posts
};
