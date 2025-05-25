import nox


@nox.session(reuse_venv=True)
def lint(session):
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "run", "sh", "scripts/lint.sh", external=True)


@nox.session(reuse_venv=True)
def typecheck(session):
    session.run("uv", "sync", "--dev", external=True)
    session.run("uv", "run", "sh", "scripts/typecheck.sh", external=True)


@nox.session(reuse_venv=True)
def tests(session):
    session.run("uv", "sync", "--dev", external=True)
    session.run(
        "uv",
        "run",
        "pytest",
        "--cov=stbsim",
        "--cov-report=term-missing",
        "--cov-report=html:reports/coverage_html",
        "--cov-fail-under=80",
        "tests",
        external=True,
    )
