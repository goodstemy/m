
from flask import Flask, send_from_directory
from getproxy import main as getProxy

app = Flask(__name__)

@app.route('/')
def main():
    # proxy = getProxy()

    return send_from_directory('.', 'raw-proxy.txt')

# t = threading.Timer(86400, getProxy(), )