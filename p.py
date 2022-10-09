import socket,sys,_thread,traceback, ssl
import streamlit as st

 
def main():
    global listen_port, buffer_size, max_conn
    try:
        number = st.number_input('Enter a listening port: ')
        listen_port = int(number)
    except KeyboardInterrupt:
        sys.exit (0)
        
    max_conn = 10000
    buffer_size = 10000
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", listen_port))
        s.listen(max_conn)
        st.write("[*] Intializing socket. Done.")
        st.write("[*] Socket binded successfully...")
        st.write("[*] Server started successfully [{}]".format(listen_port))
    except Exception as e:
        st.write(e)
        sys.exit(2)

    while True:
        try:
            conn,addr = s.accept()
            data = conn. recv(buffer_size)
            _thread.start_new_thread(conn_string,(conn, data, addr))
        except KeyboardInterrupt:
            s.close()
            st.write("\n[*] Shutting down...")
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr):
    try: 
        st.write(addr)
        first_line = data.decode('latin-1').split("\n")[0]
        st.write(first_line)
        url = first_line.split(" ")[1]
        
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]
            
        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos + 1):][:webserver_pos - port_pos -1])
            webserver = temp[:port_pos]

        st.write(webserver)
        proxy_server(webserver,port,conn,data,addr)
    except Exception as e:
        st.write(e)
        traceback.print_exc()
        
def proxy_server(webserver, port, conn, data, addr):
    st.write("{} {} {} {}".format(webserver, port, conn, addr))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)
        while 1:
            reply = s.recv(buffer_size)
            
            if len(reply) > 0:
                conn.sendall(reply)
                st.write("[*] Request sent: {} > {}".format(addr[0],webserver))
            else:
                break        
        
        s.close()
        conn.close()
        
    except Exception as e:
        st.write(e)
        traceback.print_exc()
        s.close()
        conn.close()
        sys.exit(1)

if __name__ == "__main__":
    main()