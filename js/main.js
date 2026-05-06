/* ============================================================
   STUDIO DENTAIRE BELMONT — main.js
   Site démo Nextiweb.ca — Vanilla JS, zéro dépendance
   ============================================================ */
(function () {
  'use strict';

  // Détection langue
  const isEN = document.documentElement.lang.startsWith('en');

  // Textes bilingues
  const t = isEN ? {
    menuOpen: 'Open menu',
    menuClose: 'Close menu',
    formError: 'Please fill in all required fields correctly.',
    formEmailError: 'Please enter a valid email address.',
    formPhoneError: 'Please enter a valid phone number.',
    formSuccess: '✓ Demo site — your request would be sent to the practice.\n\nThank you!\n\n— Built by Nextiweb.ca',
    days: ['Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.'],
  } : {
    menuOpen: 'Ouvrir le menu',
    menuClose: 'Fermer le menu',
    formError: 'Merci de remplir correctement tous les champs obligatoires.',
    formEmailError: 'Merci d\'entrer une adresse courriel valide.',
    formPhoneError: 'Merci d\'entrer un numéro de téléphone valide.',
    formSuccess: '✓ Site démo — votre demande serait transmise au cabinet.\n\nMerci !\n\n— Conçu par Nextiweb.ca',
    days: ['Dim.', 'Lun.', 'Mar.', 'Mer.', 'Jeu.', 'Ven.', 'Sam.'],
  };

  /* ----------- Header sticky scroll ----------- */
  const header = document.getElementById('site-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 12);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ----------- Menu mobile ----------- */
  const menuBtn = document.getElementById('menu-btn');
  const mobileNav = document.getElementById('mobile-nav');
  if (menuBtn && mobileNav) {
    const toggleMenu = (open) => {
      const isOpen = open !== undefined ? open : !mobileNav.classList.contains('is-open');
      mobileNav.classList.toggle('is-open', isOpen);
      menuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      menuBtn.setAttribute('aria-label', isOpen ? t.menuClose : t.menuOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    };
    menuBtn.addEventListener('click', () => toggleMenu());
    mobileNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => toggleMenu(false));
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileNav.classList.contains('is-open')) toggleMenu(false);
    });
  }

  /* ----------- Smooth scroll pour ancres (au cas où le navigateur ne le fait pas) ----------- */
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (href === '#' || href.length < 2) return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Maj URL sans recharger
      history.pushState(null, '', href);
    });
  });

  /* ----------- Calendrier visuel : injection de la semaine en cours ----------- */
  const slotsWeek = document.getElementById('slots-week');
  if (slotsWeek) {
    const today = new Date();
    const startOfWeek = new Date(today);
    const day = today.getDay();
    // Lundi = 1, Dimanche = 0 → on démarre le lundi
    const offset = day === 0 ? -6 : 1 - day;
    startOfWeek.setDate(today.getDate() + offset);

    let html = '';
    for (let i = 0; i < 5; i++) {
      const d = new Date(startOfWeek);
      d.setDate(startOfWeek.getDate() + i);
      const isToday = d.toDateString() === today.toDateString();
      html += `
        <div class="slot-day"${isToday ? ' style="background:var(--c-primary-light);"' : ''}>
          <div class="slot-day__name">${t.days[d.getDay()]}</div>
          <div class="slot-day__num">${d.getDate()}</div>
        </div>`;
    }
    slotsWeek.innerHTML = html;
  }

  /* ----------- Sélection créneau RDV ----------- */
  const slots = document.querySelectorAll('.slot:not(.is-taken)');
  const messageField = document.getElementById('message');
  slots.forEach((slot) => {
    slot.addEventListener('click', () => {
      slots.forEach((s) => s.classList.remove('is-selected'));
      slot.classList.add('is-selected');
      const value = slot.getAttribute('data-slot');
      if (messageField) {
        const prefix = isEN ? 'Preferred slot: ' : 'Créneau souhaité : ';
        const existing = messageField.value;
        // Remplace toute ligne existante "Créneau souhaité"
        const cleaned = existing.replace(/^(Créneau souhaité|Preferred slot)\s*:.*\n?/m, '');
        messageField.value = `${prefix}${value}\n${cleaned}`.trim();
      }
      // Scroll doux vers le formulaire
      const form = document.getElementById('rdv-form');
      if (form) form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  /* ----------- Validation formulaire RDV ----------- */
  const form = document.getElementById('rdv-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const required = form.querySelectorAll('[required]');
      let valid = true;
      let firstInvalid = null;

      required.forEach((field) => {
        const v = (field.value || '').trim();
        const isEmail = field.type === 'email';
        const isPhone = field.type === 'tel';
        let fieldValid = v.length > 0;
        if (isEmail && fieldValid) {
          fieldValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
        }
        if (isPhone && fieldValid) {
          // Accepte 10 chiffres dans n'importe quel format
          fieldValid = (v.replace(/\D/g, '').length >= 10);
        }
        if (!fieldValid) {
          field.style.borderColor = '#D04A4A';
          valid = false;
          if (!firstInvalid) firstInvalid = field;
        } else {
          field.style.borderColor = '';
        }
      });

      if (!valid) {
        const emailField = form.querySelector('input[type="email"]');
        const phoneField = form.querySelector('input[type="tel"]');
        let msg = t.formError;
        if (emailField && emailField.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailField.value.trim())) {
          msg = t.formEmailError;
        } else if (phoneField && phoneField.value.trim() && phoneField.value.replace(/\D/g, '').length < 10) {
          msg = t.formPhoneError;
        }
        alert(msg);
        if (firstInvalid) firstInvalid.focus();
        return;
      }

      alert(t.formSuccess);
      form.reset();
      slots.forEach((s) => s.classList.remove('is-selected'));
    });

    // Reset border on input
    form.querySelectorAll('input, select, textarea').forEach((field) => {
      field.addEventListener('input', () => { field.style.borderColor = ''; });
    });
  }

  /* ----------- Reveal on scroll (IntersectionObserver) ----------- */
  if ('IntersectionObserver' in window) {
    const targets = document.querySelectorAll('.service, .member, .pillar, .testi, .info-block, .pricing__row');
    targets.forEach((el) => el.classList.add('reveal'));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    targets.forEach((el) => io.observe(el));
  }

  /* ----------- Année dynamique footer (si présente) ----------- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
