from lib.portal import __version__ as portal_version
from lib.aimmo import __version__ as aimmo_version
from lib.game import __version__ as rapid_router_version

requirements = "\n".join(
    [
        f"codeforlife-portal=={portal_version}",
        "git+https://github.com/ocadotechnology/aimmo.git@agones2",
        # f"aimmo=={aimmo_version}",
        f"rapid-router=={rapid_router_version}",
        "requests-toolbelt==0.9.*",
        "mysqlclient==1.4.*",
        "redis==3.3.*",
        "django-redis==4.11.*",
        "django-anymail[amazon_ses]==7.0.*",
        "google-python-cloud-debugger==2.*",
        "google-cloud-logging==1.*",
        "google-auth==1.*",
        "kubernetes",
    ]
)

requirements_path = "requirements.txt"
requirements_file = open(requirements_path, "w")
requirements_file.write(requirements)
requirements_file.close()
