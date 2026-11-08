export const initFilters = () => {
  document.querySelectorAll<HTMLElement>('[data-filter-root]').forEach((root) => {
    const buttons = [...root.querySelectorAll<HTMLButtonElement>('[data-filter]')];
    const input = root.querySelector<HTMLInputElement>('[data-filter-search]');
    const items = [...root.querySelectorAll<HTMLElement>('[data-filter-item]')];
    const count = root.querySelector<HTMLElement>('[data-result-count]');
    const empty = root.querySelector<HTMLElement>('[data-filter-empty]');
    let category = 'All';

    const apply = () => {
      const query = (input?.value || '').trim().toLocaleLowerCase();
      let visible = 0;
      items.forEach((item) => {
        const categoryMatch = category === 'All' || item.dataset.category === category;
        const searchMatch = !query || (item.dataset.search || '').toLocaleLowerCase().includes(query);
        const show = categoryMatch && searchMatch;
        item.hidden = !show;
        if (show) visible += 1;
      });
      if (count) count.textContent = `${visible} item${visible === 1 ? '' : 's'} shown`;
      if (empty) empty.dataset.visible = String(visible === 0);
    };

    buttons.forEach((button) => button.addEventListener('click', () => {
      category = button.dataset.filter || 'All';
      buttons.forEach((candidate) => candidate.setAttribute('aria-pressed', String(candidate === button)));
      apply();
    }));
    input?.addEventListener('input', apply);
    apply();
  });
};
