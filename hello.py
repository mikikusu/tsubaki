import os
import glob

from flask import Flask, request, send_file
app = Flask(__name__)

DATA_DIR = os.environ.get('DATA_DIR', '.')

@app.route('/')
def index():
    body = """
    <html>
    <head><style type="text/css">
        input[type="text"] {
            width: 100%;
            padding: 10px 15px;
            font-size: 14px;
            font-size: 1.4rem;
            border: 1px solid #ccc;
            -webkit-border-radius: 4px;
            -moz-border-radius: 4px;
            -ms-border-radius: 4px;
            border-radius: 4px;
        }
        label {
            background: #b0c4de;
            color: #191970;
            cursor: pointer;
            padding: 15px 30px;
            margin: 0 10px 0 0;
            display: inline-block;
        }
        label input {
            display: none;
        }
        input[type="submit"] {
          -webkit-appearance: none;
          width:100%;
          height: 50px;
          background: #70c1ff；
          font-size: 14px;
          font-size: 1.4rem;
          border-radius: 10px;
          box-shadow: 3px 3px 3px gray;
        }
    </style></head>
    <body>
        <h2>りんご組さん動画アップロード</h2>
        <div><form method="POST" action="upfile" enctype="multipart/form-data">
        <p><input type="text" name="idName" placeholder="お子様のお名前（例：ともな）"><p>
        <p><label for="sample1">ファイルを選択<input type="file" name="idFile" id="sample1"></label><p>
        <p><input type="submit" value="送信する" class="btn-square-little-rich"><p>
        </form></div>
    </body></html>
    """
    return body

@app.route('/upfile', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        name = request.form['idName']
        f = request.files['idFile']
        if name == '':
            return '名前を入力してください。<br><a href="/">戻る</a>'
        elif f.filename == "":
            return 'ファイルを選択してください。<br><a href="/">戻る</a>'
        f.save(DATA_DIR + '/' + name + '_' + f.filename)
        body = 'ファイルをアップロードしました。<br>別のファイルは<a href="/">こちら</a>から。<br>'
        body += DATA_DIR + '/' + name + '_' + f.filename
        return body
    else:
        return "Fileをアップロードしてください"

@app.route('/filelist', methods=["GET"])
def file_list():
    f_list = glob.glob(DATA_DIR + "/*")
    body = '<html><body>'
    body += '<h2>りんご組さん動画一覧</h2>'
    body += '<ul>'
    for f_name in f_list:
        if f_name == "./hello.py":
            continue
        body += '<li><a href="/dl/' + f_name + '">' + f_name + '</a></li>'
    body += '</ul>'
    body += '</body><html>'

    return body

@app.route('/dl/<string:file_name>', methods=['GET'])
def file_download(file_name):
    f_path = DATA_DIR + '/' + file_name

    return send_file(f_path, as_attachment=True, attachment_filename=file_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0')