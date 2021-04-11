#!/usr/bin/env python

import base64
import json
import os
import re
from urllib.request import Request
from urllib.request import urlopen

from typing import List
from typing import Union


def get(url: str, headers: dict) -> dict:
    req = Request(url, headers=headers)
    resp = urlopen(req, timeout=30)
    return json.loads(resp.read())


def get_releases() -> List[str]:
    gh_token = os.environ["GH_TOKEN"]
    auth = base64.b64encode(f"AleksaC:{gh_token}".encode()).decode()

    base_url = "https://api.github.com/repos/{}/{}/{}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Basic {auth}",
    }

    cfn_nag_releases = get(
        base_url.format("stelligent", "cfn_nag", "releases"), headers=headers
    )

    hook_tags = get(
        base_url.format("AleksaC", "mirrors-cfn-nag", "tags"),
        headers=headers,
    )

    new_releases = []
    latest = hook_tags[0]["name"]
    for release in cfn_nag_releases:
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
        f"s.add_dependency 'cfn-nag', '{version}'",
    )
    update_file("README.md", r"rev: \'v[0-9]+\.[0-9]+\.[0-9]+\'", f"rev: v{version}")


def push_tag(version: str) -> None:
    os.system(f"./tag.sh {version}")


if __name__ == "__main__":
    releases = get_releases()
    for release in reversed(releases):
        print(f"Adding new release: {release}")
        update_version(release.replace("v", ""))
        push_tag(release)
