#indicamos framework que vamos utilizar
from flask import Flask,request,render_template,redirect,url_for,session,jsonify
import os
import json
from pymongo import MongoClient
from bson import ObjectId 

#variables de la conexion en mongo
client = MongoClient("mongodb+srv://lyn11:pollitoM.1811@cluster0.gjcgava.mongodb.net/?retryWrites=true&w=majority")
db = client['registro'] 
collectionVen = db['vendedores'] 
collectionCas = db['casas'] 

#crear una instancia del constructor de la clase
app = Flask(__name__)

#creando una configuracion protegida nuestra sesion
app.secret_key = 'mysecretet'

#creacion de las rutas principales
@app.route('/')
def home():
    #busca las casas en la tabla de casas para que las muestre en la pagina 
    casas = collectionCas.find()
    return render_template('index.html',casas=casas)

#ruta de vista maquilas
@app.route('/maquiladoras',methods=['GET'])
def maquilas():
    return render_template('maquilas.html')

#ruta de vista lugares turisticos
@app.route('/lugares_turisticos',methods=['GET'])
def lugares():
    return render_template('info_cultura.html')

#ruta de vista acerca de nosotros
@app.route('/acerca_nosotros',methods=['GET'])
def nosotros():
    return render_template('blog.html')

#ruta de vista guia
@app.route('/guia',methods=['GET'])
def guia():
    return render_template('guia.html')

#ruta para el formulario de inicio de sesión
@app.route('/sesion',methods=['GET'])
def sesion():
    return render_template('ini_s.html')

#ruta de vista iniciar sesion
@app.route('/sesion/iniciar', methods=['GET', 'POST'])
def sesion_iniciar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        # Si las credenciales coinciden con el administrador
        if usuario == "admin" and contrasena == "admin123":
            # Iniciar la sesión y redirigir a la página de administración
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return redirect(url_for('vendedores_pagina'))

#ruta de la vista de las tablas de usuarios y casas
@app.route('/admin')
def index():
    #busca los usuarios y casas disponibles en su debidas tablas
    casas = collectionCas.find()
    vendedores = collectionVen.find()
    return render_template('admin.html', vendedores=vendedores, casas=casas)

#ruta para las tablas de vendedores
@app.route('/vendedores', methods=['GET'])
def vendedores_pagina():
    return render_template('vendedor.html')

#ruta para encontrar el formulario de registro de la pagina principal
@app.route('/registro')
def regis():
    return render_template('registro.html')

#ruta de vista registrarse de la pagina principal
@app.route('/registro/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoP']
        apellidoM = request.form['apellidoM']
        telefono = request.form['telefono']
        email = request.form['email']
        contrasena = request.form['contrasena']
        conf_contrasena = request.form['conf_contrasena']
        usuario = request.form['usuario']
        condiciones = 'aceptadas' if 'condiciones' in request.form else 'no aceptadas'

        #si la contraseña es igual a la contraseña de confirmacion agarra la variable vendedor para guardar sus datos
        if contrasena == conf_contrasena:
            vendedor = {
                "nombre": nombre,
                "apellidoP": apellidoP,
                "apellidoM": apellidoM,
                "telefono": telefono,
                "email": email,
                "contrasena": contrasena,
                "usuario": usuario,
                "condiciones": condiciones
            }
            
            #se inserta la informacion en la tabla de vendedores
            collectionVen.insert_one(vendedor)
            
            #me dirige al inicio de sesion automaticamente
            return redirect(url_for('sesion'))
        else:
            return "Las contraseñas no coinciden. <a href='/registro'>Volver</a>"


#ruta para encontrar el formulario de registro
@app.route('/registroVendedor')
def regisV():
    return render_template('registroVendedor.html')

#ruta de vista registrarse - vendedor
@app.route('/registro/registrarseVendedor', methods=['GET', 'POST'])
def registrarseV():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidoP = request.form['apellidoP']
        apellidoM = request.form['apellidoM']
        telefono = request.form['telefono']
        email = request.form['email']
        contrasena = request.form['contrasena']
        conf_contrasena = request.form['conf_contrasena']
        usuario = request.form['usuario']
        condiciones = 'aceptadas' if 'condiciones' in request.form else 'no aceptadas'

        #si la contraseña es igual a la contraseña de confirmacion agarra la variable vendedor para guardar sus datos
        if contrasena == conf_contrasena:
            vendedor = {
                "nombre": nombre,
                "apellidoP": apellidoP,
                "apellidoM": apellidoM,
                "telefono": telefono,
                "email": email,
                "contrasena": contrasena,
                "usuario": usuario,
                "condiciones": condiciones
            }
            
            #se inserta la informacion en la tabla de vendedores
            collectionVen.insert_one(vendedor)

            # Se dirige a la pagina de las tablas 
            return redirect('/admin')
        
        else:
            return "Las contraseñas no coinciden. <a href='/registroVendedor'>Volver</a>"

#ruta para editar un vendedor
@app.route('/editar_vendedor/<id_vendedor>', methods=['GET', 'POST'])
def editar_vendedor(id_vendedor):
    if request.method == 'POST':
        nuevo_nombre = request.form['nuevo_nombre']
        nuevo_apellidoP = request.form['nuevo_apellidoP']
        nuevo_apellidoM = request.form['nuevo_apellidoM']
        nuevo_telefono = request.form['nuevo_telefono']
        nuevo_email = request.form['nuevo_email']
        nueva_contrasena = request.form['nueva_contrasena']
        nuevo_usuario = request.form['nuevo_usuario']
        nuevas_condiciones = request.form['nuevas_condiciones']

        #actualiza la informacion de vendedores
        collectionVen.update_one({'_id': ObjectId(id_vendedor)}, {'$set': {
            'nombre': nuevo_nombre,
            'apellidoP': nuevo_apellidoP,
            'apellidoM': nuevo_apellidoM, 
            'telefono': nuevo_telefono,
            'email': nuevo_email,
            'contrasena': nueva_contrasena,
            'usuario': nuevo_usuario,
            'condiciones': nuevas_condiciones
        }})

        return redirect('/admin')

    #se obtiene el id
    vendedor = collectionVen.find_one({'_id': ObjectId(id_vendedor)})
    return render_template('vendedor-edit.html',  vendedor=vendedor)


#ruta para eliminar vendedor
@app.route('/eliminar_vendedor/<id_vendedor>', methods=['GET', 'POST'])
def eliminar_vendedor(id_vendedor):
    #se elimina el id de la tabla de vendedores
    collectionVen.delete_one({'_id': ObjectId(id_vendedor)})
    return redirect('/admin')


# Ruta del formulario para agregar casa de principal
@app.route('/agregar_casa1', methods=['GET', 'POST'])
def agregar_casa1():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre_casa']
            descripcion = request.form['descripcion']
            imagen = request.files['imagen']

            #aqui se guardan las imágenes 
            directorio_imagenes = os.path.join('static', 'IMG')

            #si el directorio no existe, se crea
            if not os.path.exists(directorio_imagenes):
                os.makedirs(directorio_imagenes)

            #aqui se guardará la imagen dentro de la carpeta static
            imagen_filename = os.path.join(directorio_imagenes, imagen.filename)
            imagen.save(imagen_filename)

            #se agrega un nuevo registro a la colección o tabla de casas en MongoDB
            nuevo_registro = {
                'nombre_casa': nombre,
                'descripcion': descripcion,
                'imagen': imagen_filename
            }

            #se inserta el nuevo registro en la tabla
            collectionCas.insert_one(nuevo_registro)

            return redirect(url_for('home'))
        
        #si algo sale mal muestra este mensaje
        except Exception as e:
            return f"Error al agregar casa: {str(e)}"

    return render_template('agregar_casa1.html')


#ruta de formulario casa - admin
@app.route('/agregar_casa', methods=['GET', 'POST'])
def agregar_casa():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre_casa']
            descripcion = request.form['descripcion']
            imagen = request.files['imagen']

            #en este directorio se guardan las imágenes
            directorio_imagenes = os.path.join('static', 'IMG')

            #si el directorio no existe, se crea
            if not os.path.exists(directorio_imagenes):
                os.makedirs(directorio_imagenes)

            #ruta en la que se guardará la imagen dentro de la carpeta static
            imagen_filename = os.path.join(directorio_imagenes, imagen.filename)
            imagen.save(imagen_filename)

            #se agrega un nuevo registro a la tabla de casas en MongoDB
            nuevo_registro = {
                'nombre_casa': nombre,
                'descripcion': descripcion,
                'imagen': imagen_filename
            }

            #inserta el nuevo registro en la colección
            collectionCas.insert_one(nuevo_registro)

            return redirect(url_for('index'))

        except Exception as e:
            return f"Error al agregar casa: {str(e)}"

    return render_template('agregar_casa.html')


@app.route('/editar_casa/<id>', methods=['GET', 'POST'])
def editar_casa(id):
    #se asegura que el ID sea valido
    if ObjectId.is_valid(id):
        #convierte el ID a ObjectId
        object_id = ObjectId(id)

        #busca la casa por ID en la base de datos mongo
        casa = collectionCas.find_one({'_id': object_id})

        if request.method == 'POST':
            try:
                casa['nombre_casa'] = request.form['nombre_casa']
                casa['descripcion'] = request.form['descripcion']

                #manejo de la imagen
                nueva_imagen = request.files['imagen']
                if nueva_imagen:
                    #ruta en la que se guardará la nueva imagen dentro de la carpeta static
                    nueva_imagen_filename = os.path.join('static', 'IMG', nueva_imagen.filename)
                    nueva_imagen.save(nueva_imagen_filename)

                    #actualiza la nueva imagen dada
                    casa['imagen'] = nueva_imagen_filename

                    #actualiza ahora en mongo
                    collectionCas.update_one({'_id': object_id}, {'$set': casa})
                    
                    # Redirige a la página de admin después de editar
                    return redirect(url_for('index')) 
                
            except Exception as e:
                return f"Error al editar casa: {str(e)}"
            
        #la informacion la saca de este formulario
        return render_template('editar_casa.html', id=id, casa=casa)

#ruta para eliminar una casa
@app.route('/eliminar_casa/<id>', methods=['GET', 'POST'])
def eliminar_casa(id):
    # elimina la casa de la tabla en MongoDB utilizando su ID
    collectionCas.delete_one({'_id': ObjectId(id)})
    return redirect('/admin')

#cierre del servidor
#validacion
if __name__ == '__main__':
    app.run(port=1000,debug=True)

