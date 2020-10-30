from lib.portal import __version__ as portal_version
from lib.aimmo import __version__ as aimmo_version

requirements = [
    # f"codeforlife-portal=={portal_version}\n"
    "git+https://github.com/ocadotechnology/codeforlife-portal.git@debug_branch2",
    f"aimmo=={aimmo_version}",
    "requests-toolbelt==0.9.*",
    "mysqlclient==1.4.*",
    "redis==3.3.*",
    "django-redis==4.11.*",
    "django-anymail[amazon_ses]==7.0.*",
    "google-python-cloud-debugger",
    "google-cloud-logging",
    "google-auth",
].join("\n")

requirements_path = "requirements.txt"
requirements_file = open(requirements_path, "w")
requirements_file.write(requirements)
requirements_file.close()
