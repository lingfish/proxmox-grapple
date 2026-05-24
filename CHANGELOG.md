# Changelog

## [2.0.2] - 2024-08-15

- Documentation updates.

## [2.0.1] - 2024-08-15

- Added environment exposing: `GRAPPLE_PHASE`, `GRAPPLE_MODE`, `GRAPPLE_VMID`, `GRAPPLE_ALL_ARGS`. Fixes #7.

## [2.0.0] - 2024-08-06

- **Breaking change**: Config file schema updated. `script:` replaced with `mode:` + `run:`.
  See README for migration details.
- Fixes GL #5, #6, and GH #6.

## [1.5.5] - 2024-05-16

- New `mode: shell` option, to augment the existing `mode: script` option.
- Switched to `setuptools_scm` for versioning.

## [1.5.4] - 2024-03-02

- Documentation updates.
- Updated pipeline to push to PyPI.

## [1.5.3] - 2024-03-01

- Documentation updates.
- Prepared for PyPI publishing.
- Implemented GitLab matrix builds for Python 3.9 and 3.11.

## [1.5.0] - 2024-03-01

- Initial import.
