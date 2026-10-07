from database.infraestruturadb import SessionLocal
from database.models import Autor

# Cole aqui os links das fotos que você escolheu na web
NOVAS_FOTOS = {
    "Cyro de Mattos": "https://th.bing.com/th/id/OIP.febB9RAU_KREvDpvPiRC_gHaJX?w=196&h=248&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",
    "Adonias Filho": "https://upload.wikimedia.org/wikipedia/commons/5/56/Adonias_Filho.jpg",
}


def atualizar_fotos_banco():
    db = SessionLocal()
    try:
        for nome_autor, url_foto in NOVAS_FOTOS.items():
            autor = db.query(Autor).filter(Autor.nome_autor == nome_autor).first()
            if autor:
                autor.foto_url = url_foto
                print(f"✅ URL de '{nome_autor}' atualizada!")
            else:
                print(f"⚠️ Autor '{nome_autor}' não encontrado no banco.")

        db.commit()  # Salva as alterações no Neon
        print("\n✨ Commit realizado com sucesso no banco de dados!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao atualizar o banco: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    atualizar_fotos_banco()
