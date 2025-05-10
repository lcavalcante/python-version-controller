from pyvc.bump import bump_version, print_semver


def test_bump_major(feat_breaking_with_text: tuple[str, str], initial_version):
    message = feat_breaking_with_text[1]
    bump_version(message, initial_version)
    assert print_semver(initial_version) == "1.0.0"


def test_bump_major_2(feat_breaking_with_exclamation: tuple[str, str], initial_version):
    message = feat_breaking_with_exclamation[1]
    bump_version(message, initial_version)
    assert print_semver(initial_version) == "1.0.0"


def test_bump_minor(feat_commit: tuple[str, str], initial_version):
    message = feat_commit[1]
    bump_version(message, initial_version)
    assert print_semver(initial_version) == "0.2.0"


def test_bump_patch(fix_commit: tuple[str, str], initial_version):
    message = fix_commit[1]
    bump_version(message, initial_version)
    assert print_semver(initial_version) == "0.1.1"


def test_no_bump(docs_commit: tuple[str, str], initial_version):
    message = docs_commit[1]
    bump_version(message, initial_version)
    assert print_semver(initial_version) == "0.1.0"


def test_bump_multiple():
    """patch -> minor -> major"""
    version = {"major": 0, "minor": 1, "patch": 0}

    # First bump patch
    bump_version("fix: Fix login bug", version)
    assert print_semver(version) == "0.1.1"

    # Then bump minor
    bump_version("feat: Add new feature", version)
    assert print_semver(version) == "0.2.0"

    # Finally bump major
    bump_version("feat!: Complete API redesign", version)
    assert print_semver(version) == "1.0.0"


def test_bump_multiple2():
    """patch -> patch -> major"""
    version = {"major": 0, "minor": 1, "patch": 0}

    # First bump patch
    bump_version("fix: Fix login bug", version)
    assert print_semver(version) == "0.1.1"

    # Then bump patch again
    bump_version("fix: Fix logout bug", version)
    assert print_semver(version) == "0.1.2"

    # Finally bump major
    bump_version("feat: New API\n\nBREAKING CHANGE: Complete API redesign", version)
    assert print_semver(version) == "1.0.0"


def test_bump_multiple3():
    """patch -> major -> minor"""
    version = {"major": 0, "minor": 1, "patch": 0}

    # First bump patch
    bump_version("fix: Fix login bug", version)
    assert print_semver(version) == "0.1.1"

    # Then bump major
    bump_version("feat!: Complete API redesign", version)
    assert print_semver(version) == "1.0.0"

    # Finally bump minor
    bump_version("feat: Add new feature", version)
    assert print_semver(version) == "1.1.0"


def test_bump_multiple4():
    """patch -> patch -> minor"""
    version = {"major": 0, "minor": 1, "patch": 0}

    # First bump patch
    bump_version("fix: Fix login bug", version)
    assert print_semver(version) == "0.1.1"

    # Then bump patch again
    bump_version("fix: Fix logout bug", version)
    assert print_semver(version) == "0.1.2"

    # Finally bump minor
    bump_version("feat: Add new feature", version)
    assert print_semver(version) == "0.2.0"
