from django.http import HttpResponse
from django.db.utils import OperationalError


class DBUnavailableMiddleware:
    """Simple middleware to catch database OperationalError and return a
    friendly informational page instead of a 500.

    This is intended as a development convenience when the legacy MySQL
    schema hasn't been imported or when using the SQLite fallback without
    creating the `library` tables. It keeps the site usable and provides
    setup guidance.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except OperationalError:
            msg = (
                "<h1>Database unavailable</h1>"
                "<p>The application's database tables are not available. "
                "If you haven't imported the supplied MySQL schema, follow "
                "the README instructions to import <code>source/book.sql</code> "
                "or set up the SQLite fallback by exporting <code>DJANGO_USE_SQLITE=1</code>." 
                "</p>"
                "<p><a href=\"/\">Return to home</a></p>"
            )
            return HttpResponse(msg, status=503)
        return response
