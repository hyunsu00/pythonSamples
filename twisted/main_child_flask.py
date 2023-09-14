# flask_main.py
from flask import Flask
import os
from twisted.web import server, resource
from twisted.internet import reactor, endpoints

class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader(b"content-type", b"text/plain")
        content = u"{} request #{}\n".format(request.uri, self.numberRequests)
        return content.encode("ascii")
    
class HealthCheckResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return b"Health Check: OK"
    
app = Flask(__name__)

@app.route('/health')
def health_check():
    return '서버 정상 작동 중입니다.', 200

def run_child_flask():
    try:
        # fork()를 호출하여 자식 프로세스를 생성합니다.
        child_pid = os.fork()

        if child_pid == 0:
            # 자식 프로세스에서 실행되는 코드
            print("자식 프로세스 실행 중")
            
            app.run(host='0.0.0.0', port=8103)
        
            print("자식 프로세스 종료")
            os._exit(0)  # 자식 프로세스를 종료합니다.

    except OSError as e:
        print(f"fork() 호출 중 오류 발생: {e}")

if __name__ == '__main__':
    # flask를 자식 프로세스로 실행 시킨다.
    run_child_flask()

    # twisted를 메인 프로세스로 실행 시킨다.
    root = resource.Resource()
    root.putChild(b"health", HealthCheckResource())
    endpoints.serverFromString(reactor, "tcp:8101").listen(server.Site(Counter()))
    endpoints.serverFromString(reactor, "tcp:8102").listen(server.Site(root))
    reactor.run()
    