from flask import Flask, send_file, request
import datetime
import hashlib
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'BIMBaseAdServer ON'


@app.route('/down')
def download_file():
    return send_file('BIMBaseAdConfig.xml', as_attachment=True)


@app.route('/up')
def upload_file():
    date_object = datetime.date.today()
    md5 = hashlib.md5()
    md5.update(str(date_object).encode('utf-8'))
    calculate_md5 = md5.hexdigest()
    request_md5 = request.headers.get("Authorization")
    if request_md5 != calculate_md5:
        return "error"
    f = request.files['file']
    print(request.files)
    f.save("BIMBaseAdConfig.xml")
    return "success"


if __name__ == '__main__':
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0', 5001), app)
    server.serve_forever()
