import mentorado
from mentor import Mentor
from mentorado import  Mentorado
import sqlite3

class Mentoria:
    def __init__(self, mentor: Mentor, mentorado: Mentorado, data_mentoria: str, id_=None):
        self.id = id_
        self.mentor = mentor
        self.mentorado = mentorado
        self.data_mentoria = data_mentoria

    def to_dict(self):
        mentor_dict = self.mentor.to_dict() if self.mentor else None
        mentorado_dict = self.mentorado.to_dict() if self.mentorado else None


        return {
            "id": self.id,
            "mentor": mentor_dict,
            "mentorado": mentorado_dict,
            "data_mentoria": self.data_mentoria
        }

    def save(self, db: sqlite3.Connection):
        if self.id is None:  # Verifica se é uma nova instância
            query = "INSERT INTO mentorias (id_mentor, id_mentorado, data_mentoria) VALUES (?, ?, ?)"
            with db:
                cursor = db.cursor()
                cursor.execute(query, (self.mentor.id, self.mentorado.id, self.data_mentoria))
                self.id = cursor.lastrowid
        else:
            # Atualizar o registro se já existir
            query = "UPDATE mentorias SET id_mentor = ?, id_mentorado = ?, data_mentoria = ? WHERE id_mentoria = ?"
            with db:
                db.execute(query, (self.mentor.id, self.mentorado.id, self.data_mentoria, self.id))

    def delete(self, db: sqlite3.Connection):
        if self.id is None:
            raise ValueError("ID da mentoria não está definido. Não é possível excluir.")
        query = "DELETE FROM mentorias WHERE id_mentorias = ?"
        with db:
            db.execute(query, (self.id,))
    
    @staticmethod
    def get_by_id(mentoria_id: int, db: sqlite3.Connection):
        query = "SELECT * FROM mentorias WHERE id_mentorias = ?"
        with db:
            cursor = db.cursor()
            result = cursor.execute(query, (mentoria_id,)).fetchone()
            if result:
                mentor = Mentor.get_by_id(result[1], db)
                mentorando = Mentorado.get_by_id(result[2], db)
                return Mentoria(id_=result[0], mentor=mentor, mentorado=mentorado, data_mentoria=result[3])
            return None

    @staticmethod
    def get_all(db: sqlite3.Connection):
        query = "SELECT * FROM mentorias"
        with db:
            cursor = db.cursor()
            cursor.execute(query)
            mentorias = []
            for result in cursor.fetchall():
                mentor = Mentor.get_by_id(result[1], db)
                mentorado = Mentorado.get_by_id(result[2], db)
                data_mentoria = result[3]  # A data é um dado de texto diretamente do banco de dados
                mentoria = Mentoria(mentor=mentor, mentorado=mentorado, data_mentoria=data_mentoria, id_=result[0])
                mentorias.append(mentoria.to_dict())
            return mentorias
