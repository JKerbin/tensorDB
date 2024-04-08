from flask import Flask, request, jsonify
from scripts.database import Mysql
from gevent import pywsgi

app = Flask(__name__)


@app.route('/get_tensors', methods=['GET'])
def get_tensors():
    start_index = request.args.get('start_index', default=0, type=int)
    end_index = request.args.get('end_index', default=-1, type=int)
    user = request.args.get('user')
    pw = request.args.get('pw')
    db_name = request.args.get('db_name')
    tb_name = request.args.get('tb_name')
    db_host = request.args.get('host', default='localhost', type=str)
    db_port = request.args.get('port', default=3306, type=int)
    mysql_instance = Mysql(user=user, pw=pw, db_name=db_name, tb_name=tb_name, host=db_host, port=db_port)
    tensors = mysql_instance.get_tensors_by_ind(start_index=start_index, end_index=end_index)
    return jsonify({'tensors': tensors.tolist()})


@app.route('/get_texts', methods=['GET'])
def get_texts():
    start_index = request.args.get('start_index', default=0, type=int)
    end_index = request.args.get('end_index', default=-1, type=int)
    user = request.args.get('user')
    pw = request.args.get('pw')
    db_name = request.args.get('db_name')
    tb_name = request.args.get('tb_name')
    db_host = request.args.get('host', default='localhost', type=str)
    db_port = request.args.get('port', default=3306, type=int)
    mysql_instance = Mysql(user=user, pw=pw, db_name=db_name, tb_name=tb_name, host=db_host, port=db_port)
    texts = mysql_instance.get_texts_by_ind(start_index=start_index, end_index=end_index)
    return jsonify({'texts': texts})


@app.route('/add_pdf', methods=['POST'])
def add_pdf():
    data = request.get_json()
    url = data['url']
    user = data.get('user')
    pw = data.get('pw')
    db_name = data.get('db_name')
    tb_name = data.get('tb_name')
    db_host = request.args.get('host', default='localhost', type=str)
    db_port = request.args.get('port', default=3306, type=int)
    mysql_instance = Mysql(user=user, pw=pw, db_name=db_name, tb_name=tb_name, host=db_host, port=db_port)
    mysql_instance.add_pdf(url)
    return jsonify({'message': 'PDF added successfully.'})


if __name__ == '__main__':
    port = 8080
    print('Running on http://127.0.0.1:' + str(port))
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()
