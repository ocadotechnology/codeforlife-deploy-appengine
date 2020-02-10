import os
import shutil

# Copy over the files from gaerpytz directory to the one in the lib folder
for pytz_file in os.listdir("gaerpytz"):
    shutil.copy("gaerpytz/" + pytz_file, "lib/pytz")
