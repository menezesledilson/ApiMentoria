from mentor import Mentor
from mentorando import Mentorando
import sqlite3

class Mentoria:
    def __init__(self, mentor: Mentor, mentorando: Mentorando, data: str, id_=None):
        self.id = id_
        self.mentor = mentor 
        self.mentorando = mentorando
        self.data = data
        
    def to_dict(self):
        mentor_dict = self.mentor.to_dict() if self.mentor else None
        mentorando_dict = self.mentorando.to_dict() if self.mentorando else None
        
        return {
            "id": self.id,
            "mentor": mentor_dict,
            "mentorando": mentorando_dict,
            "data": self.data
        }
    
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
                mentorando = Mentorando.get_by_id(result[2], db) 
                return Mentoria(id_=result[0], mentor=mentor, mentorando=mentorando, data=result[3])           
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
                mentorando = Mentorando.get_by_id(result[2], db)
                mentorias.append(Mentoria(id_=result[0], mentor=mentor, mentorando=mentorando, data=result[3]).to_dict())
            return mentorias