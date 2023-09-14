# mainEx1.py
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

endpoints.serverFromString(reactor, "tcp:8101").listen(server.Site(Counter()))
reactor.run()