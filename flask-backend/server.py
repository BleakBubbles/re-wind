from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# members API
@app.route("/receive", methods=['post'])
def form():
    files = request.files
    file = files.get('file')
    print(file)

    with open(os.path.abspath(f'backend/audios/{file}'), 'wb') as f:
        f.write(file.content)

    response = jsonify("File received and saved!")
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    app.run(debug=True)