# Contribution Guide

## Before you start ##

Please make sure you've cleared your doubts [_Volunteer Questions_](https://docs.google.com/forms/d/e/1FAIpQLSfMO-_ByPnTWuIFo7sGlbqnutv4oaNlu4caHwzWfnvno964ig/viewform) - you already know what hummingbird-v2 is, right?

We also have a multi-member technology community to support you on our technical channel on Slack. Don't hesitate to contact us there.

## Installing

Since our stack is simple, we have chosen to standardize our instructions do [Docker Compose](https://docs.docker.com/compose/install/), which will help you to rotate each service in some commands.

Everything is expected to work with:

```console
$ docker-compose up --build
```

**Note:** `docker-compose up --build` is just a health check to make sure all the dependencies are successfully installed and the project is working well. To properly run hummingbird-v2 there are a few more steps (migrations, for example). We have a guide on how to perform all the steps working locally in [_README.md_](https://github.com/CovidZero/hummingbird-v2/blob/staging/README.md)

Then browse from [`localhost:5000`](http://localhost:5000). 

## The basics of contributing

Many discussions about ideas take place in the [Issues](https://github.com/CovidZero/hummingbird-v2/issues) section. There, and interacting on the `#hummingbird-v2` Slack channel, you can catch up on what's going on and also suggest new ideas.

You can follow what the core team is working on [Projects](https://github.com/CovidZero/hummingbird-v2/projects/1).

### The basics of Git

**1. _Fork_ this repository**.

There is a big button for this on the GitHub interface, usually in the top right corner.

**2. Clone your repository fork**.

```console
$ git clone http://github.com/<YOUR-GITHUB-USERNAME>/hummingbird-v2.git
```

**3. Configure your fork remote by pointing to the organization's repo**.

```console
$ git remote add upstream https://github.com/CovidZero/hummingbird-v2.git 
```

**4. Create a development branch**.

```console
$ git checkout staging
$ git checkout -b <YOUR-FEATURE-BRANCH>
```

Please keep your fork updated with our STAGING branch.

```console
$ git fetch upstream staging
```

**5. Do what you do best**.

Now it's your turn to shine and write meaningful code to raise the bar for the project!

**6. Commit yourself to your changes***.

```console
$ git rebase <YOUR-FEATURE-BRANCH>
$ git commit -m"My very nice contribution"
```

Note that we use the `rebase` to keep our commits more organized and linear.

**7. Push to the branch to the fork**.

```console
$ git push origin <YOUR-FEATURE-BRANCH> 
```
**8. Code Clear and Test**.

Two of the Actions we have implemented will do test analysis and code style, using respectively the libs [_unittest_](https://docs.python.org/3/library/unittest.html) and [_flake8_](http://flake8.pycqa.org/en/latest/).

**9. Create a new _Pull Request_**.

From your fork at GitHub there is usually a button to open pull requests.

- Please be very descriptive in your PR. More verbose is better. 

By default all _Pull Request_ will be analyzed by our pre-defined _Git Actions_, and if it passes the build tests, it must still be analyzed and approved by at least two `reviewers` before it can be merged into the production branch.
