document.addEventListener("DOMContentLoaded", function () {
    let button = document.getElementById("send");
    let container = document.getElementById("message");

    fetch(`/orders/open/`)
        .then(response => response.json())
        .then(data => {
            if (Object.keys(data).length > 0) {
                if (button) {
                    button.style.display = "inline-block";
                }
                console.log("data: ", data);
                radio_create(data);
                send_choice();
            }
            else {
                if (button) {
                    button.style.display = "none";
                }
                if (container) {
                    container.innerHTML = "<p>Não há entregas disponíveis<p>";
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

function radio_create(data) {
    let container = document.getElementById("message");

    if (!data || data.length === 0) {
        container.innerHTML = "<p>Nenhum item disponível.</p>";
        return;
    }

    data.forEach(item => {
        const label = document.createElement("label");
        const input = document.createElement("input");

        input.type = "radio";
        input.name = "item";
        input.value = item.id;

        label.appendChild(input);
        label.append(` ${item.delivery_date}  ${item.client__name} `);
        label.appendChild(document.createElement("br"));




        //label.innerHTML = `<input type="radio" name="item" value="${item.id}"> ${item.delivery_date} ${item.status}<br>`;
        container.appendChild(label);

    });
    const button = document.createElement("button");
    button.type = "submit";  // Se estiver dentro de um <form>
    button.textContent = "Enviar";
    button.id = "send";
    container.appendChild(button);
}

function send_choice() {
    // Evento de envio do formulário
    let button = document.getElementById("send");
    if (!button) {
        console.error("⚠️ Botão de envio não encontrado.");
        return;
    }
    button.addEventListener("click", function (event) {
        event.preventDefault(); // Evita o recarregamento da página

        let selectedItem = document.querySelector('input[name="item"]:checked');

        if (!selectedItem) {
            alert("Escolha um item antes de enviar!");
            return;
        }

        // Enviar item selecionado para a API
        fetch(`/orders/choice/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ id_order: selectedItem.value }) // Resolver id driver!!!
        })
            .then(response => response.json())
            .then(result => {
                console.log("Resposta do servidor:", result.message);
                if (result.message == "OK") {
                    window.location.href = `/tracker/tracking/`;
                }
            })
            .catch(error => console.error("Erro ao enviar item:", error));
    });
}