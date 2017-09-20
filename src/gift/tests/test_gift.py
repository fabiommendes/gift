import pytest
import gift


def test_project_defines_author_and_version():
    assert hasattr(gift, '__author__')
    assert hasattr(gift, '__version__')
