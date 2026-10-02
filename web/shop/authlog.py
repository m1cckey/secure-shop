import json
from datetime import datetime

class AuthLogger:
    def __init__(self):
        self.log_file = open('/Users/lenar/Desktop/secure-shop/auth.log', 'a', encoding='utf-8', buffering=1)


    def log_auth(self, ip, username, result, latency_ms):
        event = {
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'username': username,
            'result': result,
            'latency': latency_ms
        }
        self.log_file.write(json.dumps(event, ensure_ascii=False) + '\n', )

auth_logger = AuthLogger()