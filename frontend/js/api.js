const API_BASE = '/api';

const Api = (() => {

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

    if (data.status === "error") {
      throw new Error(data.message);
    }

    return {
      filenames: data.files || [],
      message: data.status || 'Upload successful'
    };
  }

  async function sendQuery(query) {
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

  async function newChat() {
    const res = await fetch(`${API_BASE}/new-chat`, {
      method: "POST"
    });

    if (!res.ok) {
      throw new Error("Failed to reset session");
    }

    return res.json();
  }

  return { uploadFiles, sendQuery, newChat };

})();