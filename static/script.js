async function searchMentions() {
    const term = document.getElementById('searchTerm').value.trim();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Loading...';

    if (!term) {
        resultsDiv.innerHTML = '<p style="color:red;">Please enter a search term.</p>';
        return;
    }

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({search_term: term})
        });

        const data = await response.json();

        if (response.ok) {
            resultsDiv.innerHTML = `
                <h3>Results for "${term}" (last 7 days)</h3>
                <p><strong>Total Mentions:</strong> ${data.mentions_count}</p>
                <p><strong>Posts:</strong> ${data.posts_count}</p>
                <p><strong>Comments:</strong> ${data.comments_count}</p>

                <h4>Sample Posts</h4>
                <ul>
                    ${data.posts.map(p => `<li><a href="${p.url}" target="_blank">${p.title}</a> (Score: ${p.score})</li>`).join('')}
                </ul>

                <h4>Sample Comments</h4>
                <ul>
                    ${data.comments.map(c => `<li>${c.body.substring(0, 100)}... (Score: ${c.score})</li>`).join('')}
                </ul>
            `;
        } else {
            resultsDiv.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`;
        }
    } catch (err) {
        resultsDiv.innerHTML = `<p style="color:red;">Request failed: ${err.message}</p>`;
    }
}
