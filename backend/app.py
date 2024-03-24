from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def info():
    return 'Server is Running on port ' + os.getenv('APP_PORT') 

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('APP_PORT'))