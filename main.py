from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import datetime
import uuid
from controllers.mongo import MongoConect
import sys
from pathlib import Path  # python3 only
from dotenv import load_dotenv  # pip install python-dotenv

app = Flask(__name__)

# This is necessary because QUploader uses an AJAX request
# to send the file
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})


@app.route('/api/server/fileslist')
def list_files():
    try:
        insertarMongo = MongoConect(None)
        result = insertarMongo.BuscarFileAll()
        print("result", result)
        # print("filename: ", app.config['STATIC'], filename)
        return {
            "result": result
        }
    except NameError:
        print(NameError)
        return "error controlado"


@app.route('/api/server/files/<filename>')
def uploaded_file_static_test(filename):
    try:
        name = filename.split('.')[0]
        insertarMongo = MongoConect(name)
        result = insertarMongo.BuscarFile()
        print(result)
        print("result: {}{}{}".format(result['ruta'], result['idRegistro'], result['ext']))

        # print("filename: ", app.config['STATIC'], filename)
        return send_from_directory("{}".format(result['ruta']), "{}{}".format(result['idRegistro'], result['ext']))
    except:
        return "error controlado"


@app.route('/api/server/upload', methods=['POST', "OPTIONS"])
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
            print("Archivo F:", f)
            print("Archivo F:", type(f))
            print("Archivo fname:", fname)
            print("Archivo fname:", type(fname))

            # print("secure_filename", secure_filename(fname))

            date = datetime.datetime.now()
            ruta = "./uploads/{}/{}/{}/{}".format(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"),
                                                  idregistro)
            print("ruta: {}".format(ruta))

            # print("{}".format(secure_filename(f)))
            f.save('{}.{}'.format(ruta, secure_filename(fname).split('.')[1]))
            g = request.files.get(fname)
            peso = len(g.read())
            print("Peso: ", f)
            print("Peso: ", peso)

            date = datetime.datetime.now()
            ext = f.filename.split('.')[-1]
            print("ext", ext)
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
                    "name": "{}.{}".format(idregistro, ext)
                }
            else:
                result = "{}".format("Error controlado")

            # f.save('./uploads/%s' % secure_filename(fname))

        return result
    except:
        return "error controlado"


try:
    enviro = sys.argv[1]
    if enviro == "pro":
        env_path = Path('.') / '.env.pro'
        load_dotenv(dotenv_path=env_path)
        print(os.getenv('ENVIRO'))
        print("APP ENV: PRODUCCION")
    deb = os.getenv("DEBUG")
    if __name__ == '__main__':
        # app.run()
        app.run(host='0.0.0.0', port=os.getenv("PORT"), debug=False if deb=="False" else True)

except:
    env_path = Path('.') / '.env.dev'
    load_dotenv(dotenv_path=env_path)
    print(os.getenv('ENVIRO'))
    print("APP ENV: DESARROLLO")
    deb = os.getenv("DEBUG")
    if __name__ == '__main__':
        # app.run()
        app.run(host='0.0.0.0', port=os.getenv("PORT"), debug=False if deb=="False" else True)
