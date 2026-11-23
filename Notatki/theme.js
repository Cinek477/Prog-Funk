(() => {
  const key = 'prog-funk-theme';
  const button = document.getElementById('theme');
  if (!button) return;
  function apply(value) {
    const dark = value === 'dark';
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    button.textContent = dark ? 'Motyw: ciemny' : 'Motyw: jasny';
    button.setAttribute('aria-label', 'Ciemny motyw');
    button.setAttribute('aria-pressed', String(dark));
  }
  try { apply(localStorage.getItem(key)); } catch { apply('light'); }
  button.hidden = false;
  button.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    apply(next);
    try { localStorage.setItem(key, next); } catch { /* Storage can be disabled. */ }
  });
  window.addEventListener('storage', event => { if (event.key === key) apply(event.newValue); });
})();
