"""Replays every lesson in LESSONS.md and checks what it prints.

Each lesson runs in a fresh copy of the repository, in bash, exactly as typed in
the videos. The only changes: the site listens on a free port instead of 8000,
and after starting it in the background the run waits until it answers.
"""

import difflib
import os
import re
import shutil
import signal
import socket
import stat
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# What each lesson must print, in this order.
EXPECTED = {
    "3.1.3": [
        '"status": "ok"',
        '"item": "Notebook"',
        '"item": "Desk lamp"',
    ],
    "3.1.4": ["-rw-r--r--", "customers.csv", "-rw-------", "customers.csv"],
    "3.1.5": [
        "customers.csv: OK",
        "customers.csv: FAILED",
        "WARNING: 1 computed checksum did NOT match",
    ],
    "3.3.2": [
        'if self.path == "/health":',
        'if self.path == "/.well-known/security.txt":',
        'if self.path == "/orders":',
        'if self.path.startswith("/orders/"):',
        "HTTP/1.0 200 OK",
        '"status": "ok"',
        "HTTP/1.0 401 Unauthorized",
        'WWW-Authenticate: Basic realm="orders"',
        '"error": "sign in first"',
    ],
    "3.4.2": [
        '"item": "Notebook"',
        '"item": "Desk lamp"',
        '"owner": "bob"',
        '"item": "Headphones"',
    ],
    "3.4.3": [
        'if order["owner"] != user:',
        'return self.reply(403, {"error": "not your order"})',
        "HTTP/1.0 403 Forbidden",
        '"error": "not your order"',
    ],
    "3.4.4": [
        "HTTP/1.0 200 OK",
        '"item": "Notebook"',
        "HTTP/1.0 403 Forbidden",
        '"error": "not your order"',
        "HTTP/1.0 200 OK",
        '"item": "Headphones"',
        "HTTP/1.0 401 Unauthorized",
        '"error": "sign in first"',
    ],
}

# What a lesson must never print.
NEVER = {
    "3.1.3": ['"owner": "bob"'],
    "3.3.2": ["ORDERS.get"],
    "3.4.3": ['"item": "Headphones"'],
}

# A lesson ends with this exit status; most end with 0. The checksum lesson ends on the failed check.
EXIT_STATUS = {"3.1.5": 1}

# rmedia refuses a recording that shows these, so a lesson must not print them.
REFUSED = {
    "an email address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
    "a home folder path": re.compile(r"/(home|Users)/[A-Za-z0-9._-]+/"),
    "a private key": re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
}

TERMINAL_COLUMNS = 80

ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

# The site has a mistake on purpose, then the fix.
BROKEN = ["getting-started", "entry-points", "another-users-order"]
FIXED = ["access-check", "verify-access"]


def lessons():
    """{id: (title, [commands])} from LESSONS.md."""
    text = (ROOT / "LESSONS.md").read_text()
    found = {}
    for match in re.finditer(r"^## (\d+\.\d+\.\d+) (.+?)\n\n```bash\n(.*?)```", text, re.M | re.S):
        found[match[1]] = (match[2], match[3].strip().splitlines())
    return found


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def run_lesson(commands, workdir, port):
    """Runs the commands in bash, in a terminal as the videos do, and returns what they printed.

    A terminal matters: piped into a file, curl prints a progress meter it never shows on screen.
    """
    script = []
    for command in commands:
        command = command.replace("127.0.0.1:8000", f"127.0.0.1:{port}")
        script.append(command)
        if command.endswith("&"):
            script.append(f"until curl -s -o /dev/null http://127.0.0.1:{port}/health; do sleep 0.1; done")
    (workdir / ".lesson.sh").write_text("\n".join(script) + "\n")
    process = subprocess.Popen(
        ["script", "--quiet", "--return", "--command", "bash .lesson.sh", "/dev/null"],
        cwd=workdir,
        env={**os.environ, "PORT": str(port)},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    try:
        out, _ = process.communicate(timeout=30)
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)  # nothing keeps running after a lesson
        except ProcessLookupError:
            pass
    # The terminal ends lines with \r\n and curl prints header names in bold; keep only the text.
    return process.returncode, ANSI.sub("", out).replace("\r", "")


def assert_in_order(out, expected):
    position = 0
    for piece in expected:
        found = out.find(piece, position)
        assert found >= 0, f"expected {piece!r} after position {position} in:\n{out}"
        position = found + len(piece)


def test_every_lesson_is_checked():
    assert sorted(lessons()) == sorted(EXPECTED)


@pytest.mark.parametrize("lesson", sorted(EXPECTED))
def test_lesson(lesson, tmp_path):
    title, commands = lessons()[lesson]
    workdir = tmp_path / "repo"
    shutil.copytree(ROOT, workdir, ignore=shutil.ignore_patterns(".venv", ".git", "__pycache__", ".pytest_cache"))
    # A fresh clone gets the usual permissions, whatever this copy has now.
    for folder in ["file-permissions", "file-integrity"]:
        (workdir / folder / "customers.csv").chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    status, out = run_lesson(commands, workdir, free_port())

    assert status == EXIT_STATUS.get(lesson, 0), f"{lesson} {title} exited {status}:\n{out}"
    assert_in_order(out, EXPECTED[lesson])
    for piece in NEVER.get(lesson, []):
        assert piece not in out, f"{lesson} printed {piece!r}:\n{out}"
    for what, pattern in REFUSED.items():
        assert not pattern.search(out), f"{lesson} prints {what}, which rmedia refuses:\n{out}"
    for line in out.splitlines():
        assert len(line) <= TERMINAL_COLUMNS, f"{lesson} prints a line wider than {TERMINAL_COLUMNS}: {line!r}"


@pytest.mark.parametrize("copies", [BROKEN, FIXED])
def test_copies_of_the_same_site_are_the_same(copies):
    first = (ROOT / copies[0] / "app.py").read_text()
    for folder in copies[1:]:
        assert (ROOT / folder / "app.py").read_text() == first, folder
        assert (ROOT / folder / "security.txt").read_text() == (ROOT / copies[0] / "security.txt").read_text()


def added_lines(before, after):
    before = (ROOT / before / "app.py").read_text().splitlines()
    after = (ROOT / after / "app.py").read_text().splitlines()
    changes = [line for line in difflib.unified_diff(before, after, lineterm="", n=0)
               if line[:1] in "+-" and not line.startswith(("+++", "---"))]
    assert all(line.startswith("+") for line in changes), "a step only adds lines"
    return [line[1:].strip() for line in changes if line[1:].strip()]


def test_the_fix_is_only_the_access_check():
    assert added_lines(BROKEN[0], FIXED[0]) == [
        'if order["owner"] != user:',
        'return self.reply(403, {"error": "not your order"})',
    ]
