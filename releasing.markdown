To release a new version
========================

* Double-check that tests are passing
* Create a branch `release-$v`
* Double-check the release note is comprehensive
* Edit the release note to include the date for this release
* Bump the version in `flourish/version.py`
* Build and upload to pypi:
    * `make pypi`
    * `twine upload dist/flourish-$v*`
* Push, PR, and merge the branch
* Tag the merge commit
* Copy the release note into the GitHub release page
* Add the next release note template:

```
## NEW_VERSION - UNRELEASED

High level description, if applicable.

#### New

#### Other changes

#### Bug fixes

#### Dependency updates
```
