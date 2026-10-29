// Accessible mobile navigation; links remain usable without JavaScript.
const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() {
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', 'Buka menu');
  navigation.classList.remove('is-open');
}
toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
  navigation.classList.toggle('is-open', open);
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation.classList.contains('is-open')) {
    closeMenu();
    toggle.focus();
  }
});
// Filter only the work samples, while keeping all evidence visible by default.
const filters = document.querySelectorAll('[data-filter]');
const works = document.querySelectorAll('[data-category]');
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(item => {
    item.classList.toggle('active', item === button);
    item.setAttribute('aria-pressed', String(item === button));
  });
  let visible = 0;
  works.forEach(work => {
    work.hidden = button.dataset.filter !== 'all' && work.dataset.category !== button.dataset.filter;
    if (!work.hidden) visible++;
  });
  document.querySelector('#filter-status').textContent = `Menampilkan ${visible} karya`;
}));
// Native dialog provides keyboard trapping, Escape dismissal, and focus return.
const lightbox = document.querySelector('#lightbox');
const lightboxImage = document.querySelector('#lightbox-image');
document.querySelectorAll('[data-image]').forEach(button => button.addEventListener('click', () => {
  lightboxImage.src = button.dataset.image;
  lightboxImage.alt = button.dataset.caption;
  document.querySelector('#lightbox-caption').textContent = button.dataset.caption;
  lightbox.showModal();
  document.body.classList.add('modal-open');
}));
document.querySelector('.close-lightbox').addEventListener('click', () => lightbox.close());
lightbox.addEventListener('click', event => {
  if (event.target === lightbox) {
    const box = lightbox.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) lightbox.close();
  }
});
lightbox.addEventListener('close', () => document.body.classList.remove('modal-open'));
// Highlight the currently visible section without changing browser history.
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navigation.querySelectorAll('a[href^="#"]').forEach(link => {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });
  }, { rootMargin: '-15% 0px -65% 0px' });
  ['ringkasan', 'pengalaman', 'bukti', 'kontak'].forEach(id => observer.observe(document.getElementById(id)));
}
