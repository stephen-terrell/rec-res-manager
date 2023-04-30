import nox


max_line_length = "120"


@nox.session(python="3.10")
def format_black(session):
    session.install("black")
    session.run("black", "--version")
    session.run("black", "src", "tests", "noxfile.py", "--line-length", max_line_length)


@nox.session(python="3.10")
def lint_flake8(session):
    session.install("flake8")
    session.install("Flake8-pyproject")
    session.install("flake8-bugbear")
    session.run("flake8", "--version")
    session.run("flake8", "src", "tests", "noxfile.py", "--max-line-length", max_line_length, "--max-complexity", "10")


@nox.session(python="3.10")
def type_check_mypy(session):
    session.install("mypy")
    session.install("boto3-stubs")  # TODO: how to get this out of here?
    session.run("mypy", "--version")
    session.run("mypy", "src/", "--install-types", "--non-interactive")


@nox.session(python="3.10")
def security_scan_bandit(session):
    session.install("bandit[toml]")
    session.run("bandit", "--version")
    session.run("bandit", "-r", "src/")


@nox.session(python="3.10")
def test_pytest(session):
    session.install("pytest")
    session.install("-r", "tests/requirements.txt")
    session.run("pytest", "--version")
    session.run("pytest", "tests")


@nox.session(python="3.10", tags=["cov"])
def coverage_pytest_cov(session):
    session.install("coverage")
    session.install("-r", "tests/requirements.txt")
    session.run("coverage", "--version")
    session.run("coverage", "run", "-m", "--branch", "--source", "src/", "pytest", "tests")
    session.run("coverage", "html", "-d", "build/coverage/html")
    session.run("coverage", "xml", "-o", "build/coverage/xml/coverage-report.xml")
    session.run("coverage", "report", "--fail-under=45")  # TODO: pathetic
