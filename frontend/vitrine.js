document.addEventListener("DOMContentLoaded", () => {
    // 1. FILTRAGEM DINÂMICA POR GÊNERO
    const filtroSelect = document.getElementById("filtro-genero");
    const cards = document.querySelectorAll(".card-vitrine");

    if (filtroSelect) {
        filtroSelect.addEventListener("change", (e) => {
            const generoSelecionado = e.target.value.toLowerCase();

            cards.forEach((card) => {
                const generoCard = card.getAttribute("data-genero") ? card.getAttribute("data-genero").toLowerCase() : "";

                if (generoSelecionado === "todos" || generoCard === generoSelecionado) {
                    card.classList.remove("oculto");
                } else {
                    card.classList.add("oculto");
                }
            });
        });
    }

    // 2. AÇÃO DO BOTÃO CTA (TELEGRAM)
    const btnCta = document.getElementById("btn-cta-texto");
    if (btnCta) {
        btnCta.addEventListener("click", () => {
            // Pode ser redirecionado para o link oficial do bot ou grupo do Telegram
            const telegramUrl = "https://t.me/vozesdograpiuna";
            window.open(telegramUrl, "_blank");
        });
    }
});

