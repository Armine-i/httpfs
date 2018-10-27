# httpfs
HTTP file server
github link: https://github.com/Armine-i/httpfs

***Steps before using the command line tool:***

    $ source venv/bin/activate

***Usage:***

     httpfs [-v] [-p PORT] [-d PATH-TO-DIR]

        -v Prints debugging messages.
  
        -p Specifies the port number that the server will listen and serve at.
        Default is 8080.
  
        -d Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.

***Examples with curl:***
- GET request:

      curl -get localhost:8080/
      curl -get localhost:8080/somefile.txt

- POST request:

      curl -post -H "Content-Type:application/text" -d "L.O.V.E" localhost:8080/ex.txt
