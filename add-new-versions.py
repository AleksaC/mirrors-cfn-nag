#!/usr/bin/env python

import os
import re
from typing import List, Union

import requests


def get_releases() -> List[str]:
    base_url = "https://api.github.com/repos/{}/{}/{}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    circleci_cli_releases = requests.get(
        base_url.format("stelligent", "cfn_nag", "releases"), headers=headers
    )

    hook_tags = requests.get(
        base_url.format("AleksaC", "mirrors-cfn-nag", "tags"),
        headers=headers,
    )

    new_releases = []

    if circleci_cli_releases.ok and hook_tags.ok:
        latest = hook_tags.json()[0]["name"]
        for release in circleci_cli_releases.json():
            version = release["tag_name"]
            if version == latest:
                break
            new_releases.append(version)

    return new_releases


def update_file(
    file_path: str, pattern: Union[re.Pattern, str], replacement: str
) -> None:
    with open(file_path, "r+") as f:
        contents = f.read()
        f.seek(0)
        f.write(
            re.sub(
                pattern,
                replacement,
                contents,
            )
        )
        f.truncate()


def update_version(version: str) -> None:
    update_file(
        "pre_commit_fake_gem.gemspec",
        r"s\.add_dependency \'cfn-nag\', \'[0-9]+\.[0-9]+\.[0-9]+\'",
        f"s\.add_dependency 'cfn-nag', '{version}'",
    )
    update_file("README.md", r"rev: \'v[0-9]+\.[0-9]+\.[0-9]+\'", f"rev: v'{version}'")


def push_tag(version: str) -> None:
    os.system(f"./tag.sh {version}")


if __name__ == "__main__":
    releases = get_releases()
    for release in reversed(releases):
        print(f"Adding new release: {release}")
        update_version(release.replace("v", ""))
        push_tag(release)
