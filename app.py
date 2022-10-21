from flask import Flask, flash
import psycopg2
from flask import render_template, request, redirect

conexion = psycopg2.connect(host="localhost", database="consultas", user="postgres", password="postgres")
cursor = conexion.cursor()

app = Flask(__name__)

@app.route('/')
def index():

    sql = "SELECT idCita, nombre, apellido, cedula, correo, fecha, nombreDoctor, Especialidad FROM citas " \
        "INNER JOIN pacientes " \
        "ON citas.pacienteId = pacientes.id " \
        "INNER JOIN doctores " \
        "ON citas.doctorId = doctores.id;" 

    cursor.execute(sql)

    citas = cursor.fetchall()

    return render_template('consultas/index.html', citas=citas)


@app.route('/create')
def create():

    cursor.execute("SELECT * FROM doctores;")
    doctores = cursor.fetchall()

    return render_template('/consultas/create.html', doctores=doctores)

@app.route('/store', methods = ["POST"])
def storage():
    nombre = request.form["txtNombre"]
    apellido = request.form["txtApellido"]
    cedula = request.form["txtCedula"]
    correo = request.form["txtCorreo"]
    doctorId = int(request.form["txtDoctor"])
    fecha = request.form["txtFecha"]

    paciente = (nombre, apellido, cedula, correo)

    sqlPaciente = "INSERT INTO pacientes " \
    "(nombre, apellido, cedula, correo) " \
    "VALUES (%s, %s, %s, %s);"

    sqlCita = "INSERT INTO citas " \
    "(pacienteId, doctorId, fecha) " \
    "VALUES (%s, %s, %s);"

    # TODO: verificar si ya el paciente existe en la tabla
    if True:
        cursor.execute(sqlPaciente, paciente)
        conexion.commit()

    # obtener ultimo id insertado en la tabla pacientes
    cursor.execute("SELECT MAX(id) FROM pacientes;")
    pacienteId = cursor.fetchone()
    print(pacienteId )
    
    cursor.execute(sqlCita, (pacienteId, doctorId, fecha))
    conexion.commit()

    return redirect("/")

@app.route("/destroy/<int:id>")
def destroy(id):
    cursor.execute("DELETE FROM citas WHERE idCita = %s;", [id])
    conexion.commit()

    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):

    sql = "SELECT idCita, nombre, apellido, cedula, correo, fecha, nombreDoctor, Especialidad FROM citas " \
        "INNER JOIN pacientes " \
        "ON citas.pacienteId = pacientes.id " \
        "INNER JOIN doctores " \
        "ON citas.doctorId = doctores.id " \
        "WHERE idCita = %s;"

    cursor.execute(sql, [id])
    cita = cursor.fetchall()

    cursor.execute("SELECT * FROM doctores;")
    doctores = cursor.fetchall()

    return render_template("/consultas/edit.html", cita=cita, doctores=doctores)

@app.route("/update", methods = ["POST"])
def update():
    nuevoDoctor = int(request.form["txtDoctor"])
    nuevaFecha = request.form["txtFecha"]
    idCita = request.form["txtId"]

    sqlCita = "UPDATE citas SET fecha = %s, doctorId = %s WHERE idCita = %s;"

    cursor.execute(sqlCita, (nuevaFecha, nuevoDoctor, idCita))
    
    conexion.commit()
    
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True)