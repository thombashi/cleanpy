import re

import pytest
from subprocrunner import SubprocessRunner


def print_result(stdout, stderr, expected=None):
    if expected:
        print(f"[expected]\n{expected}")

    print(f"[stdout]\n{stdout}")
    print(f"[stderr]\n{stderr}")


class Test_cli:
    def test_normal_help(self, tmpdir):
        runner = SubprocessRunner(["cleanpy", "-h"])
        assert runner.run() == 0, runner.stderr

    @pytest.mark.parametrize(["log_level_option"], [["--debug"], ["--quiet"], ["--verbose"]])
    def test_normal_log_level(self, tmpdir, log_level_option):
        runner = SubprocessRunner(["cleanpy", str(tmpdir), log_level_option])
        assert runner.run() == 0, runner.stderr

    def test_normal_single_dir(self, tmpdir):
        p = tmpdir.mkdir("__pycache__").join("dummy.pyc")
        p.write("dummy")

        p = tmpdir.join("test.pyc")
        p.write("dummy")

        runner = SubprocessRunner(["cleanpy", str(tmpdir), "-v"])
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 1 directories", runner.stderr) is not None
        assert re.search("removed 1 files", runner.stderr) is not None

    def test_normal_multi_dir(self, tmpdir):
        first_dir = tmpdir.mkdir("first")
        first_dir.mkdir("__pycache__")
        first_dir.mkdir("build")

        second_dir = tmpdir.mkdir("second")
        second_dir.mkdir("__pycache__")

        runner = SubprocessRunner(["cleanpy", str(first_dir), str(second_dir), "-v"])
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 2 directories", runner.stderr) is not None

    def test_normal_exclude(self, tmpdir):
        p = tmpdir.mkdir("__pycache__").join("dummy.pyc")
        p.write("dummy")

        p = tmpdir.join("test.pyc")
        p.write("dummy")

        runner = SubprocessRunner(["cleanpy", str(tmpdir), "--exclude", "__pycache__", "-v"])
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 1 directories", runner.stderr) is None
        assert re.search("removed 1 files", runner.stderr) is not None
