# Z-Anatomy 中文版 — Blender 5.0+ 适配与优化

**简体中文** | [English](README.en.md)

基于 [Z-Anatomy 官方项目](https://github.com/Z-Anatomy/Models-of-human-anatomy) 和 [Dean Song 的简体中文版](https://github.com/Dean-Song-1/z-anatomy-)，面向 Blender 5.0 及以上版本进行兼容适配、问题修复和使用体验优化。

原始模型与图谱来自 Z-Anatomy；中文翻译来自 **Dean Song（@Dean-Song-1）**；本项目的适配与优化工作由 **@hendasheng** 完成。详细来源与署名见 [ATTRIBUTION.md](ATTRIBUTION.md)。

![Z-Anatomy 中文版在 Blender 中的项目截图](docs/images/Z-Anatomy-cn-Blender-5.webp)

## 适配与优化

- 调整 HUD 字号调用，并增加中文字体加载逻辑。
- 修复语言列缺失、空译文回退、Key colors 面板判断及无界面区域时的刷新问题。
- 改善选中物体与文本编辑器的联动，处理肌肉起止点名称后缀。
- 完善中文界面、语言下拉切换和中文词条查找。
- 保留集合编号，按编号查找并递归显示系统，调整数字快捷键绑定与大纲展开。
- 整理中文名称应用、补充词条和多语言术语卡。

**版本定位：Blender 5.0+。** 本仓库尚未提供逐版本运行测试记录；“5.0+”表示适配目标，不代表所有后续版本均已验证。

## 下载与安装

1. 在本仓库的 **Releases** 页面下载 **Z-Anatomy-cn-Blender-5.zip**，不用解压。
2. 打开 Blender，点击左上角 **Blender 图标 → 安装应用模板（Install Application Template）**，选择刚下载的 ZIP 文件。
3. 安装完成后，点击 **文件 → 新建 → Z-Anatomy**，即可使用。

以后使用时，同样从 **文件 → 新建 → Z-Anatomy** 打开。

## 仓库内容

| 路径 | 内容 |
|---|---|
| `src/Z-Anatomy/` | 成品包中的模板脚本和主题文件 |
| `patches/01-fixes.patch` | 6 类崩溃与正确性修复 |
| `patches/02-zh-i18n.patch` | 中文界面、字体与文本联动 |
| `patches/03-shortcuts.patch` | 集合显示、快捷键及大纲行为调整 |
| `data/` | 原中文词表、补充词条及应用后的对照表 |
| `ATTRIBUTION.md` | 来源与贡献说明 |
| `UPSTREAM.md` | 与两个来源项目的关系 |
| `RELEASE_NOTES.md` | 可用于 GitHub Release 的说明 |

补丁以模板 `__init__.py` 为目标，按 01、02、03 顺序应用。它们作为改动记录保留；目前未包含将词表完整应用到场景并生成术语卡的自动化脚本，因此**不能仅凭补丁与 CSV 完整重建预构建场景**。完整场景请使用 Release 附件。

原材料记录的覆盖数量为：物体 7036/7184、集合 1719/1944、文字标签 1659/1660，术语卡 3350 条。这些数字尚未在本次发布整理中重新运行统计。

## 许可与署名

- 中文词表来自 Dean Song；数据与文档沿用 CC BY-SA 4.0，见 [LICENSE](LICENSE)。
- 代码补丁的许可说明见 [patches/LICENSE-NOTE.md](patches/LICENSE-NOTE.md)。
- 原始模型及其他第三方内容保留各自许可，见 [License_Song1.txt](License_Song1.txt) 和 [ATTRIBUTION.md](ATTRIBUTION.md)。
- 根目录 LICENSE 不替代模型、代码、字体等第三方内容各自的许可。

## 已知限制

部分名称和场景中的说明文字仍为英文；一个原始文本数据块存在编码问题。中文词表沿用来源项目，尚未进行专业术语逐条校审。
