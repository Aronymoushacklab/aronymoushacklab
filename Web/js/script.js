(() => {
  // Seguridad: Esperar DOM cargado
  document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const menuToggle = document.getElementById('menu-toggle');
    const closeSidebar = document.getElementById('close-sidebar');

    if (!sidebar || !overlay || !menuToggle || !closeSidebar) {
      console.warn('Sidebar elements not found.');
      return;
    }

    const openSidebar = () => {
      sidebar.classList.add('show');
      overlay.classList.add('show');
      document.body.classList.add('no-scroll');
    };

    const closeSidebarFn = () => {
      sidebar.classList.remove('show');
      overlay.classList.remove('show');
      document.body.classList.remove('no-scroll');
    };

    // Botón abrir sidebar
    menuToggle.addEventListener('click', openSidebar);

    // Botón cerrar ✖
    closeSidebar.addEventListener('click', closeSidebarFn);

    // Click en overlay
    overlay.addEventListener('click', closeSidebarFn);

    // Submenús desplegables (delegación de eventos segura)
    sidebar.addEventListener('click', (e) => {
      const trigger = e.target.closest('.has-submenu > strong');
      if (trigger) {
        const parent = trigger.parentElement;
        if (parent) {
          parent.classList.toggle('open');
        }
      }
    });

    // Extra: Cerrar con tecla ESC
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeSidebarFn();
      }
    });
  });
})();
