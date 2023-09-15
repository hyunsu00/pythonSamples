# main_thread_twisted.py
from threading import Thread
from twisted.web import server, resource
from twisted.internet import reactor, endpoints, threads
from flask import Flask

# twisted
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

root = resource.Resource()
root.putChild(b"health", HealthCheckResource())
endpoints.serverFromString(reactor, "tcp:8101").listen(server.Site(Counter()))
endpoints.serverFromString(reactor, "tcp:8102").listen(server.Site(root))

# flask
app = Flask(__name__)
@app.route('/health')
def health_check():
    return '서버 정상 작동 중입니다.', 200

if __name__ == '__main__':
    # twisted를 자식 쓰레드로 실행 시킨다.
    Thread(target=reactor.run, args=(False,)).start()

    # flask를 메인 쓰레드로 실행 시킨다.
    app.run(host='0.0.0.0', port=8103)
    
    