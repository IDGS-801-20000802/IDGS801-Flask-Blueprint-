from flask import Blueprint, render_template, redirect, url_for, request, flash
from db import get_connection
from models import db
from models import Maestros
import forms

maestros= Blueprint('maestros', __name__)


@maestros.route("/insertarMaestro",methods=['GET', 'POST'])
def index():
    create_form=forms.UserForm2(request.form)
    if request.method == 'POST':
        nombre = create_form.nombre.data
        apellidos = create_form.apellidos.data
        correo = create_form.correo.data
        nomMateria = create_form.nomMateria.data
        
        try:
           connection=get_connection()
           with connection.cursor() as cursor:
                cursor.execute('call sp_InsertarMaestro(%s,%s,%s,%s)', (nombre, apellidos, correo, nomMateria))
           connection.commit()
           connection.close()

        except Exception as ex:
            print('ERROR {}'.format(ex))

        return redirect(url_for('maestros.ABCompleto'))
    
    return render_template('Maestros.html',form=create_form)
    

@maestros.route("/modificar2",methods=['GET','POST'])
def modificar():
    create_fprm=forms.UserForm2(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        connection = get_connection()
        try:
           with connection.cursor() as cursor:
               cursor.execute('CALL sp_ObtenerMaestroPorId(%s)',(id))
               resultset = cursor.fetchall()
           create_fprm.id.data=request.args.get('id')
           create_fprm.nombre.data=resultset[0][1]
           create_fprm.apellidos.data=resultset[0][2]
           create_fprm.correo.data=resultset[0][3]
           create_fprm.nomMateria.data=resultset[0][4]        
            
        except Exception as ex:
           print(ex)
        finally:
           connection.close()

    if request.method=='POST':
        id=create_fprm.id.data
        nombre = create_fprm.nombre.data
        apellidos = create_fprm.apellidos.data
        correo = create_fprm.correo.data
        nomMateria = create_fprm.nomMateria.data
        
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL sp_ModificarMaestro(%s,%s,%s,%s,%s)', (id, nombre, apellidos, correo, nomMateria))
            connection.commit()
            connection.close()

        except Exception as ex:
           print('ERROR {}'.format(ex))
        return redirect(url_for('maestros.ABCompleto'))
    return render_template('Modificar2.html', form= create_fprm)


@maestros.route("/eliminar2",methods=['GET','POST'])
def eliminar():
    create_fprm=forms.UserForm2(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        connection = get_connection()
        try:
           with connection.cursor() as cursor:
               cursor.execute('CALL sp_ObtenerMaestroPorId(%s)',(id))
               resultset = cursor.fetchall()
           create_fprm.id.data=request.args.get('id')
           create_fprm.nombre.data=resultset[0][1]
           create_fprm.apellidos.data=resultset[0][2]
           create_fprm.correo.data=resultset[0][3]
           create_fprm.nomMateria.data=resultset[0][4]          
            
        except Exception as ex:
           print(ex)
        finally:
           connection.close()
    if request.method=='POST':
        id=create_fprm.id.data
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL sp_EliminarMaestro(%s)', (id))
            connection.commit()
            connection.close()

        except Exception as ex:
           print('ERROR {}'.format(ex))
        return redirect(url_for('maestros.ABCompleto'))
    return render_template('Eliminar2.html', form= create_fprm)


@maestros.route("/ABCompleto2",methods=["GET","POST"])
def ABCompleto():
    create_form=forms.UserForm2(request.form)
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('call sp_ObtenerTodosMaestros()')
            resultset = cursor.fetchall()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()
    print (resultset)
    return render_template("ABCompleto2.html", form=create_form, resultset=resultset)

