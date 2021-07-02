import argparse

# from pathlib import Path

# Versions will be fetched from the init of each package (portal, aimmo, game) after they are installed in lib - this happens in the "Build" step.
from lib.aimmo import __version__ as aimmo_version
from lib.game import __version__ as rapid_router_version

# portal_requirement = f"codeforlife-portal=={portal_version}"
# common_requirement = ""
# if Path("build/codeforlife-portal").is_dir():
#     portal_requirement = "./build/codeforlife-portal"
#     common_requirement = "./build/codeforlife-portal/cfl_common"

parser = argparse.ArgumentParser()
parser.add_argument("--portal-branch")
args = parser.parse_args()

if args.portal_branch is None:
    from lib.portal import __version__ as portal_version

    portal_requirement = f"codeforlife-portal=={portal_version}"
    common_requirement = ""
else:
    portal_requirement = f"git+https://github.com/ocadotechnology/codeforlife-portal@{args.portal_branch}#egg=portal"
    common_requirement = f"git+https://github.com/ocadotechnology/codeforlife-portal@{args.portal_branch}#egg=common&subdirectory=cfl_common"


requirements = "\n".join(
    [
        portal_requirement,
        common_requirement,
        f"aimmo=={aimmo_version}",
        # "./aimmo",  # Uncomment this to install a custom aimmo built in deploy_gcloud workflow
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
        "google-cloud-container==2.3.0",
        "git+https://github.com/ocadotechnology/django-autoconfig",
    ]
)

requirements_path = "requirements.txt"
requirements_file = open(requirements_path, "w")
requirements_file.write(requirements)
requirements_file.close()
