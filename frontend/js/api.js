/**
 * api.js — RAG Assistant
 * Handles all communication with the FastAPI backend.
 */

const API_BASE = 'api'; // adjust to your FastAPI host/port

const Api = (() => {

  /**
   * Upload one or more files (PDF / TXT) to the backend.
   * @param {FileList|File[]} files
   * @returns {Promise<{ filenames: string[], message: string }>}
   */
  async function uploadFiles(files) {
    const form = new FormData();
    for (const file of files) {
      form.append('files', file);
    }
    const res = await fetch(`${API_BASE}/ingest`, {
      method: 'POST',
      body: form,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Upload failed (${res.status})`);
    }
    const data = await res.json();

    // Normalize response for frontend
    return {
        filenames: data.files || data.filenames || [],
        message: data.status || 'Upload successful'
    };
  }
  
  /**
   * Send a chat query to the RAG backend.
   * @param {string} query
   * @param {string[]} [filenames]  optional list of already-uploaded filenames to scope
   * @returns {Promise<{ answer: string, sources: string[] }>}
   */
  async function sendQuery(query, filenames = []) {
    const res = await fetch(`${API_BASE}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Query failed (${res.status})`);
    }
    return res.json();
  }
  async function resetSession() {
    const res = await fetch(`${API_BASE}/reset`, {
      method: 'POST'
    });

    if (!res.ok) {
      throw new Error("Failed to reset session");
    }

    return res.json();
  }
  return { uploadFiles, sendQuery, resetSession };
})();