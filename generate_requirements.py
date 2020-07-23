from lib.portal import __version__ as portal_version
from lib.aimmo import __version__ as aimmo_version

requirements = (
    f"git+https://github.com/ocadotechnology/rapid-router@common-test#egg=rapid-router\n"
    f"git+https://github.com/ocadotechnology/codeforlife-portal@common-models-test#egg=codeforlife-portal\n"
    f"git+https://github.com/ocadotechnology/aimmo@add_class_to_game#egg=aimmo\n"
    f"requests-toolbelt==0.9.*\n"
    f"mysqlclient==1.4.*\n"
    f"redis==3.3.*\n"
    f"django-redis==4.11.*\n"
    f"django-anymail[amazon_ses]==7.0.*\n"
    f"google-python-cloud-debugger\n"
    f"https://test-files.pythonhosted.org/packages/00/a8/08be861e496afbb359626fcb2aa52838cac0ff1aeb0ccb4be3d17441776d/cfl_common_test-0.0.0-py3-none-any.whl"
)

requirements_path = "requirements.txt"
requirements_file = open(requirements_path, "w")
requirements_file.write(requirements)
requirements_file.close()
