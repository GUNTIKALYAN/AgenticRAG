/**
 * app.js — RAG Assistant
 * Orchestrates chat, file uploads, history, and UI.
 * Depends on: ui.js, api.js (chat page), ui.js (home page)
 */
let isUploading = false;

(function () {
  'use strict';

  /* ---- Shared: render history on every page ---- */
  document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const activeId = params.get('cid') || null;
    UI.renderHistory(activeId);

    // Detect which page we're on
    const isChatPage = !!document.getElementById('messages-area');

    if (isChatPage) {
      initChatPage(activeId);
    }
    // Home page send logic is inline in index.html for simplicity
  });

  /* 
     CHAT PAGE
   */

  let conversationId = null;
  let conversationMessages = []; // { role, content }
  let uploadedFiles = []; // filenames confirmed by backend

  async function initChatPage(cid) {
    conversationId = cid || UI.generateId();

    // Restore prior conversation from sessionStorage if exists
    const storedConvo = sessionStorage.getItem('convo_' + conversationId);
    // try {
    //   // await Api.resetSession();
    //   console.log("Session reset");
    // } catch (err) {
    //   console.error("Reset failed", err);
    // }
    if (storedConvo) {
      try {
        const { title, messages, files } = JSON.parse(storedConvo);
        uploadedFiles = files || [];
        conversationMessages = messages || [];
        if (title) document.getElementById('chat-title').textContent = title;
        UI.renderFileBadges(uploadedFiles);
        conversationMessages.forEach(m => UI.appendMessage(m.role, m.content));
      } catch (e) { /* ignore */ }
    }

    // Handle pending query from home page
    const pending = sessionStorage.getItem('pendingQuery');
    if (pending) {
      sessionStorage.removeItem('pendingQuery');
      document.getElementById('chat-input').value = pending;
      submitQuery();
    }

    // Send button
    document.getElementById('send-btn').addEventListener('click', submitQuery);

    // Enter key
    document.getElementById('chat-input').addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitQuery();
      }
    });

    // Auto-resize textarea
    document.getElementById('chat-input').addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 160) + 'px';
    });

    // Top-bar file upload
    document.getElementById('file-upload-chat').addEventListener('change', function () {
      handleFileUpload(this.files);
      this.value = '';
    });

    // Inline attach
    document.getElementById('file-attach-inline').addEventListener('change', function () {
      handleFileUpload(this.files);
      this.value = '';
    });
  }

  /* ---- File Upload ---- */
  async function handleFileUpload(files) {
    if (!files || !files.length) return;
    isUploading = true;
    UI.showToast(`Uploading ${files.length} file(s)…`, 'info', 2500);

    try {
      const result = await Api.uploadFiles(files);
      const names = result.filenames || result.files || [];
      uploadedFiles = [...new Set([...uploadedFiles, ...names])];
      UI.renderFileBadges(uploadedFiles);
      UI.showToast(`✓ Uploaded: ${names.join(', ')}`, 'success');
      saveConversation();
    } catch (err) {
      UI.showToast('Upload failed: ' + err.message, 'error');
    } finally{
      isUploading = false;
    }
  }

  /* ---- Submit Query ---- */
  async function submitQuery() {
    if (isUploading) {
      UI.showToast("⏳ Please wait, file is still processing...", "info");
      return;
    }
    const input = document.getElementById('chat-input');
    const query = input.value.trim();
    if (!query) return;

    input.value = '';
    input.style.height = 'auto';

    // Append user message
    UI.appendMessage('user', query);
    conversationMessages.push({ role: 'user', content: query });

    // Set title from first message
    if (conversationMessages.length === 1) {
      const title = query.length > 50 ? query.slice(0, 47) + '…' : query;
      document.getElementById('chat-title').textContent = title;
      UI.saveHistoryItem(conversationId, title);
      UI.renderHistory(conversationId);
    }

    // Disable input
    const sendBtn = document.getElementById('send-btn');
    if (isUploading) {
      UI.showToast("Wait for upload to finish", "info");
      return;
    }
    sendBtn.disabled = true;

    // Show typing
    UI.showTyping();

    try {
      const result = await Api.sendQuery(query);
      UI.removeTyping();

      const answer = result.answer || result.response || 'No answer returned.';
      const sources = result.sources || result.source_documents || [];

      UI.appendMessage('assistant', answer, sources);
      conversationMessages.push({ role: 'assistant', content: answer });
      saveConversation();

    } catch (err) {
      UI.removeTyping();
      UI.appendMessage('assistant', '⚠ Error: ' + err.message);
      UI.showToast('Request failed: ' + err.message, 'error');
    } finally {
      sendBtn.disabled = false;
      input.focus();
    }
  }

  /* ---- Persist Conversation ---- */
  function saveConversation() {
    const title = document.getElementById('chat-title')?.textContent || 'Conversation';
    sessionStorage.setItem('convo_' + conversationId, JSON.stringify({
      title,
      messages: conversationMessages,
      files: uploadedFiles,
    }));
  }

})();