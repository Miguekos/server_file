from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import datetime
import uuid
from controllers.mongo import MongoConect

app = Flask(__name__)

# This is necessary because QUploader uses an AJAX request
# to send the file
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})


@app.route('/files/<filename>')
def uploaded_file_static_test(filename):
    name = filename.split('.')[0]
    insertarMongo = MongoConect(name)
    result = insertarMongo.BuscarFile()
    print(result)
    print("result: {}{}{}".format(result['ruta'], result['idRegistro'], result['ext']))

    # print("filename: ", app.config['STATIC'], filename)
    return send_from_directory("{}".format(result['ruta']), "{}{}".format(result['idRegistro'], result['ext']))


@app.route('/api/upload', methods=['POST', "OPTIONS"])
def upload():
    try:
        # creando carpeta de la ruta si no existe
        date = datetime.datetime.now()
        ruta = "./uploads/{}/{}/{}".format(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"))
        if not os.path.exists(ruta):
            os.makedirs(ruta)

        # Inicia la logica
        global result
        result = "Error Controlado"
        for fname in request.files:
            f = request.files.get(fname)
            import uuid
            idregistro = "{}".format(uuid.uuid4())
            print("Archivo F:",f)
            print("Archivo F:", type(f))
            print("Archivo fname:", fname)
            print("Archivo fname:", type(fname))

            # print("secure_filename", secure_filename(fname))

            date = datetime.datetime.now()
            peso = len(f.read())
            print("Peso: ", peso)
            ruta = "./uploads/{}/{}/{}/{}".format(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"),
                                                  idregistro)
            print("ruta: {}".format(ruta))
            # print("{}".format(secure_filename(f)))
            f.save('{}.{}'.format(ruta, secure_filename(fname).split('.')[1]))

            date = datetime.datetime.now()
            ext = f.filename.split('.')[1]
            nombre = secure_filename(fname)

            print(nombre)
            print(date)

            insertarMongo = MongoConect({
                "idRegistro": idregistro,
                "nombre": nombre,
                "ext": ".{}".format(ext),
                "peso": peso,
                "ruta": "./uploads/{}/{}/{}/".format(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"))
            })
            result = insertarMongo.InsertarFile()
            print("result", result)
            if result:
                print(result)
                result = {
                    "name" : "{}.{}".format(idregistro, ext)
                }
            else:
                result = "{}".format("Error controlado")

            # f.save('./uploads/%s' % secure_filename(fname))

        return result
    except NameError:
        print(NameError)


if __name__ == '__main__':
    app.run(port=4444, debug=True)
