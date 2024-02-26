from scp import SCPClient  
from http.server import BaseHTTPRequestHandler, HTTPServer  
import paramiko 
from Crypto.PublicKey import RSA  
from Crypto.Cipher import AES, PKCS1_OAEP  
import smtplib  
from ftplib import FTP  


params = '', 8086  


class HelloHandler(BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        self.send_response(200)  
        self.send_header('Content-type', 'text/html')  
        self.end_headers()  

    def do_GET(self):
        self.do_HEAD()  

        self.wfile.write("""
            <html><head>
                <title>Examen </title></head><body><p>HelloWorld</p>
            <form method="POST" >
            <input type="submit" value="Probar">
                <img src="https://s2.abcstatics.com/media/deportes/2020/10/08/hs-kzYF--1248x698@abc.jpg">
                        </input>
            </form>
            </body></html>""".encode("utf-8"))  

    def do_POST(self):
        self.do_HEAD()  

        self.wfile.write("""<html><head><title>Hello
            World</title></head><body><p>Form received</p>
            </body></html>""".encode("utf-8"))  
        self.Examn()  
        
    def Examn(self):
        print("Me ha llegado")
        self.connectSSH()  
        self.desEncrypt()  
        self.writeEncryptedDataTofile()  
        self.sendEmail()  
        self.uploadFTP()
    
    def connectSSH(self):
        print("Conenctando a SSH")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname='192.168.1.123', port=2222, username='tresdos', password='tresdos')
        print("Conecté")

        scp = SCPClient(ssh.get_transport())
        scp.get('/home/encrypted_data.bin')
        scp.get('/home/private.pem')
        print("Descargé los files")
        scp.close()
        ssh.close()
        
        print("Finish SSH")
    
    def listCallback(self, line):
        print(line)
    
    def desEncrypt(self):
        print("Desencriptar")
        file_in = open("encrypted_data.bin","rb")
        private_key = RSA.import_key(open("private.pem").read())
        enc_session_key = file_in.read(private_key.size_in_bytes())
        file_in.close()  

        cipher_rsa = PKCS1_OAEP.new(private_key)
        self.session_key = cipher_rsa.decrypt(enc_session_key)  
        print(self.session_key)  
        print("Desencriptar end")

    def writeEncryptedDataTofile(self):
        
        file_out = open("mensajito.txt","wb")
        file_out.write(self.session_key)
        file_out.close()

    def sendEmail(self):
        print("Intentar enviar email")
        client = smtplib.SMTP(host='192.168.1.123',port=1023)
        sender = 'juancompaire2004@gmail.com'
        dest = 'gorka.sanz@zaragoza.salesuanos.edu'
        message = "Viva don bosco"
        message_template = 'From:%s\r\nTo:%s\r\n\r\n%s'  
        client.set_debuglevel(1)  
    
        client.sendmail(sender, dest, message_template % (sender, dest, message))
        client.quit()  
        print("Enviar email end")

    def uploadFTP(self):
        print("Intentando el FTP")
        
        url = '192.168.1.123'
        port = 23

        sftp = FTP()
        sftp.connect(url,port)
        sftp.login('dostres','dostresdos')

        sftp.cwd('/')
        print(sftp.pwd())
        print(sftp.getwelcome())

        with open('mensajito.txt','rb') as file:
            sftp.storbinary('STOR mensajito.txt',file)

        sftp.retrlines('LIST',self.listCallback)

        sftp.quit()

        print("Terminé FTP, por fín")

    
server = HTTPServer(params, HelloHandler)


try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()