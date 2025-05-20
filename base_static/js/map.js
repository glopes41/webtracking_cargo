document.addEventListener("DOMContentLoaded", function () {
    // Extrair o order_id da URL atual
    const urlParts = window.location.pathname.split('/');
    const orderId = urlParts[urlParts.length - 2]; // ex: /map/5/ → "5"

    // Monta diretamente a URL da API
    const apiUrl = `/tracker/get-route/${orderId}/`;
    console.log("url: ", apiUrl);

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (!data.locations) {
                console.warn("❌ Nenhuma localização disponível.");
                return;
            }

            const routeCoordinates = [data.locations.latitude, data.locations.longitude];
            console.log("📍 Localização:", data.locations);

            const map = L.map("map").setView(routeCoordinates, 15);
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);
            const driverName = data.locations.driver_name;
            L.marker(routeCoordinates).addTo(map).bindPopup(`🚚 ${driverName}`, {
                autoClose: false,
                closeOnClick: false
            })
                .openPopup();
        })
        .catch(error => console.error("❌ Erro ao buscar localizações:", error));
});
