from flask import Flask, request, jsonify
import requests
import ast

app = Flask(__name__)

route_mapping = {
    "call": "http://127.0.0.1:8005", #Orchastrator
    "product": "http://127.0.0.1:8009" #Product Page
}

routes=route_mapping.keys()
@app.route('/health', methods=['GET'])
def server_health():
    return {"message":"works"}

@app.route('/', methods=["POST"])
def load_balance():
    if request.method=='POST':
        payload=request.data
        payload=ast.literal_eval(payload.decode('utf-8'))
        path=payload['path']
        if path=='call':
            try:
                return {"message":"hit"}
            except:
                raise Exception("Response from agent failed")
        elif path=='product':
            try:
                url=route_mapping["product"]
                params={}
                r=requests.post(url, json=params)
                return{"response":r.json()}
            except:
                raise Exception("Request body invalid")
        raise Exception("Path not defined, available paths: ",route_mapping.keys())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)  # Load balancer runs on port 5050