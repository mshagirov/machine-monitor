import requests

def http_get(hostname : str, path : str):
    try:
        res = requests.get("http://" + hostname + "/" + path, headers={"accept": "application/json"})
        if res.status_code != requests.codes.ok:
            return {'error': f"HTTPError:{res.status_code}"}
        return res.json()
    except Exception as e:
        return {'error':str(e)}

