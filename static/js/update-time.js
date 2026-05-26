// static/js/update-time-simple.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('Script de actualización de hora iniciado');
    
    function updateTime() {
        fetch('/usuarios/get-current-time/')
            .then(response => response.json())
            .then(data => {
                console.log('Hora recibida:', data.time);
                
                // Actualizar por ID
                const timeElement = document.getElementById('current-time');
                const dateElement = document.getElementById('current-date');
                
                // Si no hay IDs, buscar por estructura
                if (!timeElement) {
                    const container = document.querySelector('.datetime-container');
                    if (container) {
                        const spans = container.querySelectorAll('span');
                        if (spans.length >= 2) {
                            spans[1].textContent = data.time;
                            if (spans.length >= 1 && data.date) {
                                spans[0].textContent = data.date;
                            }
                        }
                    }
                } else {
                    // Usar IDs
                    if (timeElement && data.time) {
                        timeElement.textContent = data.time;
                    }
                    if (dateElement && data.date) {
                        dateElement.textContent = data.date;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback a hora local
                const now = new Date();
                const timeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                               now.getMinutes().toString().padStart(2, '0');
                const dateStr = now.getDate().toString().padStart(2, '0') + '/' +
                              (now.getMonth() + 1).toString().padStart(2, '0') + '/' +
                              now.getFullYear();
                
                const timeElement = document.getElementById('current-time') || 
                                  document.querySelector('.datetime-container span:nth-child(2)');
                const dateElement = document.getElementById('current-date') || 
                                  document.querySelector('.datetime-container span:nth-child(1)');
                
                if (timeElement) timeElement.textContent = timeStr;
                if (dateElement) dateElement.textContent = dateStr;
            });
    }
    
    // Asegurarse de que los elementos tengan IDs
    function prepareElements() {
        const container = document.querySelector('.datetime-container');
        if (container && !document.getElementById('current-time')) {
            const spans = container.querySelectorAll('span');
            // El primer span es la fecha
            if (spans[0] && !spans[0].id) spans[0].id = 'current-date';
            // El tercer span es la hora (porque hay un separador en medio)
            if (spans[2] && !spans[2].id) spans[2].id = 'current-time';
        }
    }
    
    prepareElements();
    updateTime(); // Actualizar inmediatamente
    setInterval(updateTime, 60000); // Cada minuto
});