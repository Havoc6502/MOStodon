#Dictionary converts ascii into petscii bytes
petscii={'A':b'\xc1','B':b'\xc2','C':b'\xc3','D':b'\xc4','E':b'\xc5','F':b'\xc6','G':b'\xc7','H':b'\xc8',
'I':b'\xc9','J':b'\xca','K':b'\xcb','L':b'\xcc','M':b'\xcd','N':b'\xce','O':b'\xcf','P':b'\xd0',
'Q':b'\xd1','R':b'\xd2','S':b'\xd3','T':b'\xd4','U':b'\xd5','V':b'\xd6','W':b'\xd7','X':b'\xd8','Y':b'\xd9',
'Z':b'\xda','a':b'A','b':b'B','c':b'C','d':b'D','e':b'E','f':b'F','g':b'G','h':b'H','i':b'I','j':b'J',
'k':b'K','l':b'L','m':b'M','n':b'N','o':b'O','p':b'P','q':b'Q','r':b'R','s':b'S','t':b'T','u':b'U',
'w':b'W','x':b'X','y':b'Y','z':b'Z','v':b'V','0':b'0','1':b'1','2':b'2','3':b'3','4':b'4','5':b'5',
'6':b'6','7':b'7','8':b'8','9':b'9','!':b'!','"':b'"','$':b'$','%':b'%','&':b'&','/':b'/','(':b'(',
')':b')',  '*':b'*',  '-':b'-','+':b'+','<':b'<','>':b'>',' ':b' ',':':b':','\n':b'\r\n','.':b'.',
',':b',','?':b'?','@':b'@','┌':b'\xb0','┐':b'\xae','└':b'\xad','┘':b'\xbd','─':b'\xc0',
'├':b'\xab','┤':b'\xb3','#':b'#', '£':b'\x5c','~':b'\xa3', '^':b'\xae','_':b'\xa4', '|':b'\x7d',
 '{':b'\xb3', '}':b'\xab', '\\':b'\xa5',          
'\x1c':b'\x1c','\x1e':b'\x1e','\x1f':b'\x1f','\x9c':b'\x9c',
'\x98':b'\x98','\x1d':b'\x1d','\x11':b'\x11','\x91':b'\x91','\x9d':b'\x9d','\x93':b'\x93',
'\x12':b'\x12','\x92':b'\x92','\x81':b'\x81','\x90':b'\x90','\x95':b'\x95','\x96':b'\x96',
'\x97':b'\x97','\x98':b'\x98','\x99':b'\x99','\x9a':b'\x9a','\x9b':b'\x9b','\x9e':b'\x9e',
'\x9f':b'\x9f','\x13':b'\x13',
"'":b"\x27","=":b"\x3d","[":b"[","]":b"]",";":b";"                                
}


#This function moves the cursor and changes color, clear screen
def cbmcursor(tx):
    out = b''
    if tx=="right" : out =b'\x1d'
    if tx=="home" : out =b'\x13'
    if tx=="down" : out =b'\x11'
    if tx=="up": out =b'\x91'
    if tx=="left": out=b'\x9d'
    if tx=="clear" : out =b'\x93'
    if tx=="white" : out =b'\x05'
    if tx=="red": out = b'\x1c'
    if tx=="green": out =b'\x1e'
    if tx=="blue": out =b'\x1f'
    if tx=="orange": out =b'\x81'
    if tx=="black": out =b'\x90'
    if tx=="brown": out =b'\x95'
    if tx=="pink": out =b'\x96'
    if tx=="dark grey": out=b'\x97'
    if tx=="dark gray": out=b'\x97'
    if tx=="gray": out=b'\x98'
    if tx=="grey": out=b'\x98'
    if tx=="lightgreen": out=b'\x99'
    if tx=="lightblue": out=b'\x9a'
    if tx=="lightgrey": out=b'\x9b'
    if tx=="purple": out=b'\x9c'
    if tx=="yellow": out=b'\x9e'
    if tx=="cyan": out=b'\x9f'
    if tx=="revon": out=b'\x12'
    if tx=="revoff": out=b'\x92'
    if tx=="randc":
       m=random.randint(0, 15)
       if m==0: out =b'\x1f'
       if m==1: out =b'\x81'
       if m==2: out =b'\x90'
       if m==3: out =b'\x95'
       if m==4: out =b'\x96'
       if m==5: out=b'\x97'
       if m==6: out=b'\x98'
       if m==7: out=b'\x99'
       if m==8: out=b'\x9a'
       if m==9: out=b'\x9b'
       if m==10: out=b'\x9c'
       if m==11: out=b'\x9e'
       if m==12: out=b'\x9f'
       if m==13: out =b'\x05'
       if m==14: out = b'\x1c'
       if m==15: out =b'\x1e'
    return out

#this function moves the cursor to an x,y position
def cursorxy(connection,x,y):
      connection.send(cbmcursor("home"))
      cy=1
      cx=1
      for cy in range(1,y):
         if (cy<y):
            connection.send(cbmcursor("down"))
      for cx in range(1,x):
         if (cx<x):
            connection.send(cbmcursor("right"))

def cbmencode(tx):

    out = b''
    for n in tx:
        try:
            out=out+(petscii[n])
        except:
            out
    return out
   

def cbmdecode(tx):
     out = ''
     for n in range(0,len(tx)):
        byten=tx[n:n+1]
        for k,v in petscii.items():
           #byten=tx[n:n+1]
           if(v==byten):
              out=out+str(k)
        if byten==b'a': out=out+"A"
        if byten==b'b': out=out+"B"
        if byten==b'c': out=out+"C"
        if byten==b'd': out=out+"D"
        if byten==b'e': out=out+"E"
        if byten==b'f': out=out+"F"
        if byten==b'g': out=out+"G"
        if byten==b'h': out=out+"H"
        if byten==b'i': out=out+"I"
        if byten==b'j': out=out+"J"
        if byten==b'k': out=out+"K"
        if byten==b'l': out=out+"L"
        if byten==b'm': out=out+"M"
        if byten==b'n': out=out+"N"
        if byten==b'o': out=out+"O"
        if byten==b'p': out=out+"P"
        if byten==b'q': out=out+"Q"
        if byten==b'r': out=out+"R"
        if byten==b's': out=out+"S"
        if byten==b't': out=out+"T"
        if byten==b'u': out=out+"U"
        if byten==b'v': out=out+"V"
        if byten==b'w': out=out+"W"
        if byten==b'x': out=out+"X"
        if byten==b'y': out=out+"Y"
        if byten==b'z': out=out+"Z"
        if byten==b'\x8d': out=out+"\n"
     return out


def input_line(connection):
     tline=b''
     while True:
        data = connection.recv(256, 0x40)
        if not data:
           print("no data - closed connection")
           connection.close()
           break
        if (data==b'\xff' or data==b'\xe6' or data==b'\xfe' or data==b'\xfb' or data==b'\x00' or data==b'\x01' or data==b'\xfd'):
           data=b''
        if (data==b'\xff\xfb\x01'):
           data=b''
        if (data==b'\xff\xfb\x00'):
           data=b''
        if (data==b'\xff\xfb\x00\xff\xfd\x00'):
           data=b''
        if (data==b'\xff\xfb\x00\xff\xfb\x00'):
           data=b''
        if (data==b'\xff\xfb\x01\xff\xfb\x00\xff\xfd\x00'):
           data=b''
        if (data==b'\x14'):
           if (len(tline)==0):
             data=b''
           tline=tline[0:len(tline)-1]
        if (tline==b'\xff\xfb\x01\xff\xfb\x00\xff\xfd\x00'):
           tline=b''
        connection.send(data)
        if (data==b'\r' or data==b'\r\n' or data==b'\n'):
           break
        if (data==b'\x14'):
            tline=tline
        else:
            tline=tline+data
     tline=cbmdecode(tline)
     return tline

#reads a password (and when typing it shows '*' to the user)
def input_pass(connection):
     tline=b''
     bbb=0
     while True:
        data = connection.recv(256, 0x40) #funciona como un input
        if not data:
           print("no data - closed connection")
           connection.close()
           break
        delchar=0
        if (data==b'\xff' or data==b'\xfb' or data==b'\x00' or data==b'\x01' or data==b'\xfd'):
           data=b''
        if (data==b'\xff\xfb\x01\xff\xfb\x00\xff\xfd\x00'):
           data=b''
        if (data==b'\x14'):
           if (len(tline)==0):
             data=b''
           tline=tline[0:len(tline)-1]
        if (tline==b'\xff\xfb\x01\xff\xfb\x00\xff\xfd\x00'):
           tline=b''
        if (data==b'\x14' or data==b'\r' or data==b'\r\n' or data==b'\n' or data==b''):
            connection.send(data)
        else:
            connection.send(b'*')
        if (data==b'\r' or data==b'\r\n' or data==b'\n'):
           break
        if (data==b'\x14'):
            tline=tline
        else:
            tline=tline+data
     tline=cbmdecode(tline)
     return tline

#similar to commodore basic get command (it just wait to type one char)
def get_char(connection):
     while True:
        data = connection.recv(256, 0x40) #works like a get
        if not data:
           print("no data - closed connection")
           connection.close()
           break
        rchar=data[0:1]
        connection.send(rchar)
        rchar=cbmdecode(rchar)
        return(rchar)

#this is to send the SEQ file to the user (useful for petscii graphics portions)
def send_seq(connection, filen):
    print("send_seq")
    print("FN->",filen)
    textMode = b'\x0e'
    connection.send(textMode)
    with open(filen, "rb") as f:
        nb=b''
        byte = f.read(1)
        while byte:
           nb = byte
           connection.send(nb)
           #print(nb)
           byte = f.read(1)
    send_cr(connection, "black")
    send_cr(connection, "revoff")
    get_char(connection) 


def send_ln(connection, line):
    linet=cbmencode(line)
    connection.send(linet)

def send_cr(connection, charx):
    chrxx=cbmcursor(charx)
    connection.send(chrxx)
