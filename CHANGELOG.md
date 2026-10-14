# Changelog

## [0.4.0](https://github.com/MusicalForm/musicalform/compare/v0.3.0...v0.4.0) (2026-10-14)


### Features

* **cli:** show help instead of an error when no input is given ([1823878](https://github.com/MusicalForm/musicalform/commit/18238784cee8864029032baf797ad1bb672afa9e))


### Bug Fixes

* **cli:** expand ~ in path arguments ([72f62b0](https://github.com/MusicalForm/musicalform/commit/72f62b0e496aa0a4876c9008f189b84faaa94c8a))
* **deps:** exclude DHParser 1.9.8 to keep installs working ([81118af](https://github.com/MusicalForm/musicalform/commit/81118af0f6e0d5a71093a38f152f5ec37179a816))
* render material operators in a canonical order ([e7b75d7](https://github.com/MusicalForm/musicalform/commit/e7b75d77e3c9a60045552a83741a79e9e9904042))
* **tilia:** match timeline kinds regardless of spelling ([f61965f](https://github.com/MusicalForm/musicalform/commit/f61965ffd76237812d52c5414479813cf9c7fd85))

## [0.3.0](https://github.com/MusicalForm/musicalform/compare/v0.2.0...v0.3.0) (2026-04-27)


### Features

* adds "musicalform convert" command by integrating functionality from the tilia_warp.py script ([848583b](https://github.com/MusicalForm/musicalform/commit/848583be9f6c2e457c6a6527771e58c871acc4e0))

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
