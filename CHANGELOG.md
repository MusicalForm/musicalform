# Changelog

## [0.4.0](https://github.com/MusicalForm/musicalform/compare/v0.3.0...v0.4.0) (2026-10-20)


### Features

* **cli:** puts filename first and source_file last in concatenated validation reports ([d1d9d4f](https://github.com/MusicalForm/musicalform/commit/d1d9d4fd9e43c100882c6e9313fc47fef2b04092))
* **cli:** show help instead of an error when no input is given ([af36e44](https://github.com/MusicalForm/musicalform/commit/af36e44f3dbd1c1a101dfc7f19b399fa7eaf3248))
* **core:** implements FunctionalFusion in the same way as FunctionalTransformation (i.e., can come with or without subsequent function in the same label) ([2507277](https://github.com/MusicalForm/musicalform/commit/2507277b3ca979869f8a01abb5900a7a9b8e54a9))
* **grammar:** adds abbreviation "sec" for "section" ([4333c8a](https://github.com/MusicalForm/musicalform/commit/4333c8a5b2e3ac491033719599223f33adef9b8c))
* **grammar:** adds modseq type ([c9ffc3e](https://github.com/MusicalForm/musicalform/commit/c9ffc3e50b8d13bc1348ff9fa382f24390824df4))
* **grammar:** adds SpecificFunctions beginning (beg), middle (mid), and end ([3a360fd](https://github.com/MusicalForm/musicalform/commit/3a360fd246df07277f9f3a35b5bdf8aee31ea944))
* **grammar:** allows all ordinals from 0th -- 99th ([c4f8a49](https://github.com/MusicalForm/musicalform/commit/c4f8a49288af49ce809968031d76646c964a1eb5))
* **grammar:** allows the symbol _ in names ([f37794d](https://github.com/MusicalForm/musicalform/commit/f37794da4fa582524d1eccf4c4f553aa235e43c3))
* **grammar:** cad = cadential phrase; cadi = cadential idea ([1a73e3e](https://github.com/MusicalForm/musicalform/commit/1a73e3e4ddcfbdb1ffd19fb021d63e77e80d0f6b))
* **grammar:** differentiates between combinators (&gt;/) between two functions and at the end of the label ("rightwards") ([a5c3ad0](https://github.com/MusicalForm/musicalform/commit/a5c3ad0dfbc3ae458d62cce86fd9717ec707d4f1))
* **grammar:** implements combination operator & for material references ([70bab62](https://github.com/MusicalForm/musicalform/commit/70bab62452b058d99efb08944e84edac3386d7a1))
* **grammar:** includes the material $operators in the grammar ([1b451ea](https://github.com/MusicalForm/musicalform/commit/1b451eace5f2dfb0fbef88f598504c7b1b34a4c8))
* **grammar:** includes the term contrasting middle ([c2fa1cd](https://github.com/MusicalForm/musicalform/commit/c2fa1cd303af4505d00fefec228d91c392439f11))
* **grammar:** includes the term piece ([48a17e1](https://github.com/MusicalForm/musicalform/commit/48a17e155c9e8a6c8904a79da728c26f0597b9b1))
* **grammar:** now validation expects underscores instead of spaces ([cd51013](https://github.com/MusicalForm/musicalform/commit/cd510131f8070f831024bfa44dddb19dd28ebd6c))


### Bug Fixes

* **cli:** expand ~ in path arguments ([4cdb4fb](https://github.com/MusicalForm/musicalform/commit/4cdb4fb93cf808ee290eb1a6f54db0c8fe2128dc))
* **deps:** exclude DHParser 1.9.8 to keep installs working ([06f418a](https://github.com/MusicalForm/musicalform/commit/06f418a8623ba8f9a8d5224878942be2a14f06ec))
* **grammar:** removes movement (mvt) from SpecificFunction to Unit (was duplicated) ([6589619](https://github.com/MusicalForm/musicalform/commit/6589619a4224c62a105fe76b326fd694153b48f0))
* render material operators in a canonical order ([99e2c36](https://github.com/MusicalForm/musicalform/commit/99e2c36992049f4c8f786add44d47c49083025f2))
* **tilia:** match timeline kinds regardless of spelling ([1caf778](https://github.com/MusicalForm/musicalform/commit/1caf778aa7e7d66f6852d5873423c24a1213923e))


### Documentation

* **grammar:** adds TL;DR for updating the annotation standard ([b3ee5b1](https://github.com/MusicalForm/musicalform/commit/b3ee5b14444bd719900597946b908115085413e2))

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
