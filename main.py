from django_site.wsgi import application

try:
    import googleclouddebugger

    googleclouddebugger.enable()
except ImportError:
    pass

app = application
