import re
import sys

import pytest
from subprocrunner import SubprocessRunner


MODULE = "cleanpy"


def print_result(stdout, stderr, expected=None):
    if expected:
        print(f"[expected]\n{expected}")

    print(f"[stdout]\n{stdout}")
    print(f"[stderr]\n{stderr}")


class Test_cli:
    def test_normal_help(self, tmpdir):
        runner = SubprocessRunner([MODULE, "-h"])
        assert runner.run() == 0, runner.stderr

        runner = SubprocessRunner([sys.executable, "-m", MODULE, "-h"])
        assert runner.run() == 0, runner.stderr

    @pytest.mark.parametrize(["log_level_option"], [["--debug"], ["--quiet"], ["--verbose"]])
    def test_normal_log_level(self, tmpdir, log_level_option):
        runner = SubprocessRunner([MODULE, str(tmpdir), log_level_option])
        assert runner.run() == 0, runner.stderr

    def test_normal_single_dir(self, tmpdir):
        p = tmpdir.mkdir("__pycache__").join("dummy.pyc")
        p.write("dummy")

        p = tmpdir.join("test.pyc")
        p.write("dummy")

        runner = SubprocessRunner([MODULE, "-f", str(tmpdir), "-v"])
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

        runner = SubprocessRunner([MODULE, "-f", str(first_dir), str(second_dir), "-v"])
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 2 directories", runner.stderr) is not None

    def test_normal_exclude(self, tmpdir):
        p = tmpdir.mkdir("__pycache__").join("dummy.pyc")
        p.write("dummy")

        p = tmpdir.join("test.pyc")
        p.write("dummy")

        runner = SubprocessRunner([MODULE, "-f", str(tmpdir), "--exclude", "__pycache__", "-v"])
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 1 directories", runner.stderr) is None
        assert re.search("removed 1 files", runner.stderr) is not None

    def test_normal_include_builds(self, tmpdir):
        first_dir, second_dir = make_dirs(tmpdir)
        runner = SubprocessRunner(
            [MODULE, "-f", str(first_dir), str(second_dir), "--debug", "--include-builds"]
        )
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 3 directories", runner.stderr) is not None

    def test_normal_include_envs(self, tmpdir):
        first_dir, second_dir = make_dirs(tmpdir)
        runner = SubprocessRunner(
            [MODULE, "-f", str(first_dir), str(second_dir), "--debug", "--include-envs"]
        )
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 2 directories", runner.stderr) is not None

    def test_normal_include_metadata(self, tmpdir):
        first_dir, second_dir = make_dirs(tmpdir)
        runner = SubprocessRunner(
            [MODULE, "-f", str(first_dir), str(second_dir), "--debug", "--include-metadata"]
        )
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 3 directories", runner.stderr) is not None

    def test_normal_include_tests(self, tmpdir):
        first_dir, second_dir = make_dirs(tmpdir)
        runner = SubprocessRunner(
            [MODULE, "-f", str(first_dir), str(second_dir), "--debug", "--include-testing"]
        )
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 3 directories", runner.stderr) is not None
        assert re.search("removed 1 files", runner.stderr) is not None

    def test_normal_all(self, tmpdir):
        first_dir, second_dir = make_dirs(tmpdir)
        runner = SubprocessRunner([MODULE, "-f", str(first_dir), str(second_dir), "--debug", "-a"])
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        assert re.search("removed 5 directories", runner.stderr) is not None
        assert re.search("removed 1 files", runner.stderr) is not None

    def test_normal_list(self, tmpdir):
        first_dir, second_dir = make_dirs(tmpdir)
        runner = SubprocessRunner([MODULE, "--list", str(first_dir), str(second_dir), "-a"])
        assert runner.run() == 0, runner.stderr

        print_result(stdout=runner.stdout, stderr=runner.stderr)

        targets = runner.stdout.splitlines()
        assert len(targets) == 6
        for target in targets:
            assert str(tmpdir) in target


def make_dirs(dir_obj):
    first_dir = dir_obj.mkdir("first")
    first_dir.mkdir("__pycache__")
    first_dir.mkdir("build")
    first_dir.mkdir("hoge.egg-info")

    second_dir = dir_obj.mkdir("second")
    second_dir.mkdir("__pycache__")
    second_dir.mkdir(".tox")
    f0 = second_dir.join("coverage.xml")

    f0.write("dummy")

    return (first_dir, second_dir)
