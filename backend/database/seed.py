from database.infraestruturadb import SessionLocal
from database.models import Autor

AUTORES = [
    {
        "nome_autor": "Cyro de Mattos",
        "historia": "Nascido em Itabuna, Cyro de Mattos (1939) é um dos poetas, contistas e romancistas mais premiados da Bahia, vencedor do prestigiado Prêmio Casa das Américas e da Academia Brasileira de Letras. Membro fundador e presidente de honra da Academia de Letras de Itabuna (ALITA) e Doutor Honoris Causa pela UESC, sua obra é deeply marcada pelas memórias do Rio Cachoeira, pela infância em Itabuna e pela identidade da região cacaueira.",
        "obras": [
            "Nada Era Melhor",
            "O Velho e o Velho Rio",
            "Devoto do Campo",
            "Infância com Bicho e Pesadelo",
            "Histórias do Mundo que se Foi",
        ],
        "resumo_obras": "Em 'Nada Era Melhor', romance de formação ambientado nas ruas e quintais de Itabuna, o autor resgata as vivências, angústias e descobertas de um menino grapiúna à beira do Rio Cachoeira durante a era de ouro do cacau.",
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Cyro_de_Mattos.jpg/600px-Cyro_de_Mattos.jpg",
    },
    {
        "nome_autor": "Adonias Filho",
        "historia": "Nascido na região cacaueira do Sul da Bahia, Adonias Aguiar Filho (1915–1990) foi um dos mais expressivos romancistas e críticos literários do Brasil, ocupante da Cadeira 21 da Academia Brasileira de Letras. Ao lado de Jorge Amado, transformou o Sul da Bahia em cenário universal, imortalizando os dramas humanos, os coronéis e a terra grapiúna com uma linguagem poética e visceral.",
        "obras": [
            "Corpo Vivo",
            "Memórias de Lázaro",
            "Os Servos da Morte",
            "O Forte",
            "Léguas da Promissão",
        ],
        "resumo_obras": "'Corpo Vivo' (1962) acompanha a jornada de vingança e sobrevivência de Cajango pelas roças de cacau e sertões grapiúnas após a destruição de sua família, tornando-se um clássico da literatura sul-baiana.",
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Adonias_Filho.jpg/600px-Adonias_Filho.jpg",
    },
]


def popular():
    db = SessionLocal()
    try:
        for dados in AUTORES:
            existente = (
                db.query(Autor).filter(Autor.nome_autor == dados["nome_autor"]).first()
            )
            if not existente:
                novo_autor = Autor(**dados)
                db.add(novo_autor)
                print(f"Autor '{dados['nome_autor']}' adicionado com sucesso!")
            else:
                print(f"Autor '{dados['nome_autor']}' já está cadastrado.")

        db.commit()
        print("Banco populado com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro ao popular o banco: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    popular()
