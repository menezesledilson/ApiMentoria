import sqlite3

class Mentor:
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
            query = "INSERT INTO mentores(nome_mentor,linkedin_mentor) VALUES (?, ?)"
            cursor = db_connection.execute(query, (self.nome, self.linkedin))
            self.id = cursor.lastrowid
        else:
            query = "UPDATE mentores SET nome_mentor = ?, linkedin_mentor = ? WHERE id_mentor = ?"
            db_connection.execute(query, (self.nome, self.linkedin, self.id))
        db_connection.commit()
    
    def delete(self, db_connection: sqlite3.Connection):
        query = "DELETE FROM mentores WHERE id_mentor = ?"
        db_connection.execute(query, (self.id,))
        db_connection.commit()

        
    @staticmethod
    def get_by_id(id: int, db_connection: sqlite3.Connection):
        query = "SELECT * FROM mentores WHERE id_mentor = ?"
        cursor = db_connection.cursor()
        result = cursor.execute(query, (id,)).fetchone()
        if result:
            return Mentor(id=result[0], nome=result[1], linkedin=result[2])
        else:
            return None

    @staticmethod
    def get_all(db_connection: sqlite3.Connection):
        query = "SELECT * FROM mentores"
        cursor = db_connection.cursor()
        results = cursor.execute(query).fetchall()
        mentors = []
        for result in results:
            mentors.append(Mentor(id=result[0], nome=result[1], linkedin=result[2]).to_dict())
        return mentors
