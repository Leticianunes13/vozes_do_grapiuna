document.addEventListener("DOMContentLoaded", () => {

    // --- 1. CONFIGURAÇÃO DO MAPA (LEAFLET.JS) ---
    const map = L.map('mapa').setView([-14.7866, -39.2811], 13);

    // Adiciona a camada de visualização gratuita do OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Exemplo de Marcador no mapa
    L.marker([-14.7866, -39.2811]).addTo(map)
        .bindPopup('Centro de Itabuna - Berço literário.')
        .openPopup();


    // --- 2. RENDERIZAÇÃO DOS CARDS DA VITRINE ---
    const mockDadosAPI = [
        { nome: "João Silva", genero: "Poesia", contato: "@joao.silva", previa: "A chuva cai sobre o cacau..." },
        { nome: "Maria Costa", genero: "Crônica", contato: "@mariac", previa: "Era uma tarde de domingo na praça..." },
        { nome: "Ana Luz", genero: "Conto", contato: "@analuz", previa: "O mistério do Rio Cachoeira..." }
    ];

    const wrapper = document.getElementById("cards-wrapper");

    // Loop que cria a estrutura HTML igual ao seu desenho
    mockDadosAPI.forEach(texto => {
        const cardHTML = `
            <div class="card-texto">
                <div class="card-info">
                    <strong>${texto.nome}</strong>
                    <span>${texto.genero}</span>
                    <small>${texto.contato}</small>
                    <button class="btn-ler">Ler</button>
                </div>
                <div class="card-previa">
                    <p>"${texto.previa}"</p>
                </div>
            </div>
        `;
        wrapper.innerHTML += cardHTML;
    });

});

const btnacervo = document.getElementById("btn-acervo");
btnacervo.addEventListener("click", () => {
    if (btnacervo) {
        window.location.href = "acervo.html";
    } else {
        console.error("Pagina não encontrada");
    }
});