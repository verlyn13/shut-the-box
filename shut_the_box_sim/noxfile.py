import nox


@nox.session(reuse_venv=True)
def lint(session):
    session.install("ruff", "black")
    session.run("ruff", "check", ".")
    session.run("black", "--check", ".")


@nox.session(reuse_venv=True)
def typecheck(session):
    session.install("mypy")
    # Only include specific test files to avoid old/deprecated tests
    sources = ["src/stbsim", "tests/test_core.py", "tests/__init__.py"]
    session.run("mypy", *sources)


@nox.session(reuse_venv=True)
def tests(session):
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov=src/stbsim", "tests")
