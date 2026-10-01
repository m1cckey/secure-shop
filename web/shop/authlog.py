import json

class AuthLogger:
    def __init__(self):
        self.log_file = open('/Users/lenar/Desktop/secure-shop/auth.log', 'a', encoding='utf-8', buffering=1)


    def log_auth(self, ip, username, result, latency):
        event = {
            'ip': ip,
            'username': username,
            'result': result,
            'latency': latency
        }
        self.log_file.write(json.dump(event) + '/n')
