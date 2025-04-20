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

window.onload = fetchPosts;
