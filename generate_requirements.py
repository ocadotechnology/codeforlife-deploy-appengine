from lib.portal import __version__ as portal_version
from lib.aimmo import __version__ as aimmo_version

requirements = (
    f"git+https://github.com/ocadotechnology/rapid-router@cypress_smoke_tests#egg=rapid-router\n"
    f"git+https://github.com/ocadotechnology/codeforlife-portal@cypress_smoke_tests#egg=codeforlife-portal\n"
    f"aimmo=={aimmo_version}\n"
    f"requests-toolbelt==0.9.*\n"
    f"mysqlclient==1.4.*\n"
    f"redis==3.3.*\n"
    f"django-redis==4.11.*\n"
    f"django-anymail[amazon_ses]==7.0.*\n"
    f"google-python-cloud-debugger"
)

requirements_path = "requirements.txt"
requirements_file = open(requirements_path, "w")
requirements_file.write(requirements)
requirements_file.close()
