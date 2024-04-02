import sqlite3
class Mentorado:
    def __init__(self, nome: str, linkedin: str, id=None):
        self.id = id
        self.nome = nome
        self.linkedin = linkedin

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "linkedin": self.linkedin
        }

    def save(self, db_connection: sqlite3.Connection):
        if self.id is None:
            query = "INSERT INTO mentorados(nome_mentorado,linkedin_mentorado) VALUES (?, ?)"
            cursor = db_connection.execute(query, (self.nome, self.linkedin))
            self.id = cursor.lastrowid
        else:
            query = "UPDATE mentorados SET nome_mentorado = ?, linkedin_mentorado = ? WHERE id_mentorado = ?"
            db_connection.execute(query, (self.nome, self.linkedin, self.id))
        db_connection.commit()

    def delete(self, db_connection: sqlite3.Connection):
        query = "DELETE FROM mentorados WHERE id_mentorado = ?"
        db_connection.execute(query, (self.id,))
        db_connection.commit()

    @staticmethod
    def get_by_id(id: int, db_connection: sqlite3.Connection):
        query = "SELECT * FROM mentorados WHERE id_mentorado = ?"
        cursor = db_connection.cursor()
        result = cursor.execute(query, (id,)).fetchone()
        if result:
            return Mentorado(id=result[0], nome=result[1], linkedin=result[2])
        else:
            return None

    @staticmethod
    def get_all(db_connection: sqlite3.Connection):
        query = "SELECT * FROM mentorados"
        cursor = db_connection.cursor()
        results = cursor.execute(query).fetchall()
        mentorado = []
        for result in results:
            mentorado.append(Mentorado(id=result[0], nome=result[1], linkedin=result[2]).to_dict())
        return mentorado
