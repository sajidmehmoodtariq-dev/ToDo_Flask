from app import app

# Vercel looks for either `app` or `application`
application = app

# Required handler for Vercel serverless
def handler(request, *args, **kwargs):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
