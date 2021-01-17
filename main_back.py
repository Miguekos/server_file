from flask import Flask, request, send_from_directory, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_cors import CORS
import os
import datetime
from controllers.mongo import MongoConect

UPLOAD_FOLDER = './uploads/2021/01/10/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "super secret key"

print(os.getcwd())
# app.config['STATIC'] = './uploads/2021/01/10/'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This is necessary because QUploader uses an AJAX request
# to send the file
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})







def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/filestest/<filename>')
def uploaded_file_static_test(filename):
    # insertarMongo = MongoConect(filename)
    # result = insertarMongo.BuscarFile()
    # print("result: {}{}".format(result['ruta'], result['nombre']))
    print("filename: ", app.config['STATIC'], filename)
    return send_from_directory("{}".format(app.config['STATIC']), "{}".format(filename))
    # return send_file("uploads/2020/12/30/eshoponcontainers-reference-application-architecture.png", as_attachment=True)


# @app.route('/api/upload', methods=['POST', 'GET'])
# def uploaded_file_static():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return "asd"
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))


@app.route('/api/upload', methods=['POST'])
def upload():
    global result
    result = "Error Controlado"
    for fname in request.files:
        # print(fname)
        f = request.files.get(fname)
        # f.filename.split('.')[1]
        # print(f.filename.split('.')[1])
        print(f)
        print("Peso: ", len(f.read()))
        ext = f.filename.split('.')[1]
        nombre = secure_filename(fname)
        date = datetime.datetime.now()
        print(nombre)
        print(date)
        # ruta = "./uploads/{}/{}/{}/{}".format(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"),
        #                                       nombre)
        # f.save(ruta)
        # insertarMongo = MongoConect({
        #     "nombre": nombre,
        #     "ext": ".{}".format(ext),
        #     "peso": len(f.read()),
        #     "ruta": "./uploads/{}/{}/{}/".format(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"))
        # })
        # result = insertarMongo.InsertarFile()
        # result = "{}.{}".format(result, ext)
    return result


if __name__ == '__main__':
    date = datetime.datetime.now()
    ruta = "./uploads/{}/{}/{}".format(date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"))
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    app.run(host="0.0.0.0", port=4343, debug=True)

# import StringIO
#
# output = StringIO.StringIO()
# output.write('First line.\n')
# print >>output, 'Second line.'
#
# # Retrieve file contents -- this will be
# # 'First line.\nSecond line.\n'
# contents = output.getvalue()
#
# # Close object and discard memory buffer --
# # .getvalue() will now raise an exception.
# output.close()
