// Debrief page logic
// - Captures required questionnaire (matches screenshot)
// - Enables Done only when all questions completed
// - Ensures combined data is submitted
// - Shows completion code and copy button

const submitBtn = document.getElementById('debrief-submit');
const form = document.getElementById('debrief-form');
const errorEl = document.getElementById('debrief-error');
const completionEl = document.getElementById('completion');
const codeEl = document.getElementById('completion-code');
const copyBtn = document.getElementById('copy-code');

function setError(msg) {
  if (!errorEl) return;
  if (!msg) {
    errorEl.style.display = 'none';
    errorEl.textContent = '';
    return;
  }
  errorEl.textContent = msg;
  errorEl.style.display = 'block';
}

function getFormData({ includeEmpty = false } = {}) {
  if (!form) return {};
  const fd = new FormData(form);
  const obj = {};
  for (const [k, v] of fd.entries()) {
    const value = typeof v === 'string' ? v.trim() : v;
    if (includeEmpty) {
      obj[k] = value;
    } else if (value !== '') {
      obj[k] = value;
    }
  }
  return obj;
}

function setDoneEnabled(enabled) {
  if (!submitBtn) return;
  submitBtn.disabled = !enabled;
  submitBtn.style.opacity = enabled ? '1' : '0.35';
}

function isFormComplete() {
  if (!form) return false;

  // Use native constraint validation where possible.
  // If any required field is missing, form.checkValidity() returns false.
  try {
    return form.checkValidity();
  } catch (_) {
    return false;
  }
}

function updateUi() {
  const complete = isFormComplete();
  setDoneEnabled(complete);
  if (complete) setError('');
}

async function ensureSubmitted() {
  // If we already have a marker, don't spam the server.
  const already = localStorage.getItem('serverSubmissionSuccess');
  if (already === 'true') return { ok: true, skipped: true };

  if (typeof submitCombinedData !== 'function') {
    return { ok: false, error: 'Submission function not available.' };
  }

  const result = await submitCombinedData();
  if (result && result.success) {
    localStorage.setItem('serverSubmissionSuccess', 'true');
    return { ok: true };
  }

  return { ok: false, error: (result && result.error) ? result.error : 'Submission failed.' };
}

function showCompletion() {
  if (completionEl) completionEl.style.display = 'block';
}

// Keep Done disabled until all required fields completed.
if (form) {
  form.addEventListener('input', updateUi);
  form.addEventListener('change', updateUi);
}

// Initial state
updateUi();

submitBtn.addEventListener('click', async () => {
  setError('');
  // Guard: if incomplete, show message (should be prevented by disabled button)
  if (!isFormComplete()) {
    setError('Please answer all questions before continuing.');
    updateUi();
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';

  try {
    // Save debrief responses (required)
    const debrief = {
      ...getFormData({ includeEmpty: true }),
      prolificId: localStorage.getItem('prolificId') || null,
      participantId: localStorage.getItem('participantId') || null,
      submissionTime: new Date().toISOString()
    };
    localStorage.setItem('debriefData', JSON.stringify(debrief));

    // Attach debrief into existing experiment JSON blobs (so it reaches the server)
    // We keep this additive to avoid breaking old analysis scripts.
    const taskStr = localStorage.getItem('taskExperimentData');
    if (taskStr) {
      try {
        const taskObj = JSON.parse(taskStr);
        if (taskObj && typeof taskObj === 'object') {
          taskObj.debrief = debrief;
          localStorage.setItem('taskExperimentData', JSON.stringify(taskObj));
        }
      } catch (_) {}
    }

    const freeStr = localStorage.getItem('freeplayExperimentData');
    if (freeStr) {
      try {
        const freeObj = JSON.parse(freeStr);
        if (freeObj && typeof freeObj === 'object') {
          freeObj.debrief = debrief;
          localStorage.setItem('freeplayExperimentData', JSON.stringify(freeObj));
        }
      } catch (_) {}
    }

    const submitted = await ensureSubmitted();
    if (!submitted.ok) {
      // Allow retry: re-enable the button and keep the participant on this page.
      setError(
        'We could not submit your data automatically. Please check your internet connection and try again. '
        + 'If the issue persists, please contact the researcher.'
      );
      submitBtn.disabled = false;
      submitBtn.textContent = 'Done';
      updateUi();
      return;
    }

    showCompletion();
    submitBtn.textContent = 'Submitted ✓';
  } catch (e) {
    console.error(e);
    setError(
      'Something went wrong while submitting. Please try again. '
      + 'If the issue persists, please contact the researcher.'
    );
    submitBtn.disabled = false;
    submitBtn.textContent = 'Done';
    updateUi();
  } finally {
    // If we successfully submitted, keep disabled (avoid duplicates).
    // If not, we already re-enabled above.
    if (localStorage.getItem('serverSubmissionSuccess') === 'true') {
      submitBtn.disabled = true;
    }
  }
});

copyBtn?.addEventListener('click', async () => {
  const code = (codeEl?.textContent || '').trim();
  if (!code) return;
  try {
    await navigator.clipboard.writeText(code);
    copyBtn.textContent = 'Copied';
    setTimeout(() => (copyBtn.textContent = 'Copy'), 1200);
  } catch (e) {
    console.error(e);
    // silent fallback
  }
});
