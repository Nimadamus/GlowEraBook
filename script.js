document.getElementById('year').textContent = new Date().getFullYear();

const header = document.getElementById('siteHeader');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 40);
});

const coverImg = document.getElementById('coverImg');
const bookCover = document.getElementById('bookCover');
coverImg.addEventListener('error', () => bookCover.classList.add('no-image'));

const revealEls = document.querySelectorAll('[data-reveal]');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });
revealEls.forEach(el => observer.observe(el));

const form = document.querySelector('.contact-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button');
    const original = btn.textContent;
    btn.textContent = 'Thank You!';
    form.querySelector('input').value = '';
    setTimeout(() => { btn.textContent = original; }, 2500);
  });
}
