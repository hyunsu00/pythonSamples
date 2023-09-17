
from threading import Thread
from twisted.web import server, resource
from twisted.internet import reactor, endpoints, threads
from http.server import SimpleHTTPRequestHandler
import socketserver

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

# httpd
class HealthCheckHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8') # 한글 문자열을 전송하기 위해 charset을 설정
            self.end_headers()
            response_text = "서버 정상 작동 중입니다."  # 한글 문자열을 포함한 응답 텍스트
            self.wfile.write(response_text.encode('utf-8')) # 문자열을 UTF-8 인코딩으로 바이트로 변환하여 전송
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

if __name__ == '__main__':
    # httpd를 자식 쓰레드로 실행 시킨다.
    httpd = socketserver.TCPServer(("", 8103), HealthCheckHandler)
    Thread(target=httpd.serve_forever).start()

    # twisted를 메인 쓰레드로 실행 시킨다.
    reactor.run()
