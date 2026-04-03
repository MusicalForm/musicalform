# Changelog

## [0.2.0](https://github.com/MusicalForm/musicalform/compare/v0.1.0...v0.2.0) (2026-04-03)


### Features

* adds AnnotationLabel.from_string() constructor ([ca8a4b1](https://github.com/MusicalForm/musicalform/commit/ca8a4b1a5ac713e90c1202115a3dccd574410879))
* all objects consistently expose .to_label() which is used by .__str__() ([d693b44](https://github.com/MusicalForm/musicalform/commit/d693b446478e1928c099b3c72aaddf9162b21d91))
* enables subscripting AnnotationLabel using convenience method .get_form_label() ([d54fcd4](https://github.com/MusicalForm/musicalform/commit/d54fcd4316e74cfe6dceff9d248263d8c344eb02))
* FancyStrEnum members now have .alias property returning the shortest alias string ([c5d4ee8](https://github.com/MusicalForm/musicalform/commit/c5d4ee8bf9e5fc83a33c9cfcbb94843efdaf06cf))


### Bug Fixes

* prevents warning due to unhandled key "Name" ([efa2511](https://github.com/MusicalForm/musicalform/commit/efa2511eba60eae355b911dc701cdb1d77aa1614))

## 0.1.0 (2026-03-27)


### Features

* sets up CI workflow running tests and using Release Please for automatic version release ([af5812a](https://github.com/MusicalForm/musicalform/commit/af5812ae51f492663dae49d640e7efe12fee0410))


### Bug Fixes

* corrects setup for Release Please! ([e058971](https://github.com/MusicalForm/musicalform/commit/e0589716ed672090a8fb4c63adb8704e6f08d6f4))
