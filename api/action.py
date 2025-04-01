from flask import Flask, request
import service_file

app = Flask(__name__)

@app.route('/action', methods=['POST'])
def action():
    data = request.get_json()
    response = service_file.perform_action(data)
    return response

if __name__ == '__main__':
    app.run(debug=True)
