import datetime
import time
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = open('/Users/lenar/Desktop/secure-shop/access.log', 'a', encoding='utf-8', buffering=1)


    def __call__(self, request):
        print('MW: request', request.path)
        start_time = time.time()
        User_Agent = request.META.get('HTTP_USER_AGENT')
        protocol = request.META['SERVER_PROTOCOL']
        ip = request.META.get('REMOTE_ADDR')
        refer = request.META.get('HTTP_REFERER', '-')
        method = request.method
        query_string = request.META.get('QUERY_STRING')
        full_path = request.get_full_path()
        date =  datetime.datetime.now().astimezone().strftime('%d/%b/%Y:%H:%M:%S %z')
        response = self.get_response(request)
        end_time = time.time()
        latency = end_time - start_time
        status_code  = response.status_code
        size = len(response.text)
        apache_combained = f'{ip} - - [{date}] "{method} {full_path}" {status_code} {size} "{refer}" "{User_Agent}"'
        print('MW: пишу в файл:', apache_combained)
        self.log_file.write(apache_combained + '\n')
        print('MW: файл =', self.log_file.name, 'позиция =', self.log_file.tell())
        return response
        