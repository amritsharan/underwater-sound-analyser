const revealItems = document.querySelectorAll(
  ".section, .hero, .card, .step, .doc-card"
);

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.2 }
);

revealItems.forEach((item, index) => {
  item.classList.add("reveal");
  item.style.transitionDelay = `${Math.min(index * 60, 360)}ms`;
  observer.observe(item);
});

// Upload + predict UI
const audioInput = document.getElementById('audioInput');
const uploadStatus = document.getElementById('uploadStatus');
if (audioInput) {
  audioInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    uploadStatus.textContent = 'Uploading...';
    try {
      const form = new FormData();
      form.append('file', file);
      const resp = await fetch('/predict', { method: 'POST', body: form });
      if (!resp.ok) throw new Error('Server error: ' + resp.status);
      const data = await resp.json();
      uploadStatus.textContent = data.prediction ? `Prediction: ${data.prediction}` : 'No prediction returned';
    } catch (err) {
      uploadStatus.textContent = 'Error: ' + err.message;
    }
    // reset input so same file can be reselected
    audioInput.value = '';
  });
}
