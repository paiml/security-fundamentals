# Security Fundamentals

Learn what security means in software, who keeps it safe, and how attackers think,
then practice on a small site you run on your own computer.

This repository holds the examples from the **Security Fundamentals** video lessons.
Most of the lessons are ideas, explained without code, and the first two weeks need only
a browser. The terminal lessons, all in week 3, share one small orders site that runs
only on your computer: you start it, check its customers file against the three pillars
of security, list its ways in, watch one user read another user's order, then add the
check that stops it.

<details>
  <summary><b>Table of Contents</b></summary>
  <br>

* [What you will learn](#what-you-will-learn)
* [Who this is for](#who-this-is-for)
* [Get set up](#get-set-up)
* [How each lesson works](#how-each-lesson-works)
* [Learning path](#learning-path)
  * [1. What security means](#1-what-security-means)
  * [2. Who keeps software safe](#2-who-keeps-software-safe)
  * [3. Thinking like an attacker](#3-thinking-like-an-attacker)
* [Troubleshooting](#troubleshooting)
* [Where to go next](#where-to-go-next)

</details>

## What you will learn

By the end of these lessons you will be able to:

* Explain what security is, how it has changed, and its three pillars:
  confidentiality, integrity and availability
* Use the words security people use: asset, threat, vulnerability and risk
* Find your way around the organizations and databases behind security: OWASP, CVE,
  CISA's list of exploited vulnerabilities and the GitHub Advisory Database
* Find a site's security contact, so you know how to report a problem
* Explain what a web application is, and check a file against the first two pillars
* List the ways into a web application, the first thing an attacker maps
* Recognize broken access control, add the missing check, and verify it

> [!NOTE]
> **Diversity Statement:** We share a commitment to diversity and equity, removing
> barriers to learning so that everyone can participate fully. These lessons are meant
> to be useful to people with a wide range of backgrounds, identities, and learning
> styles, whether you found them through a course or on your own on GitHub.

## Who this is for

You build, run or work around software and want to understand what keeping it secure
involves. You don't need any security experience.

For the terminal lessons, you will need to be comfortable running commands. Each one
starts by moving into its folder with `cd`, and runs everything from there. You can
read a few lines of Python, but you don't need to write any. The web lessons only need
a browser.

## Get set up

You need:

* **A terminal running bash or zsh**: macOS, Linux, or Windows with
  [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).
* **Python 3.10 or later**. The lessons were recorded with Python 3.14.8.
* **curl**, which comes with macOS and most Linux distributions. The lessons were
  recorded with curl 8.23.0.
* **A web browser** for the lessons that visit public security websites.

There is nothing to install: the orders site uses only Python's standard library.
Clone the repository and you are ready:

```bash
git clone https://github.com/paiml/security-fundamentals.git
cd security-fundamentals
python3 --version    # 3.10 or later
```

## How each lesson works

Every terminal lesson has its own folder, holding only what that lesson needs. Most
of them start the orders site, send it requests with `curl`, and stop it:

```bash
cd getting-started                              # 1. Move into the lesson's folder
python3 app.py &                                # 2. Start the site in the background
curl http://127.0.0.1:8000/health               # 3. Send it a request
curl -u alice:wonderland http://127.0.0.1:8000/orders   # 4. Sign in as alice
kill %1                                         # 5. Stop the site
cd ..                                           # back to the root for the next lesson
```

A few conventions help you find your way:

* **The site only listens on this computer** (`127.0.0.1`, port 8000). Nothing in
  these lessons reaches a site or service on the internet, and you should only ever
  try these techniques on systems you own or have written permission to test.
* **The `&` runs the site in the background**, so your terminal is free for `curl`.
  The site starts quietly: your shell prints its job number and process id, such as
  `[1] 12345`, and `curl http://127.0.0.1:8000/health` answers once it is up. Stop it
  with `kill %1` before you leave the folder.
* **Two practice users** can sign in: `alice` with the password `wonderland`, and
  `bob` with `builder`. The site keeps these passwords in plain text so the code stays
  short. Real applications never store passwords like this.
* **The site has a mistake on purpose.** In `getting-started`, `entry-points` and
  `another-users-order`, any signed-in user can read any order. In `access-check` and
  `verify-access` it has the fix, two lines that check who owns the order.
* **The web lessons only visit public pages**, and read them without signing in.
* **[LESSONS.md](LESSONS.md)** lists every command typed in every terminal lesson, in
  order. Use it to follow along, or to replay a lesson without the video.

## Learning path

Work through the sections in order. Each table lists the lessons you can follow along
with, in the terminal or in your browser, and the folder or website each one uses.
The other lessons in each week are ideas, explained in the videos.

### 1. What security means

Security is about protecting what matters: keeping information private, keeping it
correct, and keeping it available. This week is ideas only: what security is, a brief
history of it, the three pillars, and the words security people use. There is nothing
to run yet.

**You will be able to:** say what security is and how it has changed, and name the
three pillars and the principles of least privilege and defense in depth.

**Read more:** NIST's definition of [information security](https://csrc.nist.gov/glossary/term/information_security),
built on [confidentiality](https://csrc.nist.gov/glossary/term/confidentiality),
[integrity](https://csrc.nist.gov/glossary/term/integrity) and
[availability](https://csrc.nist.gov/glossary/term/availability), and the [Security by Design Principles](https://owasp.org/www-project-developer-guide/release/foundations/security_principles/)
from OWASP's Developer Guide.

### 2. Who keeps software safe

Nobody secures software alone. Organizations like OWASP, MITRE, NIST and CISA publish
the lists, names and scores everyone else uses, and every known vulnerability gets an
identifier so people can talk about the same problem. Here you visit the sites that
hold them, and read a real site's security contact.

**You will be able to:** find a site's security contact, look up a
vulnerability by its CVE identifier, read its severity and weakness category, and
check whether attackers are using it.

| Lesson | Where | Study |
|---|---|---|
| Exploring the OWASP Top 10 website | [owasp.org](https://owasp.org/projects/top-ten) | |
| Finding a site's security contact | [github.com/.well-known/security.txt](https://github.com/.well-known/security.txt) | |
| Looking up a real vulnerability record | [cve.org](https://www.cve.org/) | |
| Searching the GitHub Advisory Database | [github.com/advisories](https://github.com/advisories) | |
| Reading a vulnerability's score and weaknesses | [github.com/advisories](https://github.com/advisories/GHSA-jfh8-c2jp-5v3q) | |
| Checking the known exploited vulnerabilities list | [github.com/cisagov/kev-data](https://github.com/cisagov/kev-data) | |

**Try it yourself:** look up Log4Shell, `CVE-2021-44228`, in each place: its record on
cve.org, its entry in CISA's catalog, and its advisory in the GitHub Advisory Database.
Then find it in NIST's [National Vulnerability Database](https://nvd.nist.gov/), one
more place that scores it. Note what each one adds that the others don't.

**Read more:** [RFC 9116](https://www.rfc-editor.org/rfc/rfc9116), the standard
behind `security.txt`; the [OWASP Vulnerability Disclosure Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html);
[CWE](https://cwe.mitre.org/), the list of weakness categories; and
[OSV](https://osv.dev/), an open vulnerability database for open source packages.

### 3. Thinking like an attacker

First, what a web application is, and the practice orders site: you start it, limit
who can read its customers file, and detect a change to that file with a checksum.
Then you think like an attacker, who starts by mapping the ways in and looks for one
that lets them do more than they should. You do the same to the orders site, with its
owner's permission: yours. You list its entry points, read an order that isn't yours, then add
the check that stops it and prove it holds.

**You will be able to:** start the orders site and check it answers, limit a file to
its owner, detect a change to a file with a checksum, list the entry points of a web application, recognize broken
access control, add the missing check, and verify it for the owner, another user and
someone who isn't signed in.

| Lesson | Where | Study |
|---|---|---|
| Starting and verifying a practice orders site | [`getting-started/`](getting-started) | [`app.py`](getting-started/app.py) |
| Checking and limiting who can read a file | [`file-permissions/`](file-permissions) | [`customers.csv`](file-permissions/customers.csv) |
| Checking that a file hasn't changed | [`file-integrity/`](file-integrity) | [`customers.csv`](file-integrity/customers.csv) |
| Exploring the MITRE ATT&CK matrix | [attack.mitre.org](https://attack.mitre.org/) | |
| Listing a web app's entry points | [`entry-points/`](entry-points) | [`app.py`](entry-points/app.py) |
| Viewing another user's order | [`another-users-order/`](another-users-order) | [`app.py`](another-users-order/app.py) |
| Adding the missing access check | [`access-check/`](access-check) | [`app.py`](access-check/app.py) |
| Verifying the access check | [`verify-access/`](verify-access) | [`app.py`](verify-access/app.py) |

**Try it yourself:** in [`file-integrity/`](file-integrity), undo the change by
deleting the last line of `customers.csv` in an editor, and check again with
`sha256sum -c customers.sha256`. Removing exactly what you added brings back `OK`:
the checksum depends only on the file's contents. Then in [`verify-access/`](verify-access), start the site and try the
access check from the other side: sign in as bob and request alice's first order with
`curl -i -u bob:builder http://127.0.0.1:8000/orders/1`. The site should answer
`403 Forbidden`.

**Read more:** [Threat Modeling](https://owasp.org/www-community/Threat_Modeling) from
OWASP, the [Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html),
and the [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

## Troubleshooting

* **`OSError: [Errno 98] Address already in use`:** something else is using port 8000,
  often a copy of the site you didn't stop. Run `jobs` to see it and `kill %1` to stop
  it, or start the site on another port with `PORT=8001 python3 app.py &` and use
  `8001` in your `curl` commands.
* **`curl: (7) Failed to connect to 127.0.0.1 port 8000`:** the site isn't running.
  Start it with `python3 app.py &`, and if you typed `curl` very quickly, run it again.
* **`kill: %1: no such job`:** the site is running in another terminal window. Stop it
  there with Ctrl+C.
* **`401 Unauthorized` when you expected an order:** check the user name and password
  after `-u`; they are `alice:wonderland` and `bob:builder`.
* **`sha256sum: command not found` on macOS:** older versions of macOS don't have it.
  Use `shasum -a 256` instead, with the same arguments.
* **`chmod` doesn't change anything on Windows:** clone the repository inside your WSL
  home folder, not under `/mnt/c`, where Windows decides the permissions.
* **Your `ls -l` output shows a different name and date:** that's expected. The name
  is your user on your computer, and the date is when you cloned the repository.
* **A page on a security website looks different from the video:** these sites update
  often. Look for the same section by its name.

## Where to go next

Keep learning with more courses from Pragmatic AI Labs, on whichever platform you
prefer:

* [**Pragmatic AI Labs platform**](https://ds500.paiml.com): the full catalog of
  courses and hands-on programs
* [**Pragmatic AI Labs on Coursera**](https://www.coursera.org/partners/pragmatic-ai-labs)
* [**Pragmatic AI Labs on edX**](https://www.edx.org/school/ai)

Then put what you learned here into practice:

* Pick an application you work on and ask the three questions: who can read its data,
  how would you notice if the data changed, and what happens if it stops answering.
* Check whether the projects you use publish a security contact, and add one to your
  own.
* Look up the libraries your application depends on in the
  [GitHub Advisory Database](https://github.com/advisories).
* List your application's entry points, and for each one that returns data, find the
  line of code that checks whose data it is.
