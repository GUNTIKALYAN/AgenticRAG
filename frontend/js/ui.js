/**
 * ui.js — RAG Assistant
 * Pure DOM / UI helpers. No API calls here.
 */

const UI = (() => {

  /* ---- Toast ---- */
  function showToast(msg, type = 'info', duration = 3000) {
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; t.style.transition = 'opacity 0.3s'; }, duration - 300);
    setTimeout(() => t.remove(), duration);
  }

  /* ---- History (localStorage) ---- */
  const HISTORY_KEY = 'rag_history';

  function getHistory() {
    try { return JSON.parse(localStorage.getItem(HISTORY_KEY)) || []; }
    catch { return []; }
  }

  function saveHistoryItem(id, title) {
    const history = getHistory();
    const exists = history.find(h => h.id === id);
    if (!exists) {
      history.unshift({ id, title, ts: Date.now() });
      if (history.length > 40) history.pop();
      localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    }
  }

 
  function renderHistory(activeId = null) {
    const list = document.getElementById('history-list');
    list.innerHTML = '';

    const keys = Object.keys(sessionStorage)
      .filter(k => k.startsWith('convo_'))
      .sort()
      .reverse();

    if (keys.length === 0) {
      list.innerHTML = '<div class="history-empty">No conversations yet</div>';
      return;
    }

    keys.forEach(key => {
      const data = JSON.parse(sessionStorage.getItem(key));
      const id = key.replace('convo_', '');
      const title = data.title || 'Conversation';

      const item = document.createElement('div');
      item.className = 'history-item' + (id === activeId ? ' active' : '');

      item.innerHTML = `
        <div class="history-item-text">${title}</div>
        <div class="history-actions">
          <span class="delete-btn" data-id="${id}">🗑</span>
        </div>
      `;

      // open chat
      item.onclick = (e) => {
        if (e.target.classList.contains('delete-btn')) return;
        window.location.href = 'chat.html?cid=' + id;
      };

      // delete chat
      item.querySelector('.delete-btn').onclick = (e) => {
        e.stopPropagation();

        if (!confirm('Delete this conversation?')) return;

        sessionStorage.removeItem('convo_' + id);

        renderHistory(activeId);
      };

      list.appendChild(item);
    });
  }
  function loadConversation(id) {
    // Navigate to chat with this conversation id
    window.location.href = `chat.html?cid=${encodeURIComponent(id)}`;
  }

  /* ---- Messages ---- */
  function appendMessage(role, text, sources = []) {
    const area = document.getElementById('messages-inner');
    if (!area) return;

    const div = document.createElement('div');
    div.className = `message ${role}`;

    const roleLabel = document.createElement('div');
    roleLabel.className = 'msg-role';
    roleLabel.textContent = role === 'user' ? 'You' : 'Assistant';

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.innerHTML = formatText(text);

    div.appendChild(roleLabel);
    div.appendChild(bubble);

    if (sources && sources.length && role === 'assistant') {
      const src = document.createElement('div');
      src.className = 'msg-sources';
      sources.forEach(s => {
        const chip = document.createElement('span');
        chip.className = 'source-chip';
        chip.textContent = '📄 ' + s;
        src.appendChild(chip);
      });
      div.appendChild(src);
    }

    area.appendChild(div);
    scrollToBottom();
    return div;
  }

  function showTyping() {
    const area = document.getElementById('messages-inner');
    if (!area) return null;
    const div = document.createElement('div');
    div.className = 'message assistant';
    div.id = 'typing-indicator';
    div.innerHTML = `
      <div class="msg-role">Assistant</div>
      <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>`;
    area.appendChild(div);
    scrollToBottom();
    return div;
  }

  function removeTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
  }

  function scrollToBottom() {
    const area = document.getElementById('messages-area');
    if (area) area.scrollTop = area.scrollHeight;
  }

  /* ---- File badges ---- */
  function renderFileBadges(filenames) {
    const area = document.getElementById('file-badge-area');
    if (!area) return;
    area.innerHTML = filenames.map(f => `
      <span class="file-badge">
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        ${escapeHtml(f)}
      </span>`).join('');
  }

  /* ---- Utilities ---- */
  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatText(text) {
    // Basic markdown: bold, code, newlines
    return escapeHtml(text)
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/`(.+?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br/>');
  }

  function relativeTime(ts) {
    const diff = Date.now() - ts;
    if (diff < 60000) return 'now';
    if (diff < 3600000) return Math.floor(diff / 60000) + 'm';
    if (diff < 86400000) return Math.floor(diff / 3600000) + 'h';
    return Math.floor(diff / 86400000) + 'd';
  }

  function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  }

  return {
    showToast,
    getHistory,
    saveHistoryItem,
    renderHistory,
    loadConversation,
    appendMessage,
    showTyping,
    removeTyping,
    scrollToBottom,
    renderFileBadges,
    generateId,
    escapeHtml,
  };
})();