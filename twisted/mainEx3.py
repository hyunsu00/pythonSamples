# mainEx3.py
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

class CustomSite(server.Site):
    def getResourceFor(self, request):
        if request.path == b"/health":
            return HealthCheckResource()
        return super().getResourceFor(request)
    
# 루트 리소스 생성
root = resource.Resource()
root.putChild(b"data", DataResource())          # 데이터 리소스

# 커스텀 사이트 생성
site = CustomSite(root)

# 포트 8101에서 서버 시작
endpoints.serverFromString(reactor, "tcp:8101").listen(site)

# 리액터 시작
reactor.run()