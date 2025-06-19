from django.http import JsonResponse

import game
import portal


def versions(_request):
    """Return json containing the installed versions of the main packages."""
    return JsonResponse({
        'codeforlife-portal': portal.__version__,
        'rapid-router': game.__version__
    })
