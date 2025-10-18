from flask import Flask
import keyboard

app = Flask(__name__)

@app.route('/hold/down')
def home():
    keyboard.press("down")
    return "200"

@app.route('/release/down')
def release():
    keyboard.release("down")
    return "200"

@app.route('/hold/space')
def hold_space():
    keyboard.press_and_release("space")
    return "200"

if __name__ == '__main__':
    app.run(debug=True, port=3000, host="0.0.0.0")