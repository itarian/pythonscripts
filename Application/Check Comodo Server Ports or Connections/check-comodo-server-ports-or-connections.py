def check_tcp_connection(server, port):
    sock_object=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result=sock_object.connect_ex((server, port))
    sock_object.close()
    return result

if __name__=="__main__":
    import socket
    import time
    valkyrie_server='valkyrie.comodo.com'
    valkyrie_protocol='HTTPS', 443
    FLS_server='fls.security.comodo.com'
    FLS_protocol={'TCP': (80, 4448, 4442)}
    valkyrie_result='Checking %s %s %s %s'%(valkyrie_protocol[0], valkyrie_server, str(valkyrie_protocol[-1]), '.'*15)
    if check_tcp_connection(valkyrie_server, valkyrie_protocol[-1])==0:
        print_string='%s PASS'%valkyrie_result
    else:
        print_string='%s FAILED'%valkyrie_result
    print print_string

    for i in FLS_protocol:
        for j in FLS_protocol[i]:
            FLS_result='Checking %s %s %s %s'%(i, FLS_server, str(j), '.'*15)
            if check_tcp_connection(FLS_server, j)==0:
                print_string='%s PASS'%FLS_result
            else:
                print_string='%s FAILED'%FLS_result
            print print_string

