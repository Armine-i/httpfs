import os
import socket
import re
import argparse

HOST = ''
# local directory path
LOCAL = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Prints debugging messages.', action='store_true')
parser.add_argument('-p', '--port', help='Specifies the port number that the server will listen and serve at. '
                                         'Default is 8080.', type=int, default=8080)
parser.add_argument('-d', '--directory', help='Specifies the directory that the server will use to read/write requested files. '
                                              'Default is the current directory when launching the application.', type=str)
args = parser.parse_args()


# -- START OF HTTPFS LIBRARY --

# parsing method for curl request if GET
def fsGET(files, response, currentdir, path):
    if path == '/':
        if args.verbose:
            print('Responding with the list of files')
        for f in files:
            response += f + '\n'
    elif re.search(r'\/\w+.\w+', path):
        path = path.strip('/')
        if args.verbose:
            print('Responding with a list of files in ' + path)
        if path in files:
            theFile = open(currentdir + '/' + path, 'r')
            response = theFile.read() + '\n'
            theFile.close()
        # error handling
        else:
            if args.verbose:
                print('HTTP 404 - the file: ' + path + ' was not found')
            response = 'HTTP 404 - file(s) not found\n'
    return response


# parsing method for curl request if POST
def fsPOST(files, data, currentdir, path):
    path = path.strip('/')
    if path in files:
        if args.verbose:
            print('Responding by overwriting the data in the file ', path)
        theFile = open(currentdir + '/' + path, 'w+')
        theFile.write(data)
        theFile.close()
        response = 'Data overwritten to file ' + path
    elif path not in files:
        if args.verbose:
            print('Responding by writing data to new file ' + path)
        theFile = open(currentdir + '/' + path, 'w+')
        theFile.write(data)
        theFile.close()
        response = 'Data written to new file ' + path
    # error handling
    else:
        if args.verbose:
            print('HTTP 403 - action refused')
        response = "HTTP 403 - action refused \n"
    return response

# -- END OF LIBRARY --


# main method that runs server
def runHttpfs(PORT, directory):
    currentdir = directory
    if directory is None:
        currentdir = LOCAL

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((HOST, PORT))
    listener.listen(5)

    if args.verbose:
        print('Httpfs server is listening at port', PORT)
    while True:
        files = os.listdir(currentdir)
        conn, addr = listener.accept()
        request = conn.recv(1024).decode("utf-8")
        request = request.split('\r\n')
        pathversion = request[0].split()
        methodPath = pathversion[0]
        path = pathversion[1]
        reqIndex = request.index('')
        data = ''

        for part in request[reqIndex + 1:]:
            data += part + '\n'

        response = ''

        if methodPath == 'GET':
            response = fsGET(files, response, currentdir, path)
        elif methodPath == 'POST':
            response = fsPOST(files, data, currentdir, path)

        conn.sendall(response.encode('utf-8'))
        conn.close()


runHttpfs(args.port, args.directory)
