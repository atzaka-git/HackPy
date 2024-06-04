from flask import Flask, request

app = Flask(__name__)

# Route to receive text and save it to a file
@app.route('/submit', methods=['POST'])
def submit_text():
    text = request.get_data().decode("utf-8")

    with open("saved_text.txt", "a") as file:
        file.write(text + "\n")

    return "Text submitted: " + text + "\n", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)
