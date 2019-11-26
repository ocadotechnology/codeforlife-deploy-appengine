# Life cycle of a code change
Depending on the part of the project your code change belongs to, it might go through different pipelines. To see what happens before it gets to the deploy app engine, check the `life cycle of a code change` docs on [Portal](https://github.com/ocadotechnology/codeforlife-portal/blob/master/docs/life-cycle-of-a-code-change.md), [Kurono](https://github.com/ocadotechnology/aimmo/blob/development/docs/life-cycle-of-a-code-change.md) or [Rapid Router](https://github.com/ocadotechnology/rapid-router/blob/master/docs/life-cycle-of-a-code-change.md).


When a new version of codeforlife-portal, aimmo or rapid-router is released to one of our servers, Semaphore CI is notified. Deploying to App Engine follows these steps:
* Install Python packages:
    * Install codeforlife-portal and aimmo
    * Install gaerpytz, a library to make the pytz library work when using GAE, needed since Django 1.11
    * Collect the static files for the whole project
* Redeploy Kubernetes infrastructure
    * Get the latest aimmo version from the `__init__.py` file in aimmo
    * Recreate the ingress yaml Python object depending on the environment of the build
    * Recreate the aimmo-game-creator yaml Python object and replace the GAME_API_URL env variable depending on the environment
    * Restart the pods based on the new aimmo-game-creator and ingress yamls.
* Upload a new version of the project to Google App Engine
* Switch traffic to the new version
