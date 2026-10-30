# Changelog

[简体中文](CHANGELOG.md)

## v1.0.1 — 2026-10-30

### Features and usability

- Replace viewport geometry for 1,659 valid text objects with UI text drawing, retaining original content, anchors, and object/collection visibility rules.
- Scale text with the view using its original scene size, with a maximum font size. Remove fixed-size mode.
- Use UI text by default. Keep only the maximum font-size setting in the panel; remove the original-label switch and explanatory labels.
- Restore original text for file saving and final rendering, then resume UI drawing. Preserve underlying text data and leader lines.
- Leave the original text block with invalid encoding unchanged.

### Performance optimization and validation

Blender 5.2.0 LTS, same Startup.blend, 1,659 valid text objects. Tag text data for update and update the view layer eight times; discard the first two samples and report the median of the remaining six.

| Metric | Original 3D text | UI mode |
|---|---:|---:|
| Evaluated text vertices | 1,043,994 | 0 |
| Evaluated text triangles | 1,030,936 | 0 |
| Median forced text geometry update | 118.63 ms | 84.65 ms |

The measured update time fell by approximately 29%. This is not a 29% viewport FPS gain. The benchmark excludes UI drawing cost and does not imply all text was visible simultaneously. The user reported smoother interaction; a complete viewport FPS benchmark is not yet available.

### Current limitations

UI text does not yet support partial occlusion by models and appears in front of them. No per-character ray casting or text texture cache is used. Layout may differ from the original 3D text.

## v1.0.0 — 2026-10-30

Initial Blender 5.0+ Chinese compatibility and usability release: language-column and empty-cell fixes, HUD font calls, Key colors checks, text synchronization, Chinese UI, collection visibility, and number shortcuts. Based on official Z-Anatomy and Dean Song's Chinese edition, retaining source credits and licenses.
