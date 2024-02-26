
params = '',8083

class HelloHandler(BaseHTTPRequestHandler):
    def do_Head(self):
        self.send_reponse(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_Get(self):
        self.do_Head()
        self.wfile.write("""
            <html><head>
                <title>Examen Juan Compaire</title></head><body><p>HelloWorld</p>
            <form method="POST" >
            <input type="submit" value="Click me">
                <img src="https://fotografias.lasexta.com/clipping/cmsimages01/2023/06/27/1E6C851B-C0AD-4C37-BA0F-8BE91B59FEAE/ilia-topuria_97.jpg?crop=1024,576,x0,y0&width=1600&height=900&optimize=low&format=webply">
                        </input>
            </form>
            </body></html>

                         """.encode("utf-8"))
        
    def do_Post(self):
        self.do_Head()
        self.wfile.write("""<html><head><title>Hello
            World</title></head><body><p>Form received</p>
            </body></html>""".encode("utf-8"))
        self.Examn()

    def Examn():
        print("SE hizo el examen")
        pass

server = HTTPServer(params,HelloHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()