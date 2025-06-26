const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');

// Abrir sidebar
document.getElementById('menu-toggle').addEventListener('click', () => {
  sidebar.classList.add('show');
  overlay.classList.add('show');
});

// Cerrar sidebar con botón ✖
document.getElementById('close-sidebar').addEventListener('click', () => {
  sidebar.classList.remove('show');
  overlay.classList.remove('show');
});

// Cerrar sidebar tocando fuera (overlay)
overlay.addEventListener('click', () => {
  sidebar.classList.remove('show');
  overlay.classList.remove('show');
});

// Subcategorías desplegables
document.querySelectorAll('.has-submenu > strong').forEach(item => {
  item.addEventListener('click', () => {
    const parent = item.parentElement;
    parent.classList.toggle('open');
  });
});
