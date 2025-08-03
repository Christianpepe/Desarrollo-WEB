function setupAutocomplete(inputId) {
    const input = document.getElementById(inputId);
    if (!input) {
        console.error(`Input element with id '${inputId}' not found`);
        return;
    }

    const datalistId = `${inputId}-list`;
    let datalist = document.getElementById(datalistId);

    if (!datalist) {
        datalist = document.createElement("datalist");
        datalist.id = datalistId;
        input.parentNode.insertBefore(datalist, input.nextSibling);
    }

    let debounceTimer;

    input.addEventListener("input", (e) => {
        const query = e.target.value.trim();
        clearTimeout(debounceTimer);
        if (query.length < 2) {
            datalist.innerHTML = "";
            return;
        }
        debounceTimer = setTimeout(() => {
            fetch(`/vuelos/api/autocompletar-aeropuertos/?q=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la respuesta del servidor');
                    }
                    return response.json();
                })
                .then(data => {
                    datalist.innerHTML = "";
                    if (Array.isArray(data) && data.length > 0) {
                        data.forEach(item => {
                            const option = document.createElement("option");
                            option.value = item;
                            datalist.appendChild(option);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error en la búsqueda de aeropuertos:', error);
                });
        }, 300);
    });

    // Al perder el foco o al presionar Enter, si el valor tiene formato "XXX - Nombre", deja solo el nombre
    function limpiarCodigoIATA() {
        const val = input.value;
        const match = val.match(/^[A-Z]{3}\s*-\s*(.+)$/);
        if (match) {
            input.value = match[1].trim();
        }
    }
    input.addEventListener("change", limpiarCodigoIATA);
    input.addEventListener("blur", limpiarCodigoIATA);
    input.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            setTimeout(limpiarCodigoIATA, 10);
        }
    });
}

// Al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    try {
        setupAutocomplete("origen");
        setupAutocomplete("destino");
    } catch (error) {
        console.error('Error al inicializar el autocompletado:', error);
    }
});
