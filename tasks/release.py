"""Handles creating a release PR"""
from __future__ import annotations

import os
from pathlib import Path
from subprocess import check_call

from git import Commit, Head, Remote, Repo, TagReference
from packaging.version import Version

ROOT_SRC_DIR = Path(__file__).parents[1]


def main(version_str: str) -> None:
    version = Version(version_str)
    repo = Repo(str(ROOT_SRC_DIR))

    if repo.is_dirty():
        raise RuntimeError("Current repository is dirty. Please commit any changes and try again.")
    upstream, release_branch = create_release_branch(repo, version)
    try:
        release_commit = release_changelog(repo, version)
        tag = tag_release_commit(release_commit, repo, version)
        print("push release commit")
        repo.git.push(upstream.name, f"{release_branch}:main", "-f")
        print("push release tag")
        repo.git.push(upstream.name, tag, "-f")
    finally:
        print("checkout main to new release and delete release branch")
        repo.heads.main.checkout()
        repo.delete_head(release_branch, force=True)
        upstream.fetch()
        repo.git.reset("--hard", f"{upstream}/main")
    print("All done! ✨ 🍰 ✨")


def create_release_branch(repo: Repo, version: Version) -> tuple[Remote, Head]:
    print("create release branch from upstream main")
    upstream = get_upstream(repo)
    upstream.fetch()
    branch_name = f"release-{version}"
    release_branch = repo.create_head(branch_name, upstream.refs.main, force=True)
    upstream.push(refspec=f"{branch_name}:{branch_name}", force=True)
    release_branch.set_tracking_branch(repo.refs[f"{upstream.name}/{branch_name}"])
    release_branch.checkout()
    return upstream, release_branch


def get_upstream(repo: Repo) -> Remote:
    for remote in repo.remotes:
        if any(url.endswith("xuRebecca/py-learning.git") for url in remote.urls):
            return remote
    raise RuntimeError("could not find xuRebecca/py-learning.git remote")


def release_changelog(repo: Repo, version: Version) -> Commit:
    print("generate release commit")
    cmd = f"towncrier build --yes --config {str(ROOT_SRC_DIR)}/pyproject.toml --version v{version.public}"
    os.system(cmd)
    release_commit = repo.index.commit(f"release {version}")
    return release_commit


def tag_release_commit(release_commit, repo, version) -> TagReference:
    print("tag release commit")
    existing_tags = [x.name for x in repo.tags]
    if version in existing_tags:
        print(f"delete existing tag {version}")
        repo.delete_tag(version)
    print(f"create tag {version}")
    tag = repo.create_tag(version, ref=release_commit, force=True)
    return tag


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="release")
    parser.add_argument("--version", required=True)
    options = parser.parse_args()
    main(options.version)
