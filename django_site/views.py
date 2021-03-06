from django.http import JsonResponse

import aimmo
import game
import portal


def versions(_request):
    """Return json containing the installed versions of the main packages."""
    return JsonResponse({
        'aimmo': aimmo.__version__,
        'codeforlife-portal': portal.__version__,
        'rapid-router': game.__version__
    })
