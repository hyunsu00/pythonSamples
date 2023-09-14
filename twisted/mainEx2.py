# mainEx2.py
from twisted.web import server, resource
from twisted.internet import reactor, endpoints

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

# 루트 리소스 생성
root = resource.Resource()
root.putChild(b"health", HealthCheckResource())  # Health check 리소스
root.putChild(b"data", DataResource())          # 데이터 리소스

# 포트 8101에서 서버 시작
endpoints.serverFromString(reactor, "tcp:8101").listen(server.Site(root))

# 리액터 시작
reactor.run()