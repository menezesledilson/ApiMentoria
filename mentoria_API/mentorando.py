import sqlite3

class Mentorando:
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
            query = "INSERT INTO mentorando(nome_mentorando, linkedin_mentorando) VALUES (?, ?)"
            cursor = db_connection.execute(query, (self.nome, self.linkedin))
            self.id = cursor.lastrowid          
        else:        
            query = "UPDATE mentorando SET nome_mentorando = ?, linkedin_mentorando = ? WHERE id_mentorando = ?"
            db_connection.execute(query, (self.nome, self.linkedin, self.id))
            db_connection.commit()
            
    def delete(self, db_connection: sqlite3.Connection):
        if self.id is not None:
            query = "DELETE FROM mentorando WHERE id_mentorando = ?"
            db_connection.execute(query, (self.id,))
            db_connection.commit()
            self.id = None
            self.nome = None
            self.linkedin = None
        else:
            print("ID do mentorando não está definido. Não é possível excluir.")
        
    @staticmethod
    def get_by_id(id: int, db: sqlite3.Connection):
        query = "SELECT * FROM mentorando WHERE id_mentorando = ?"
        cursor = db.cursor()
        result = cursor.execute(query, (id,)).fetchone()
        if result:
            return Mentorando(id=result[0], nome=result[1], linkedin=result[2])
        else:
            return None

    @staticmethod
    def get_all(db: sqlite3.Connection):
        query = "SELECT * FROM mentorando"
        cursor = db.cursor()
        results = cursor.execute(query).fetchall()
        mentorandos = []
        for result in results:
            mentorandos.append(Mentorando(id=result[0], nome=result[1], linkedin=result[2]).to_dict())
        return mentorandos
