from flask import Flask, request, jsonify
from datetime import datetime
from mentor import Mentor
from mentorando import Mentorando
from mentoria import Mentoria
from db_connector import DBConnector


app = Flask(__name__)

db = DBConnector("mentorias.db")

# Métodos CRUD  

#RETORNA TODOS OS MENTORES

@app.route('/mentors', methods=['GET'])
def get_all_mentors():
    mentors = Mentor.get_all(db.connect())
    return jsonify(mentors)

#RETORNA TODOS OS MENTORANDOS

@app.route('/mentorandos', methods=['GET'])
def get_all_mentorandos():
    mentorandos = Mentorando.get_all(db.connect())
    return jsonify(mentorandos)

#RETORNA TODAS AS MENTORIAS

@app.route('/mentorias', methods=['GET'])
def get_all_mentorias():
    mentorias = Mentoria.get_all(db.connect())
    return jsonify(mentorias)

#RETORNA POR ID MENTOR

@app.route('/mentors/<int:id_mentors>', methods=['GET'])
def get_mentor(id_mentors):
    mentor = Mentor.get_by_id(id_mentors, db.connect())
    if mentor:
        return jsonify(mentor.to_dict())
    else:
        return jsonify({'error': 'Mentor not found'}), 404

#RETORNA POR ID MENTORANDO

@app.route('/mentorandos/<int:id>', methods=['GET'])
def get_mentorando(id):
    mentorando = Mentorando.get_by_id(id, db.connect())
    if mentorando:
        return jsonify(mentorando.to_dict())
    else:
        return jsonify({'error': 'Mentorando not found'}), 404

#RETORNA POR ID MENTORIA

@app.route('/mentorias/<int:id_mentoria>', methods=['GET'])
def get_mentoria(id_mentoria):
    mentoria = Mentoria.get_by_id(id_mentoria, db.connect())
    if mentoria:
        return jsonify(mentoria.to_dict())
    else:
        return jsonify({'error': 'Mentoria not found'}), 404
    
#CRIAR MENTOR

@app.route('/mentors', methods=['POST'])
def create_mentor():
    data = request.get_json()
    mentor = Mentor(data['nome'], data['linkedin'])
    mentor.save(db.connect())
    return jsonify(mentor.to_dict()), 201

#CRIAR MENTORANDO

@app.route('/mentorandos', methods=['POST'])
def create_mentorando():
    data = request.get_json()
    mentorando = Mentorando(data['nome'], data['linkedin'])
    mentorando.save(db.connect())
    return jsonify(mentorando.to_dict()), 201

#CRIAR MENTORIA    

@app.route('/mentorias', methods=['POST'])
def create_mentoria():
    data = request.get_json()
    mentor = Mentor.get_by_id(data['id_mentor'], db.connect())
    mentorando = Mentorando.get_by_id(data ['mentorando_id'], db.connect())
    data_mentoria = datetime.fromisoformat(data["data_mentoria"])
    mentoria = Mentoria(mentor=mentor,mentorando=mentorando,data=data_mentoria)  
    mentoria.save(db.connect())
    return jsonify(mentoria.to_dict()), 201
   
#ATUALIZAR MENTOR

@app.route('/mentors/<int:id>', methods=['PUT'])
def update_mentor(id):
    data = request.get_json()
    mentor = Mentor.get_by_id(id, db.connect())
    if mentor:
        mentor.nome = data['nome']
        mentor.linkedin = data['linkedin']
        mentor.save(db.connect())
        return jsonify(mentor.to_dict())
    else:
        return jsonify({'error': 'Mentor not found'}), 404
    
#ATUALIZAR MENTORANDO

@app.route('/mentorandos/<int:id>', methods=['PUT'])
def update_mentorando(id):
    data = request.get_json()
    mentorando = Mentorando.get_by_id(id, db.connect())
    if mentorando:
        mentorando.nome = data['nome']
        mentorando.linkedin = data['linkedin']
        mentorando.save(db.connect())
        return jsonify(mentorando.to_dict())
    else:
        return jsonify({'error': 'Mentorando not found'}), 404

#ATUALIZAR MENTORIA

@app.route('/mentorias/<int:id_mentoria>', methods=['PUT'])
def update_mentoria(id_mentoria):
    data = request.get_json()
    mentoria = Mentoria.get_by_id(id_mentoria, db.connect())   
    if mentoria:
        mentor = Mentor.get_by_id(data['id_mentor'],db.connect())
        mentorando =Mentorando.get_by_id(data['id_mentorando'],db.connect())
        data_mentoria= datetime.fromisoformat(data['data'])
        mentoria.mentor = mentor
        mentoria.mentorando = mentorando
        mentoria.data= data_mentoria
                
        mentoria.save(db.connect())
        return jsonify(mentoria.to_dict())
    else:
        return jsonify({'error': 'Mentoria not found'}), 404
    
#REMOVER MENTOR

@app.route('/mentors/<int:id>', methods=['DELETE'])
def delete_mentor(id):
    mentor = Mentor.get_by_id(id, db.connect())
    if mentor:
        mentor.delete(db.connect())
        return jsonify({'message': 'Mentor deleted successfully'}),204
    else:
        return jsonify({'error': 'Mentor not found'}), 404

#REMOVER MENTORANDO

@app.route('/mentorandos/<int:id>', methods=['DELETE'])
def delete_mentorando(id):
    mentorando = Mentorando.get_by_id(id, db.connect())
    if mentorando:
        mentorando.delete(db.connect())
        return jsonify({'message': 'Mentorando deleted successfully'}),204
    else:
        return jsonify({'error': 'Mentorando not found'}), 404
    
#REMOVER MENTORIA   

@app.route('/mentorias/<int:id>', methods=['DELETE'])
def delete_mentoria(id):
    mentoria = Mentoria.get_by_id(id, db.connect())
    if mentoria:
        mentoria.delete(db.connect())
        return jsonify({'message': 'Mentoria deleted successfully'}),204
    else:
        return jsonify({'error': 'Mentoria not found'}), 404

  
if __name__ == '__main__':
    app.run(debug=True)
