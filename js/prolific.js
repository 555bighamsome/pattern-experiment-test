// Prolific ID page logic
// Stores PID in localStorage as `prolificId`, then continues to consent.

document.addEventListener('DOMContentLoaded', () => {
  const prolificInput = document.getElementById('prolific-id');
  const continueBtn = document.getElementById('prolific-continue');
  const errorEl = document.getElementById('prolific-error');

  function setError(message) {
    if (!errorEl) return;
    if (!message) {
      errorEl.style.display = 'none';
      errorEl.textContent = '';
    } else {
      errorEl.style.display = 'block';
      errorEl.textContent = message;
    }
  }

  // Pre-fill if previously stored
  const existing = localStorage.getItem('prolificId');
  if (existing && prolificInput) {
    prolificInput.value = existing;
  }

  // User request: allow empty Prolific ID and still continue.
  continueBtn?.addEventListener('click', () => {
    const raw = prolificInput?.value ?? '';
    const trimmed = raw.trim();

    // Store null-ish when empty, so downstream payload becomes null.
    if (trimmed.length === 0) {
      localStorage.removeItem('prolificId');
      setError('');
    } else {
      localStorage.setItem('prolificId', trimmed);
      setError('');
    }

    window.location.href = './reminder.html';
  });
});
