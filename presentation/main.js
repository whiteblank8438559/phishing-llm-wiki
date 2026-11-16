(() => {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const previous = document.getElementById('prev-slide');
  const next = document.getElementById('next-slide');
  const counter = document.getElementById('slide-counter');
  const progress = document.getElementById('progress-fill');
  const feedback = document.getElementById('quiz-feedback');
  let current = 0;

  function indexFromHash() {
    const match = location.hash.match(/^#slide-(\d+)$/);
    if (!match) return 0;
    return Math.min(slides.length - 1, Math.max(0, Number(match[1]) - 1));
  }

  function showSlide(index, updateHash = true) {
    current = Math.min(slides.length - 1, Math.max(0, index));
    slides.forEach((slide, i) => {
      slide.hidden = i !== current;
    });
    counter.textContent = `${current + 1} / ${slides.length}`;
    progress.style.width = `${((current + 1) / slides.length) * 100}%`;
    previous.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    if (updateHash) history.replaceState(null, '', `#slide-${current + 1}`);
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  document.documentElement.classList.add('js');
  showSlide(indexFromHash(), false);

  previous.addEventListener('click', () => showSlide(current - 1));
  next.addEventListener('click', () => showSlide(current + 1));
  document.querySelectorAll('[data-next]').forEach(button => button.addEventListener('click', () => showSlide(current + 1)));
  document.querySelectorAll('[data-restart]').forEach(button => button.addEventListener('click', () => showSlide(0)));
  document.querySelector('.brand').addEventListener('click', event => {
    event.preventDefault();
    showSlide(0);
  });
  window.addEventListener('hashchange', () => showSlide(indexFromHash(), false));
  document.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.target.closest('button, a')) return;
    if (event.key === 'ArrowRight' || event.key === 'PageDown') showSlide(current + 1);
    if (event.key === 'ArrowLeft' || event.key === 'PageUp') showSlide(current - 1);
    if (event.key === 'Home') showSlide(0);
    if (event.key === 'End') showSlide(slides.length - 1);
  });

  document.querySelectorAll('.quiz-option').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.quiz-option').forEach(option => {
        option.classList.remove('is-correct', 'is-wrong');
        option.setAttribute('aria-pressed', 'false');
      });
      const correct = button.dataset.answer === 'correct';
      button.classList.add(correct ? 'is-correct' : 'is-wrong');
      button.setAttribute('aria-pressed', 'true');
      feedback.textContent = correct
        ? '答對了。先暫停，再由你自己開啟官方 App 或網站查證。'
        : '再想想：別使用可疑訊息提供的連結或聯絡方式，先獨立查證。';
    });
  });
})();
