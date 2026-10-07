document.addEventListener("DOMContentLoaded", () => {
    let tamanhoFonte = 100;
    const body = document.body;

    // TOGGLE DO MENU DE ACESSIBILIDADE
    const btnToggle = document.getElementById("btn-toggle-acessibilidade");
    const menuAcessibilidade = document.getElementById("acessibilidade-menu");

    if (btnToggle && menuAcessibilidade) {
        btnToggle.addEventListener("click", (e) => {
            e.stopPropagation();
            menuAcessibilidade.classList.toggle("ativo");
        });

        // Fecha o menu se clicar em qualquer área fora dele
        document.addEventListener("click", (e) => {
            if (!menuAcessibilidade.contains(e.target) && !btnToggle.contains(e.target)) {
                menuAcessibilidade.classList.remove("ativo");
            }
        });
    }

    // 1. AUMENTAR FONTE
    document.getElementById("btn-aumentar").addEventListener("click", () => {
        if (tamanhoFonte < 150) {
            tamanhoFonte += 10;
            body.style.fontSize = tamanhoFonte + "%";
        }
    });

    // 2. DIMINUIR FONTE
    document.getElementById("btn-diminuir").addEventListener("click", () => {
        if (tamanhoFonte > 80) {
            tamanhoFonte -= 10;
            body.style.fontSize = tamanhoFonte + "%";
        }
    });

    // 3. MODO ESCURO / ALTO CONTRASTE
    document.getElementById("btn-contraste").addEventListener("click", () => {
        body.classList.toggle("modo-escuro");
    });

    // 4. LER PÁGINA (Sintetizador de Voz Nativo)
    let estaLendo = false;
    document.getElementById("btn-ler").addEventListener("click", () => {
        if (estaLendo) {
            window.speechSynthesis.cancel();
            estaLendo = false;
        } else {
            const textoDaPagina = document.body.innerText;
            const sintese = new SpeechSynthesisUtterance(textoDaPagina);
            sintese.lang = 'pt-BR';

            window.speechSynthesis.speak(sintese);
            estaLendo = true;

            sintese.onend = () => { estaLendo = false; };
        }
    });
});