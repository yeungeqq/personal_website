'use strict';

const menuButton = document.querySelector('[data-menu-toggle]');
const navigation = document.querySelector('#site-navigation');

if (menuButton && navigation) {
  menuButton.hidden = false;
  const setMenu = (open) => {
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  };
  menuButton.addEventListener('click', () => {
    setMenu(menuButton.getAttribute('aria-expanded') !== 'true');
  });
  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      menuButton.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-header')) setMenu(false);
  });
  window.matchMedia('(min-width: 761px)').addEventListener('change', () => setMenu(false));
}

const filters = document.querySelector('[data-filters]');
if (filters) {
  const cards = [...document.querySelectorAll('[data-project-card]')];
  const status = document.querySelector('[data-filter-status]');
  filters.hidden = false;
  filters.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-category]');
    if (!button) return;
    const category = button.dataset.category;
    filters.querySelectorAll('button').forEach((item) => {
      item.setAttribute('aria-pressed', String(item === button));
    });
    cards.forEach((card) => {
      card.hidden = category !== 'all' && card.dataset.category !== category;
    });
    const count = cards.filter((card) => !card.hidden).length;
    status.textContent = `${count} projects · ${button.textContent.trim()}`;
  });
}