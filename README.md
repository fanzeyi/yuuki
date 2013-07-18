Yuuki
=====

A personal URL shorter service with `Flask`. 

install
-------

    $ virtualenv ./venv
    $ source venv/bin/activate
    $ pip install Flask Flask-SQLAlchemy
    $ vim local_config.py # rewrite any thing you want from config.py :)
    
    # Develope mode
    $ python app.py
    
    # Factory mode
    $ pip install gunicorn gevent
    $ gunicorn -w 4 app:app -k gevent -b 127.0.0.1:8060
    # then edit your nginx configuration, enjoy it :)
    
usage
-----

    $ curl http://yourlocation/create -F "url=http://www.google.com" -F "passwd=yourpasswd" # random url 
    $ curl http://yourlocation/create -F "url=http://www.google.com" -F "passwd=yourpasswd" -F "code=google" # custom url
    
license
-------

MIT License.

