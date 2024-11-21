document.addEventListener('DOMContentLoaded', function() {
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const body = document.body;

  sidebarToggle.addEventListener('click', function() {
      body.classList.toggle('sidebar-closed');
  });
});