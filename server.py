import ipaddress, requests, json
from flask import Flask, request, abort

app = Flask(__name__)
"""
def load_aws_all() -> list[ipaddress.IPv4Network]:
    url  = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    data = requests.get(url, timeout=5).json()
    return [ipaddress.ip_network(p["ip_prefix"])
            for p in data["prefixes"] if "ip_prefix" in p]

def load_google_all() -> list[ipaddress.IPv4Network]:
    nets = []
    for url in (
        "https://www.gstatic.com/ipranges/cloud.json",
        "https://www.gstatic.com/ipranges/goog.json"
    ):
        data = requests.get(url, timeout=5).json()
        nets += [ipaddress.ip_network(p["ipv4Prefix"])
                 for p in data["prefixes"] if "ipv4Prefix" in p]
    return nets

BLOCK_NETS: list[ipaddress.IPv4Network] = (
    load_aws_all()
    +load_google_all()
    +[ipaddress.ip_network("207.241.224.0/20")]
)
"""
BLOCK_NETS = [
    ipaddress.ip_network("207.241.224.0/20")
]

@app.before_request
def block_netname_ranges():
    ua = request.headers.get('User-Agent', '')
    if "ChatGPT" in ua:
        abort(404)
    if "virustotalcloud" in ua:
        abort(404)
    
    ip_str = (request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
              or request.remote_addr)
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        abort(404)

    if any(ip_obj in net for net in BLOCK_NETS):
        abort(404)


        
METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE']

#@app.route('/', defaults={'path': ''}, methods = METHODS)
#@app.route('/<path:path>', methods=METHODS)
@app.route('/about', methods=METHODS)
def index(path):
    print('headers', request.headers)

    return f'''
    <h1>Path: /{path}</h1>
    <h2>Method: {request.method}</h2>
    <h2>Request headers</h2>
    <ul>
    {''.join((f'<li>{name}: {value}</li>' for name, value in request.headers))}
    </ul>
    <h2>Request body</h2>
    <p>{request.get_data().decode() if request.get_data() else 'None.'}</p>
    '''

if __name__ == '__main__':
    app.run(port=8000)
