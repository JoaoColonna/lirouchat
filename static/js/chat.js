const sidebar = document.getElementById('sidebar');
        const toggleButton = document.getElementById('toggle-button');

        // Alterna entre abrir e fechar o menu lateral
        toggleButton.addEventListener('click', function() {
            if (sidebar.classList.contains('sidebar-closed')) {
                sidebar.classList.remove('sidebar-closed');
                sidebar.classList.add('sidebar-open');
                toggleButton.textContent = 'Fechar Menu';
            } else {
                sidebar.classList.remove('sidebar-open');
                sidebar.classList.add('sidebar-closed');
                toggleButton.textContent = 'Abrir Menu';
            }
        });