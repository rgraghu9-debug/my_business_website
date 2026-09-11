// ── Mobile Nav Toggle ─────────────────────────────
function handleMobileMenuToggle(e) {
  if (e) {
    e.stopPropagation();
    e.preventDefault();
  }
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks');
  const hamburgerIcon = document.getElementById('hamburger-icon');

  if (!navLinks) return;
  const isHidden = navLinks.classList.contains('hidden') || navLinks.style.display === 'none' || window.getComputedStyle(navLinks).display === 'none';

  if (isHidden) {
    navLinks.classList.remove('hidden');
    navLinks.style.display = 'flex';
    if (hamburger) hamburger.setAttribute('aria-expanded', 'true');
    if (hamburgerIcon) hamburgerIcon.textContent = 'close';
  } else {
    navLinks.classList.add('hidden');
    navLinks.style.display = 'none';
    if (hamburger) hamburger.setAttribute('aria-expanded', 'false');
    if (hamburgerIcon) hamburgerIcon.textContent = 'menu';
  }
}

window.toggleMobileMenu = handleMobileMenuToggle;

document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks');

  if (hamburger) {
    hamburger.onclick = handleMobileMenuToggle;
  }

  // Close nav on outside click
  document.addEventListener('click', (e) => {
    if (hamburger && navLinks && !hamburger.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.add('hidden');
      navLinks.style.display = 'none';
      hamburger.setAttribute('aria-expanded', 'false');
      const hamburgerIcon = document.getElementById('hamburger-icon');
      if (hamburgerIcon) {
        hamburgerIcon.textContent = 'menu';
      }
    }
  });
});

// ── Scroll Fade-in Animation ──────────────────────
const fadeEls = document.querySelectorAll('.fade-in');

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

fadeEls.forEach((el) => observer.observe(el));

// ── Auto-dismiss messages ─────────────────────────
const messages = document.querySelectorAll('.message');
messages.forEach((msg) => {
  setTimeout(() => {
    msg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    msg.style.opacity = '0';
    msg.style.transform = 'translateX(100%)';
    setTimeout(() => msg.remove(), 500);
  }, 4000);
});

// ── Smooth scroll for anchor links ───────────────
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (e) => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── Active nav highlight on scroll ───────────────
const sections = document.querySelectorAll('section[id]');
if (sections.length) {
  const scrollSpy = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const link = document.querySelector(`a[href="#${entry.target.id}"]`);
      if (link) link.classList.toggle('active', entry.isIntersecting);
    });
  }, { threshold: 0.4 });
  sections.forEach((s) => scrollSpy.observe(s));
}
