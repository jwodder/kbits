Creating a line-oriented client socket:

.. code:: python

    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('httpbin.org', 80))
        sf = s.makefile('rw', buffering=1, encoding='iso-8859-1', newline='\r\n')
        print('GET /get HTTP/1.0', file=sf)
        print('Host: httpbin.org', file=sf)
        print('Connection: close', file=sf)
        #print(file=sf, flush=True)
        print(file=sf)
        for line in sf:
            print(line, end='')

.. TODO:
    - Look into the necessity of flushing
    - Double-check that line reading doesn't block waiting for extra data
    - SSL
    - IPv6
    - Can the return value of `makefile` be used as a context manager?
    - Does `for line in sf:` block too much à la `sys.stdin`, requiring the use
      of `for line in iter(sf.readline, ''):` instead?
