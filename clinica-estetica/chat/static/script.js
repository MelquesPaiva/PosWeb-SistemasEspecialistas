const chatBox = document.getElementById("chat-box");

function showMessage(message, sender) {
    if (sender == 'bot') {
        message = message + " 🤖"
    } else {
        message = "👤 " + message
    }

    const messageElement = document.createElement("div");
    messageElement.className = sender;
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showPrescription(prescription) {
    const messageElement = document.createElement("div");
    messageElement.className = "bot"

    const linkElement = document.createElement("a")
    linkElement.href = "/prescription/" + prescription.path
    linkElement.textContent = prescription.title + " 🤖"
    linkElement.target = "_self";
    messageElement.appendChild(linkElement);

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (message === "") return;

    showMessage(message, "user");

    input.value = "";

    fetch("/response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: message })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro na resposta do servidor");
            }
            return response.json();
        })
        .then(data => {
            if (data.response) {
                if (data.prescriptions.length) {
                    showMessage("As seguintes prescrições foram encontradas", "bot")
                    data.prescriptions.forEach(prescription => {
                        showPrescription(prescription)
                    })
                }

                showMessage(data.response, "bot");
            } else {
                throw new Error("Resposta inválida do servidor");
            }
        })
}

function searchPrescriptions() {
    fetch("/response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: "quero receiturarios" })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro na resposta do servidor");
            }
            return response.json();
        })
        .then(data => {
            if (data.response) {
                showMessage(data.response, "bot")
            } else {
                throw new Error("Resposta inválida do servidor");
            }
        })
}

document.getElementById("user-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter") sendMessage();
});