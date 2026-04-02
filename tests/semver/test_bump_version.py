import pytest
from pyvcc.semver import SemVer


def test_bump_major(feat_breaking_with_text: tuple[str, str]):
    version = SemVer(0, 1, 0)
    message = feat_breaking_with_text[1]
    version.bump_version(message)
    assert str(version) == "1.0.0"


def test_bump_major_2(feat_breaking_with_exclamation: tuple[str, str]):
    version = SemVer(0, 1, 0)
    message = feat_breaking_with_exclamation[1]
    version.bump_version(message)
    assert str(version) == "1.0.0"


def test_bump_minor(feat_commit: tuple[str, str]):
    version = SemVer(0, 1, 0)
    message = feat_commit[1]
    version.bump_version(message)
    assert str(version) == "0.2.0"


def test_bump_patch(fix_commit: tuple[str, str]):
    version = SemVer(0, 1, 0)
    message = fix_commit[1]
    version.bump_version(message)
    assert str(version) == "0.1.1"


def test_no_bump(docs_commit: tuple[str, str]):
    version = SemVer(0, 1, 0)
    message = docs_commit[1]
    version.bump_version(message)
    assert str(version) == "0.1.0"


def test_no_bump_not_conventional(no_cc_bug_number_commit: tuple[str, str]):
    version = SemVer(1, 0, 0)
    message = no_cc_bug_number_commit[1]
    version.bump_version(message)
    assert str(version) == "1.0.0"


def test_no_bump_no_type(no_cc_simple_commit: tuple[str, str]):
    version = SemVer(1, 0, 0)
    message = no_cc_simple_commit[1]
    version.bump_version(message)
    assert str(version) == "1.0.0"


def test_bump_merge():
    version = SemVer(1, 0, 0)
    message = "Merged feat!(xyz): break"
    version.bump_version(message)
    assert str(version) == "2.0.0"


def test_bump_merge2():
    version = SemVer(1, 0, 0)
    message = "Merged feat(xyz): break"
    version.bump_version(message)
    assert str(version) == "1.1.0"


def test_bump_multiple():
    """patch -> minor -> major"""
    version = SemVer(0, 1, 0)

    version.bump_version("fix: Fix login bug")
    assert str(version) == "0.1.1"

    version.bump_version("feat: Add new feature")
    assert str(version) == "0.2.0"

    version.bump_version("feat!: Complete API redesign")
    assert str(version) == "1.0.0"


def test_bump_multiple2():
    """patch -> patch -> major"""
    version = SemVer(0, 1, 0)

    version.bump_version("fix: Fix login bug")
    assert str(version) == "0.1.1"

    version.bump_version("fix: Fix logout bug")
    assert str(version) == "0.1.2"

    version.bump_version("feat: New API\n\nBREAKING CHANGE: Complete API redesign")
    assert str(version) == "1.0.0"


def test_bump_multiple3():
    """patch -> major -> minor"""
    version = SemVer(0, 1, 0)

    version.bump_version("fix: Fix login bug")
    assert str(version) == "0.1.1"

    version.bump_version("feat!: Complete API redesign")
    assert str(version) == "1.0.0"

    version.bump_version("feat: Add new feature")
    assert str(version) == "1.1.0"


def test_bump_multiple4():
    """patch -> patch -> minor"""
    version = SemVer(0, 1, 0)

    version.bump_version("fix: Fix login bug")
    assert str(version) == "0.1.1"

    version.bump_version("fix: Fix logout bug")
    assert str(version) == "0.1.2"

    version.bump_version("feat: Add new feature")
    assert str(version) == "0.2.0"


def test_bump_multiple5():
    """patch -> patch -> minor"""
    version = SemVer(0, 1, 0)

    version.bump_version("fix: Fix login bug")
    assert str(version) == "0.1.1"

    version.bump_version("fix: Fix logout bug")
    assert str(version) == "0.1.2"

    version.bump_version("Fix logout bug")
    assert str(version) == "0.1.2"

    version.bump_version("feat(asdf): Add new feature")
    assert str(version) == "0.2.0"

    version.bump_version("Merge feat!(asdf): break new feature")
    assert str(version) == "1.0.0"


def test_bump_scope_with_slash():
    """Test commit with scope containing slash character"""
    version = SemVer(1, 0, 0)
    message = "feat(api/v2): Add new endpoint"
    version.bump_version(message)
    assert str(version) == "1.1.0"  # Should be MINOR bump


def test_bump_scope_with_hyphen():
    """Test commit with scope containing hyphen"""
    version = SemVer(1, 0, 0)
    message = "fix(core-library): Resolve memory issue"
    version.bump_version(message)
    assert str(version) == "1.0.1"  # Should be PATCH bump


def test_bump_breaking_with_scope():
    """Test breaking change commit with scope"""
    version = SemVer(1, 0, 0)
    message = "feat(api)!: Complete API redesign"
    version.bump_version(message)
    assert str(version) == "2.0.0"  # Should be MAJOR bump


def test_bump_extra_spaces():
    """Test commit with extra spaces after colon"""
    version = SemVer(1, 0, 0)
    message = "feat:    Add new feature with extra spaces"
    version.bump_version(message)
    assert str(version) == "1.1.0"  # Should be MINOR bump


def test_bump_scope_with_underscores():
    """Test commit with scope containing underscores"""
    version = SemVer(1, 0, 0)
    message = "fix(user_auth): Resolve login issue"
    version.bump_version(message)
    assert str(version) == "1.0.1"  # Should be PATCH bump


def test_bump_uppercase_type():
    """Test commit with uppercase type (should handle gracefully)"""
    version = SemVer(1, 0, 0)
    message = "FEAT: Uppercase type commit"
    version.bump_version(message)
    assert str(version) == "1.1.0"  # Should be MINOR bump


def test_bump_trailing_exclamation_in_description():
    """Trailing ! in description is NOT a breaking change indicator"""
    version = SemVer(1, 0, 0)
    message = "feat: Description with breaking change!"
    version.bump_version(message)
    assert str(version) == "1.1.0"  # Should be MINOR bump, not MAJOR


def test_bump_trailing_exclamation_in_fix_description():
    """Trailing ! in fix commit description should NOT trigger MAJOR bump"""
    version = SemVer(1, 0, 0)
    message = "fix: Critical bug fix!"
    version.bump_version(message)
    assert str(version) == "1.0.1"  # Should be PATCH, not MAJOR


def test_bump_no_space_after_colon():
    """Test commit without space after colon (should not match conventional commit spec)"""
    version = SemVer(1, 0, 0)
    message = "feat:Description without space"
    version.bump_version(message)
    assert str(version) == "1.0.0"  # Should NOT bump (no conventional commit match)


def test_breaking_change_null_type():
    """Test is_breaking_change with None type (null safety check)"""
    version = SemVer(1, 0, 0)
    # This tests the null safety check in is_breaking_change method
    # where (type and type[-1] == "!") handles None type gracefully
    message = "Some commit message without conventional format"
    version.bump_version(message)
    assert str(version) == "1.0.0"  # Should NOT bump (no conventional commit match)


def test_parse_semver_str():
    version = SemVer.semver_from_string("1.1.0")
    assert str(version) == "1.1.0"


def test_parse_semver_invalid_str():
    with pytest.raises(Exception) as excinfo:
        SemVer.semver_from_string("1.1.0.2")
    assert "invalid string" in str(excinfo)
