#!/bin/bash
#
# Original script is available at https://github.com/paulfantom/travis-helper/blob/master/releasing/releaser.sh
#
# Tags are generated by searching for a keyword in last commit message. Keywords are:
#  - [patch] or [fix] to bump patch number
#  - [minor], [feature] or [feat] to bump minor number
#  - [major] or [breaking change] to bump major number
# All keywords MUST be surrounded with square braces.
#
# Requirements:
#   - GITHUB_TOKEN variable set with GitHub token. Access level: repo.public_repo
#   - git-semver python package (pip install git-semver)
#
# Note: Exported variables needed by .travis/draft_release.sh
#
# Original script is available at https://github.com/paulfantom/travis-helper/blob/master/releasing/releaser.sh
#
# Copyright: SPDX-License-Identifier: GPL-3.0-or-later
#
# Author  : Pawel Krupa (paulfantom)
# Author  : Pavlos Emm. Katsoulakis (paul@netdata.cloud)

set -e


# If we are not in netdata git repo, at the top level directory, fail
TOP_LEVEL=$(basename "$(git rev-parse --show-toplevel)")
CWD=$(git rev-parse --show-cdup || echo "")
if [ -n "${CWD}" ] || [ ! "${TOP_LEVEL}" == "netdata" ]; then
    echo "Run as .travis/$(basename "$0") from top level directory of netdata git repository"
    echo "Changelog generation process aborted"
    exit 1
fi


# Figure out what will be new release candidate tag based only on previous ones.
# This assumes that RELEASES are in format of "v0.1.2" and prereleases (RCs) are using "v0.1.2-rc0"
function set_tag_release_candidate() {
	LAST_TAG=$(git semver)
	echo "Last tag found is: ${LAST_TAG}"

	if [[ $LAST_TAG =~ -rc* ]]; then
		VERSION=$(echo "$LAST_TAG" | cut -d'-' -f 1)
		LAST_RC=$(echo "$LAST_TAG" | cut -d'c' -f 2)
		RC=$((LAST_RC + 1))
	else
		VERSION="$(git semver --next-minor)"
		RC=0
		echo "Warning: Will set version to ${VERSION} (Last tag: ${LAST_TAG}) while tagged for release candidate generation"
	fi
	GIT_TAG="v${VERSION}-rc${RC}"
}

echo "Determining TAG"

# Check if current commit is tagged or not
GIT_TAG=$(git tag --points-at)

if [ -z "${GIT_TAG}" ]; then
	git semver
	# Figure out next tag based on commit message
	echo "Last commit message: ${TRAVIS_COMMIT_MESSAGE}"
	case "${TRAVIS_COMMIT_MESSAGE}" in
	*"[netdata patch release]"*) GIT_TAG="v$(git semver --next-patch)" ;;
	*"[netdata minor release]"*) GIT_TAG="v$(git semver --next-minor)" ;;
	*"[netdata major release]"*) GIT_TAG="v$(git semver --next-major)" ;;
	*"[netdata release candidate]"*) set_tag_release_candidate ;;
	*)
		echo "Keyword not detected. Exiting..."
		exit 0
		;;
	esac
fi

echo "Setting up GIT_TAG to ${GIT_TAG}"
export GIT_TAG