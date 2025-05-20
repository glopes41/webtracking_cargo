let watchId;

document.addEventListener("DOMContentLoaded", function () {
    let button = document.getElementById("submit");
    let container = document.getElementById("message");

    if (container) {
        container.innerHTML = `<p>Aguardando localização ...</p>`;
    }

    if (button) {
        button.style.display = "none";
    }

    fetch(`/orders/order-in-progress/`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                if (Object.keys(data).length > 0) {
                    console.log("id: ", data.order.order_id);
                    iniciarRastreamento(data.order.order_id);
                    send(data.order.order_id);
                }
                else {
                    container.innerHTML = `<p>Nenhuma ordem em adamento ...</p>`;
                }
            }
        })
        .catch(error => console.error("❌ Erro ao buscar ordens:", error));
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Verifica se este cookie começa com o nome desejado
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function iniciarRastreamento(ordemId) {
    if (navigator.geolocation) {
        watchId = navigator.geolocation.watchPosition(position => {
            let container = document.getElementById("message");
            let button = document.getElementById("submit");
            console.log("!!Marcador!!");
            let dados = {
                latitude: -23.5888,
                longitude: -46.6059
                // latitude: position.coords.latitude,
                // longitude: position.coords.longitude
            };
            console.log("csrf: ", getCookie("csrftoken"));
            fetch(`/tracker/update-location/`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
                body: JSON.stringify(dados)
            })
                .then(response => response.json())
                .then(data => {
                    console.log("📍 Localização enviada:", data);
                    container.innerHTML = `<p>Enviando localização</p><p>latitude: ${dados.latitude}</p><p>longitude: ${dados.longitude}</p>`;
                    button.innerText = "Concluir";
                    button.style.display = "inline-block";
                })
                .catch(error => console.error("❌ Erro ao enviar localização:", error));
            // }
        },
            error => {
                console.error("Erro na geolocalização:", error);
            },
            { enableHighAccuracy: true, maximumAge: 30000, timeout: 60000 });
    }
    else {
        console.log("Geolocalização não suportada");
    }
}

function send(order_id) {
    let container = document.getElementById("message");
    let button = document.getElementById("submit");

    if (!button) {
        console.error("⚠️ Botão de envio não encontrado.");
        return;
    }

    button.addEventListener("click", function (event) {
        event.preventDefault(); // Evita o recarregamento da página

        let url = `/orders/update/status/`;
        let dados = {
            status: "concluida",
            id_order: order_id,
            id_driver: 6
        };

        fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
            body: JSON.stringify(dados)
        })
            .then(response => response.json())
            .then(data => {
                console.log("✔️ Entrega finalizada!");
                stopTracking();
            })
            .catch(error => console.error("❌ Erro ao enviar mensagem de concluído:", error));
    });
}

// Função para parar o rastreamento
function stopTracking() {
    navigator.geolocation.clearWatch(watchId);
    let container = document.getElementById("message");
    if (container) {
        container.innerHTML = `<p>✔️ Entrega finalizada!</p><p>📍 Rastreamento encerrado.</p>`;
    }
    let button = document.getElementById("submit");
    if (button) {
        button.style.display = "none";  // 🔴 Esconde o botão
    }
}
