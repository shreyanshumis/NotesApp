(() => {
  const button = document.querySelector('.theme-toggle');
  const savedTheme = localStorage.getItem('scribe-theme');
  if (savedTheme === 'dark') document.documentElement.dataset.theme = 'dark';
  button?.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    document.documentElement.dataset.theme = dark ? 'dark' : '';
    localStorage.setItem('scribe-theme', dark ? 'dark' : 'light');
  });

  const cursor = document.querySelector('.cursor-blob');
  if (!cursor) return;

  document.documentElement.classList.add('custom-cursor');
  document.addEventListener('pointermove', (event) => {
    cursor.style.left = `${event.clientX}px`;
    cursor.style.top = `${event.clientY}px`;
    cursor.classList.add('is-visible');
  });
  document.addEventListener('pointerover', (event) => {
    cursor.classList.toggle('is-active', Boolean(event.target.closest('a, button, input, textarea, label, .note-card')));
  });
  document.addEventListener('pointerout', (event) => {
    if (!event.relatedTarget) cursor.classList.remove('is-visible', 'is-active');
  });
})();
