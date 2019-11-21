# Life cycle of a code change
Depending on the part of the project your code change belongs to, it might go through different pipelines. To see what happens before it gets to the deploy app engine, check the `life cycle of a code change` docs on [portal](https://github.com/ocadotechnology/codeforlife-portal/blob/master/docs/life-cycle-of-a-code-change.md), [Kurono](https://github.com/ocadotechnology/aimmo/blob/development/docs/life-cycle-of-a-code-change.md) or [Rapid Router](https://github.com/ocadotechnology/rapid-router/blob/master/docs/life-cycle-of-a-code-change.md).


When the code is ready to be deployed to one of our servers, Semaphore CI is notified. Deploying to App Engine follows these steps:
* Install Python packages
* Redeploy Kubernetes infrastructure
* Upload a new version of the project to Google App Engine
* Switch traffic to the new version
