# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- The **LICENSE** has been changed from **GPL** to **MIT**.

## [0.9.0] - 2025-11-17

### Added

- Interval and Point now include `tier()` and `textgrid()` methods.
- IntervalTier and PointTier now include a `textgrid()` method.

### Changed

- Rename the parameter **parent** as **textgrid** in Interval and Point classes.
- Move the `textgrid` parameter to the last position in `__init__`.

###  Removed

- The `get_durations()` method is removed. Use `duration()` instead.

## [0.8.0] - 2022-11-21

### Changed

- Interval and Point items require a parent tier.

## [0.7.0] - 2022-11-18

### Added

- Read textgrids from stream
- More documentation

## [0.6.1]


### Fixed

- Write to TextGrid
- Read TextGrid when a tier name is empty


## [0.6.0] - 2022-09-06

### Add

- write() method add if the TextGrid is empty.

## [0.5.0] - 2022-09-26

### Remove

- Methods to manipulate tiers in TextGrid objects.
- Remove write TextGrid as CSV.

## [0.3.3]

## [0.3.2]

## [0.3.1] - 2021-12-19

## [0.2.0]

## [0.1.0] - 2021-10-10

### Added

- Export a TextGrid instance to JSON format

### Fixed

- Return a tier instance when using the insert_tier() methods


