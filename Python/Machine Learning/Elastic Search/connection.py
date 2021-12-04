from elasticsearch import Elasticsearch

# you can use RFC-1738 to specify the url
# es = Elasticsearch(['https://user:secret@localhost:443'])

# ... or specify common parameters as kwargs

# es = Elasticsearch(
#     ['localhost', 'otherhost'],
#     http_auth=('user', 'secret'),
#     scheme="https",
#     port=443,
# )

es = Elasticsearch(
    ['http://192.168.2.134'],
    scheme="http",
    port=9200,
)

# SSL client authentication using client_cert and client_key

# from ssl import create_default_context

# context = create_default_context(cafile="path/to/cert.pem")
# es = Elasticsearch(
#     ['localhost', 'otherhost'],
#     http_auth=('user', 'secret'),
#     scheme="https",
#     port=443,
#     ssl_context=context,
# )

res=es.get(index='ccav_order_detail',id="tcrwKW0BPI6yWmuE754H")
print(res)

res= es.search(index='ccav_order_detail',body={'query':{'match_all':{}}})
print(res)


res= es.search(index='ccav_order_detail',body={  "query": {    "match": {    "reg_id":"61098"    }  },  "size": 10000})
print(res)













































upstream hello_app_server {
  # fail_timeout=0 means we always retry an upstream even if it failed
  # to return a good HTTP response (in case the Unicorn master nukes a
  # single worker for timing out).

  server unix:/webapps/hello_django/run/gunicorn.sock fail_timeout=0;
}

server {

    listen   80;
    server_name example.com;

    client_max_body_size 4G;

    access_log /webapps/hello_django/logs/nginx-access.log;
    error_log /webapps/hello_django/logs/nginx-error.log;

    location /static/ {
        alias   /webapps/hello_django/static/;
    }

    location /media/ {
        alias   /webapps/hello_django/media/;
    }

    location / {
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application
        proxy_set_header Host $http_host;

        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;

        # set "proxy_buffering off" *only* for Rainbows! when doing
        # Comet/long-poll stuff.  It's also safe to set if you're
        # using only serving fast clients with Unicorn + nginx.
        # Otherwise you _want_ nginx to buffer responses to slow
        # clients, really.
        # proxy_buffering off;

        # Try to serve static files from nginx, no point in making an
        # *application* server like Unicorn/Rainbows! serve static files.
        if (!-f $request_filename) {
            proxy_pass http://hello_app_server;
            break;
        }
    }

    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /webapps/hello_django/static/;
    }
}
