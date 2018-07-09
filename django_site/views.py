from django.http import JsonResponse

import game._version
import aimmo._version
import portal._version

def versions(_request):
    '''Return json containing the installed versions of the main packages.'''
    return JsonResponse({
        'aimmo': aimmo._version.get_versions()['full-revisionid'],
        'codeforlife-portal': portal._version.get_versions()['full-revisionid'],
        'rapid-router': game._version.get_versions()['full-revisionid'],
    })
