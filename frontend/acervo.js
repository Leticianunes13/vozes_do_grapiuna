document.addEventListener("DOMContentLoaded", () => {

    const API_URL = "http://127.0.0.1:8000/autores/";

    const containerFotos = document.getElementById("lista-fotos");
    const tituloNome = document.getElementById("nome-autor");
    const textoResumo = document.getElementById("resumo-autor");
    const listaObras = document.getElementById("lista-obras");

    // 1. BUSCA OS AUTORES NO BACKEND
    async function buscarAutores() {
        try {
            const resposta = await fetch(API_URL);

            if (!resposta.ok) {
                throw new Error(`Erro na requisição: ${resposta.status}`);
            }

            const autores = await resposta.json();

            if (autores.length === 0) {
                tituloNome.textContent = "Nenhum autor encontrado";
                textoResumo.textContent = "Ainda não há escritores cadastrados no acervo.";
                return;
            }

            carregarCarrossel(autores);
            exibirDetalhesAutor(autores[0]);

        } catch (erro) {
            console.error("Erro ao conectar com o backend:", erro);
            tituloNome.textContent = "Erro ao carregar dados";
            textoResumo.textContent = "Não foi possível conectar ao servidor. Verifique se o FastAPI está rodando.";
        }
    }

    // 2. CARROSSEL (Lê a foto_url diretamente do banco Neon)
    function carregarCarrossel(autores) {
        containerFotos.innerHTML = "";

        autores.forEach((autor, index) => {
            const divFoto = document.createElement("div");
            divFoto.classList.add("foto-autor");

            if (autor.foto_url) {
                const img = document.createElement("img");
                img.src = autor.foto_url;
                img.alt = autor.nome_autor;

                img.onerror = () => {
                    divFoto.innerHTML = "";
                    divFoto.textContent = autor.nome_autor.charAt(0);
                };

                divFoto.appendChild(img);
            } else {
                divFoto.textContent = autor.nome_autor.charAt(0);
            }

            if (index === 0) divFoto.classList.add("ativo");

            divFoto.addEventListener("click", () => {
                document.querySelectorAll(".foto-autor").forEach(f => f.classList.remove("ativo"));
                divFoto.classList.add("ativo");

                exibirDetalhesAutor(autor);
            });

            containerFotos.appendChild(divFoto);
        });
    }

    // 3. EXIBE BIOGRAFIA E LISTA DE OBRAS
    function exibirDetalhesAutor(autor) {
        tituloNome.textContent = autor.nome_autor;
        textoResumo.textContent = autor.historia;

        listaObras.innerHTML = "";

        if (autor.obras && autor.obras.length > 0) {
            autor.obras.forEach(obra => {
                const card = document.createElement("div");
                card.classList.add("card-obra");

                card.innerHTML = `
                    <div class="info-livro">
                        <h4 class="titulo-livro">📖 ${obra}</h4>
                        <p class="resumo-livro">${autor.resumo_obras || 'Sinopse não disponível para esta obra.'}</p>
                    </div>
                `;

                listaObras.appendChild(card);
            });
        } else {
            listaObras.innerHTML = "<p class='resumo-livro'>Nenhuma obra cadastrada para este autor.</p>";
        }
    }

    buscarAutores();
});