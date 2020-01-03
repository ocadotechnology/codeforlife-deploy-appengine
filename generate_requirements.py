from lib.portal import __version__ as portal_version
from lib.aimmo import __version__ as aimmo_version

requirements = (
    f"codeforlife-portal=={portal_version}\n"
    f"aimmo=={aimmo_version}\n"
    f"requests-toolbelt==0.9.1\n"
    f"mysqlclient==1.4.6\n"
    f"redis3.3.11\n"
    f"django-redis==4.11.0"
)

requirements_path = "requirements.txt"
requirements_file = open(requirements_path, "w")
requirements_file.write(requirements)
requirements_file.close()
