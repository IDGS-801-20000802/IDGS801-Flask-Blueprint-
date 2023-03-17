from flask import Blueprint

alumnos=Blueprint('maestros',__name__)

@alumnos.route('/getmaes', methods=['GET'])
def getalum():
    return {'key':'Maestros'}

