from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    ua = request.headers.get('User-Agent', '')
    print('UA: ', ua)
    if "ChatGPT" in ua:
        return "Hello, ChatGPT!"
    return "Hello, Scanner!"

if __name__ == '__main__':
    app.run(port=8000)
