import ipaddress, requests, json
from flask import Flask, request, abort

app = Flask(__name__)

BLOCK_NETS: list[ipaddress.IPv4Network] = [
    ipaddress.ip_network("207.241.224.0/20"),
    ipaddress.ip_network("5.188.6.199/32"),
    ipaddress.ip_network("5.252.55.8/32"),
    ipaddress.ip_network("23.137.253.37/32"),
    ipaddress.ip_network("23.184.48.154/32"),
    ipaddress.ip_network("38.45.65.162/32"),
    ipaddress.ip_network("45.8.124.7/32"),
    ipaddress.ip_network("45.62.163.122/32"),
    ipaddress.ip_network("45.87.43.235/32"),
    ipaddress.ip_network("45.88.200.214/32"),
    ipaddress.ip_network("45.135.229.105/32"),
    ipaddress.ip_network("46.250.252.66/32"),
    ipaddress.ip_network("51.79.250.183/32"),
    ipaddress.ip_network("51.195.151.150/32"),
    ipaddress.ip_network("57.129.134.86/32"),
    ipaddress.ip_network("65.108.243.152/32"),
    ipaddress.ip_network("77.111.247.45/32"),
    ipaddress.ip_network("77.111.247.72/32"),
    ipaddress.ip_network("80.78.28.10/32"),
    ipaddress.ip_network("88.218.206.233/32"),
    ipaddress.ip_network("92.38.132.88/32"),
    ipaddress.ip_network("94.154.172.214/32"),
    ipaddress.ip_network("102.130.116.13/32"),
    ipaddress.ip_network("103.70.115.11/32"),
    ipaddress.ip_network("104.36.80.106/32"),
    ipaddress.ip_network("104.143.10.202/32"),
    ipaddress.ip_network("130.0.232.208/32"),
    ipaddress.ip_network("139.99.171.251/32"),
    ipaddress.ip_network("146.59.231.4/32"),
    ipaddress.ip_network("151.80.18.153/32"),
    ipaddress.ip_network("160.19.78.209/32"),
    ipaddress.ip_network("164.215.103.238/32"),
    ipaddress.ip_network("165.140.202.54/32"),
    ipaddress.ip_network("165.140.203.149/32"),
    ipaddress.ip_network("171.25.193.39/32"),
    ipaddress.ip_network("171.25.193.40/32"),
    ipaddress.ip_network("185.101.35.175/32"),
    ipaddress.ip_network("185.125.168.154/32"),
    ipaddress.ip_network("185.181.62.113/32"),
    ipaddress.ip_network("185.195.236.20/32"),
    ipaddress.ip_network("185.195.236.97/32"),
    ipaddress.ip_network("194.15.36.46/32"),
    ipaddress.ip_network("194.62.248.90/32"),
    ipaddress.ip_network("195.160.220.104/32"),
    ipaddress.ip_network("198.98.54.183/32"),
    ipaddress.ip_network("198.98.51.189/32"),
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

@app.route('/', defaults={'path': ''}, methods = METHODS)
@app.route('/<path:path>', methods=METHODS)
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
