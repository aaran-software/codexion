# tests/test_generator.py

DEBUG = False  # Set to True for extra output during test failures

def test_install(run_command):
    stdout, stderr, code = run_command("install-app testapp")
    if DEBUG:
        print("STDOUT:", repr(stdout))
        print("STDERR:", repr(stderr))
        print("EXIT CODE:", code)
    assert "installed" in stdout.lower(), f"Expected 'installed' in output, got: {stdout}"


def test_install_force(run_command):
    run_command("install-app testapp")
    stdout, _, _ = run_command("install-app testapp --force")
    assert "overwriting" in stdout.lower(), f"Expected 'Overwriting' in output, got: {stdout}"


def test_list(run_command):
    run_command("install-app testapp")
    stdout, _, _ = run_command("list-apps")
    if DEBUG:
        print("LIST OUTPUT:", repr(stdout))
    assert "testapp" in stdout.lower(), f"Expected 'testapp' in list, got: {stdout}"


def test_reinstall(run_command):
    run_command("install-app testapp")
    stdout, _, _ = run_command("reinstall-app testapp")
    assert "reinstallation of 'testapp' complete" in stdout.lower(), f"Expected reinstall message, got: {stdout}"


def test_uninstall(run_command):
    run_command("install-app testapp")
    stdout, _, _ = run_command("uninstall-app testapp")
    assert "uninstalled" in stdout.lower(), f"Expected 'uninstalled' in output, got: {stdout}"


def test_update(run_command):
    run_command("install-app testapp")
    stdout, _, _ = run_command("update-app testapp")
    assert "updated successfully" in stdout.lower(), f"Expected update message, got: {stdout}"
