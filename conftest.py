import pytest

def pytest_addoption(parser):
    parser.addoption("--with_small", action="store_true", 
            help="Use small-scale data for quick test")

    parser.addoption("--force", action="store_true", 
            help="Force overwriting existing results")


def pytest_generate_tests(metafunc):
    if 'with_small' in metafunc.fixturenames:
        if metafunc.config.option.with_small:
            with_small = True
        else: 
            with_small = False

        metafunc.parametrize("with_small", [with_small])

    if 'force' in metafunc.fixturenames:
        if metafunc.config.option.force:
            force = True
        else: 
            force = False

        metafunc.parametrize("force", [force])


