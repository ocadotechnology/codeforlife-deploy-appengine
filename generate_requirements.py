import argparse

# Versions will be fetched from the init of each package (portal, game) after they are installed in lib - this happens in the "Build" step.
from lib.game import __version__ as rapid_router_version
from lib.portal import __version__ as portal_version


parser = argparse.ArgumentParser()
parser.add_argument("--portal-branch")
parser.add_argument("--rapid-router-branch")
args = parser.parse_args()

if args.portal_branch:
    portal_requirement = f"git+https://github.com/ocadotechnology/codeforlife-portal@{args.portal_branch}#egg=codeforlife-portal"
    common_requirement = f"git+https://github.com/ocadotechnology/codeforlife-portal@{args.portal_branch}#egg=cfl-common&subdirectory=cfl_common"
else:
    portal_requirement = f"codeforlife-portal=={portal_version}"
    common_requirement = ""

if args.rapid_router_branch:
    rapid_router_requirement = f"git+https://github.com/ocadotechnology/rapid-router@{args.rapid_router_branch}#egg=rapid-router"
else:
    rapid_router_requirement = f"rapid-router=={rapid_router_version}"

requirements = "\n".join(
    [
        rapid_router_requirement,
        portal_requirement,
        common_requirement,
        "requests-toolbelt==0.9.*",
        "mysqlclient==2.1.*",
        "redis==5.2.0",
        "django-redis==5.4.0",
        "google-cloud-logging==1.*",
        "google-auth==1.*",
        "psycopg2==2.9.10"
    ]
)

requirements_path = "requirements.txt"
requirements_file = open(requirements_path, "w")
requirements_file.write(requirements)
requirements_file.close()
