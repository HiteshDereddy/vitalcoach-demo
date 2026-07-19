// Fetch AI Output JSON dynamically from the backend script output
document.addEventListener('DOMContentLoaded', () => {
    fetch('ai_output.json')
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to load ai_output.json");
            }
            return response.json();
        })
        .then(data => renderData(data))
        .catch(err => {
            console.error(err);
            document.getElementById('weekly-summary').innerHTML = `
                <div style="color: var(--danger);">
                    <i class="fa-solid fa-triangle-exclamation"></i> 
                    Could not load <strong>ai_output.json</strong>. <br>
                    Make sure you ran the backend script first to generate the file!
                </div>
            `;
            document.getElementById('engagement-level').style.display = 'none';
        });
});

function renderData(data) {
    // 1. Weekly Summary
    document.getElementById('weekly-summary').innerText = data.client_summary.weekly_overview;
    document.getElementById('engagement-level').innerText = data.client_summary.engagement_level + " Engagement";

    // 2. Metrics
    const metricsContainer = document.getElementById('metrics-container');
    metricsContainer.innerHTML = '';
    for (const [key, value] of Object.entries(data.metrics || {})) {
        metricsContainer.innerHTML += createItemHTML(key, value);
    }

    // 3. Health & Symptoms
    const healthContainer = document.getElementById('health-container');
    healthContainer.innerHTML = '';
    for (const [key, value] of Object.entries(data.health_status || {})) {
        healthContainer.innerHTML += createItemHTML(key, value);
    }

    // 4. Coaching Insights (Lists)
    const riskFlags = document.getElementById('risk-flags');
    riskFlags.innerHTML = '';
    if (data.coaching_insights && data.coaching_insights.risk_attention_flags) {
        data.coaching_insights.risk_attention_flags.forEach(item => {
            riskFlags.innerHTML += `<li>${createItemHTML('', item, true)}</li>`;
        });
    }

    const keyBarriers = document.getElementById('key-barriers');
    keyBarriers.innerHTML = '';
    if (data.coaching_insights && data.coaching_insights.key_barriers) {
        data.coaching_insights.key_barriers.forEach(item => {
            keyBarriers.innerHTML += `<li>${createItemHTML('', item, true)}</li>`;
        });
    }

    const pendingActions = document.getElementById('pending-actions');
    pendingActions.innerHTML = '';
    if (data.coaching_insights && data.coaching_insights.pending_actions) {
        data.coaching_insights.pending_actions.forEach(item => {
            pendingActions.innerHTML += `<li>${createItemHTML('', item, true)}</li>`;
        });
    }

    // 5. Recommended Next Action
    if (data.coaching_insights && data.coaching_insights.recommended_next_action) {
        const nextActionData = data.coaching_insights.recommended_next_action;
        document.getElementById('next-action').innerHTML = `
            <div style="margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                <strong>${nextActionData.status}</strong>
                <span class="source-badge badge-${nextActionData.source_type}" style="font-size: 0.6rem;">${formatSourceType(nextActionData.source_type)}</span>
            </div>
            <p style="font-size: 0.9rem; margin-bottom: 1rem; font-weight: normal; color: var(--text-primary);">${nextActionData.details}</p>
            <div style="font-size: 0.8rem; font-style: italic; color: var(--text-secondary); border-left: 2px solid var(--accent-primary); padding-left: 0.5rem;">
                Evidence: "${nextActionData.evidence}"
            </div>
        `;
    }

    // Global Approve All Button
    document.getElementById('approve-all').addEventListener('click', () => {
        document.querySelectorAll('.metric-item, .recommendation-card').forEach(el => {
            el.classList.remove('item-rejected');
            el.classList.add('item-approved');
        });
    });
}

// Helper to format source type for display
function formatSourceType(source) {
    if (!source) return 'Unknown';
    return source.replace(/_/g, ' ');
}

// Generate Review Buttons HTML
function getReviewButtonsHTML() {
    return `
        <div class="review-actions">
            <button class="btn-review approve" onclick="handleReview(this, 'approve')"><i class="fa-solid fa-check"></i> Approve</button>
            <button class="btn-review edit" onclick="handleReview(this, 'edit')"><i class="fa-solid fa-pen"></i> Edit</button>
            <button class="btn-review reject" onclick="handleReview(this, 'reject')"><i class="fa-solid fa-xmark"></i> Reject</button>
        </div>
    `;
}

// Generate HTML for an Item (Metric or Insight)
function createItemHTML(key, data, isList = false) {
    const formattedKey = key ? key.replace(/_/g, ' ') : '';
    
    return `
        <div class="metric-item">
            <div class="metric-header">
                ${!isList ? `<span class="metric-title">${formattedKey}</span>` : `<span class="metric-title">${data.status}</span>`}
                <span class="source-badge badge-${data.source_type}">${formatSourceType(data.source_type)}</span>
            </div>
            <div class="metric-value">
                ${isList ? data.details : `<strong>${data.status}:</strong> ${data.details}`}
            </div>
            <button class="evidence-btn" onclick="toggleEvidence(this)">
                <i class="fa-solid fa-quote-left"></i> Show Evidence
            </button>
            <div class="evidence-content">
                "${data.evidence}"
            </div>
            ${getReviewButtonsHTML()}
        </div>
    `;
}

// Toggle Evidence Function
window.toggleEvidence = function(btn) {
    const content = btn.nextElementSibling;
    if (content.classList.contains('show')) {
        content.classList.remove('show');
        btn.innerHTML = '<i class="fa-solid fa-quote-left"></i> Show Evidence';
    } else {
        content.classList.add('show');
        btn.innerHTML = '<i class="fa-solid fa-chevron-up"></i> Hide Evidence';
    }
}

// Handle Review Actions (Approve, Edit, Reject)
window.handleReview = function(btn, action) {
    const item = btn.closest('.metric-item') || btn.closest('.recommendation-card');
    
    if (action === 'approve') {
        item.classList.remove('item-rejected');
        item.classList.add('item-approved');
    } else if (action === 'reject') {
        item.classList.remove('item-approved');
        item.classList.add('item-rejected');
    } else if (action === 'edit') {
        alert("Edit modal would open here to allow the coach to modify the AI's extraction.");
    }
}
