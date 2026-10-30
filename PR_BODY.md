# Blender 5.0+ compatibility fixes and Chinese workflow improvements

## Background
Based on Z-Anatomy and Dean Song's Simplified Chinese edition.
Chinese translation is credited to @Dean-Song-1; this contribution focuses on Blender 5.0+ adaptation and workflow improvements.

## Changes
1. Fix missing language columns and empty-cell name fallback.
2. Correct Key colors availability checks.
3. Improve text lookup, including muscle attachment suffixes.
4. Guard redraw calls when no area is available.
5. Update HUD font-size calls and CJK font handling.
6. Improve language selection, localized UI and text-editor synchronization.
7. Adjust numbered-system isolation, startup shortcut binding and Outliner expansion.

Patches are separated into fixes, Chinese UI support and shortcut behavior changes. The latter should be reviewed separately.

## Data and attribution
The 7284-row Chinese vocabulary comes from Dean Song, with 25 supplementary rows supplied by this project. The adjustments file currently contains no data rows.
Original model and third-party attribution are retained in ATTRIBUTION.md and License_Song1.txt.

## Validation
This publication pass inspected the package and documentation. Runtime behavior and translation coverage have not been revalidated in Blender.
The scene-generation script is not included, so patches and CSV files alone do not reproduce the complete scene. Use the release asset for the prepared scene.

## Sources
- https://github.com/Z-Anatomy/Models-of-human-anatomy
- https://github.com/Dean-Song-1/z-anatomy-

