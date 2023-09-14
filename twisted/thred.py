import threading
from twisted.web import server, resource
from twisted.internet import reactor, threads, endpoints

# Health check 리소스 클래스 정의
class HealthCheckResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return b"Health Check: OK"

# 다른 리소스 클래스 정의 (예: 데이터 리소스)
class DataResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return b"Data Resource: This is your data."
    
# Twisted main loop를 실행하는 함수
def twisted_main_loop():
    root = resource.Resource()
    root.putChild(b"data", DataResource()) # 데이터 리소스
    endpoints.serverFromString(reactor, "tcp:8101").listen(server.Site(root))
    reactor.run()

# Twisted main loop를 실행하는 스레드 시작
twisted_thread = threading.Thread(target=twisted_main_loop)
twisted_thread.start()

# 다른 스레드에서 작업을 실행
my_threaded_function()