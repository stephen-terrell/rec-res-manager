import nox


max_line_length = "120"
python_versions = ["3.10"]
minimum_coverage_percent = 40  # TODO: pathetic


@nox.session(python=python_versions)
def format_black(session):
    session.install("black")
    session.run("black", "--version")
    if session.interactive:
        session.run("black", "src", "tests", "noxfile.py", "--line-length", max_line_length)
    else:
        session.run("black", "src", "tests", "noxfile.py", "--check", "--diff", "--line-length", max_line_length)


@nox.session(python=python_versions)
def lint_flake8(session):
    session.install("flake8")
    session.install("flake8-bugbear")
    session.run("flake8", "--version")
    session.run("flake8", "src", "tests", "noxfile.py", "--max-line-length", max_line_length, "--max-complexity", "10")


@nox.session(python=python_versions)
def type_check_mypy(session):
    session.install("mypy")
    session.install("boto3-stubs")  # TODO: how to get this out of here?
    session.run("mypy", "--version")
    session.run("mypy", "src/", "--install-types", "--non-interactive")


@nox.session(python=python_versions)
def security_scan_bandit(session):
    session.install("bandit[toml]")
    session.run("bandit", "--version")
    session.run("bandit", "-r", "src/")


@nox.session(python=python_versions, tags=["test"])
def test_pytest(session):
    session.install("pytest")
    session.install("-r", "tests/requirements.txt")
    session.install("pytest-html")
    session.run("pytest", "--version")
    session.run(
        "pytest", "-v", "--html=build/unit-test/html/index.html", "--junitxml=build/unit-test/xml/junit.xml", "tests"
    )


@nox.session(python=python_versions, tags=["cov"])
def coverage_pytest_cov(session):
    session.install("coverage")
    session.install("-r", "tests/requirements.txt")
    if session.interactive:
        session.run("rm", "-rf", "./build/coverage")  # leftover files can skew coverage numbers
    session.run("coverage", "--version")
    session.run("coverage", "run", "--branch", "--source", "src/", "-m", "pytest", "tests")
    if session.interactive:
        session.run("coverage", "html", "-d", "build/coverage/html")
        session.run("coverage", "report", "-m", f"--fail-under={minimum_coverage_percent}")
    else:
        session.run(
            "coverage",
            "xml",
            "-o",
            "build/coverage/xml/coverage-report.xml",
            f"--fail-under={minimum_coverage_percent}",
        )
