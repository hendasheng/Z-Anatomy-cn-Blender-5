# Blender 5.0+ 适配与优化 · 贡献归属说明

本项目基于 Z-Anatomy 官方项目及 Dean Song 中文版，重点为 Blender 5.0+ 适配与优化。中文翻译归属 Dean Song；下文保留原材料的详细来源记录，其历史统计与分析未在本次发布整理中重新核验。

---

## 一、数据来源（最重要）

| 项目 | 内容 |
|---|---|
| 来源 | PR **#2** "Add Simplified Chinese translation"，作者 **Dean-Song-1** |
| 地址 | https://github.com/Z-Anatomy/Models-of-human-anatomy/pull/2 |
| 分支 / 提交 | `Dean-Song-1:add-chinese-translation` @ `38e0bdb67c6c0ce61354d1b67a6bd9bcece594b5` |
| 实际载体 | 该分支根目录的 `Z-Anatomy.zip` → 包内 `Z-Anatomy/Startup.blend` → 文本数据块 `Translations` |
| 表头 | `English;Latin;Français;Español;Portugues;中文` |
| 行数 | **7284**，中文列全部填满 |
| 提取方式 | 下载该分支 `Z-Anatomy.zip`（87,950,962 字节）→ 解包 → 后台 Blender 打开 `Startup.blend` → 导出 `Translations` 全文 |

**结论：中文对照数据（7284 行）完全来自 Dean-Song-1 的 PR #2，不是本次工作的产物。**

物证文件：`zh_terms_PR2.csv`（该 PR 的 `Translations` 原样拷贝，未做任何修改）。

---

## 二、他的其他贡献

| 内容 | 说明 |
|---|---|
| 语言项改名为 `中文` | 原项目叫 `中國人`（意为"中国人"），他提议改为"中文" |
| `blf.size()` 的 5.x 兼容 | 他在 `Startup.blend` 内嵌的 `z-anatomy.py` **文本副本**里改成 `blf.size(0, font_size)`。注意：App Template 实际执行的是模板目录的 `__init__.py`，那份副本不会被执行，所以该修复在 5.x 下不生效 |
| CJK 字体方向 | 提议 Noto Sans CJK SC；写法为 `'Noto San CJK SC'`（少一个 `s`），且未打包字体文件 |

---

## 三、本次工作（不与上表重复）

### 3.1 应用层

- 把词表真正应用到场景：物体 **7036 / 7184**、集合 **1719 / 1944**、3D 文字标签 **1659 / 1660**
- **保留集合名里的编号前缀**（`1: 骨骼系统` …）：PR #2 的词表键不含编号，直接套用会丢掉编号，而编号是 `1`–`9` 快捷键的语义基础
- 三层归一化匹配（前导空格、`*`、括号、方括号、肌肉起止点 `.e/.o/.e1` 后缀），把覆盖率从 6328 提升到 7036

### 3.2 数据补充（25 行，物证 `zh_terms_supplement.csv`）

- 9 条带编号的顶层系统（`1:Skeletal system` … `9:Reference lines, planes & movements`）
- 2 条原文件缺 `English` 自定义属性的集合（`6:Lymphoid organs`、`Cross section planes`）
- 13 条海报栏目/说明键（`Colors`、`Layers`、`Outliner`、`Display`、`Stored views` 等）
- 1 条说明文本键（`HOW TO ...` → `使用方法`）

### 3.3 对 PR #2 译文的改动：**零**

最终交付物**没有修改 PR #2 的任何一条译文**。核验方式：

```
当前 Translations 与 zh_terms_PR2.csv 逐行比对 → 差异 0 行
```

早期构建确实尝试过 9 条微调（如 `Neck`：颈 → 颈部、`Heart`：心 → 心脏），因**不应擅自改动他人译文**，已全部回退：对照表、物体/集合名、术语卡名与卡片首行、以及本地映射表 `zh_terms.json` 都已还原。

物证 `zh_terms_PR2_adjustments.csv` 现在**只有表头、零数据行**，即"没有发生任何替换"。

> 若将来维护者希望统一命名风格（例如区域名一律用双字），建议单独开 issue 讨论，而不是夹带进功能 PR。

### 3.4 生成内容

- 3350 条中文术语卡（`【中文】/【English】/【Latin】/【Français】/【Español】/【Portugues】`），**全部基于同一张词表**生成，性质是"派生数据"，不是新的翻译成果
- `使用方法`（HOW TO 速查表的中文版，583 字符）

### 3.5 代码修复与功能（`__init__.py`，+421 / −32 行）

| 编号 | 内容 | 归属 |
|---|---|---|
| A1 | 缺语言列时 `KeyError` 崩溃 → 警告并 `CANCELLED` | 本次 |
| A2 | 空单元格回退成空串 → 回退到英文键 | 本次 |
| A3 | Key colors 面板/回调写死 `'.Muscular system'` → 改按数据判断 | 本次 |
| A4 | `msgbus_callback` 按英文数据块名找词条 → 中文优先 + 后缀归一化 | 本次 |
| A5 | 3 处 `context.area.tag_redraw()` 空值保护 | 本次 |
| A6 | `blf.size` 5.x 签名 + `blf.load()` 载入 CJK 字体（4.x 保留三参数回退） | 思路来自他，实现在本次 |
| B1 | UI 中文化（翻译表注册 + 词条表 + 面板/按钮/枚举） | 本次 |
| B2 | 语言面板改下拉、选中即应用、重新应用按钮 | 本次（行为变更） |
| B3 | 文本编辑器按语言切换说明文本 | 本次 |
| C1 | `zanatomy.show_system` + 启动自动重绑 `1`–`0` | 本次（行为变更，需讨论） |

---

## 四、许可（重要，已按作者仓库原文更正）

| 对象 | 许可 | 依据 |
|---|---|---|
| 中文词表 / 他的发布包 | **CC BY-SA 4.0** | 他的仓库 `Dean-Song-1/z-anatomy-` 的 README 与 `License.txt` 明确声明："本项目采用与原始项目相同的 Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) 许可证" |
| 原始模型 | 混合（CC BY-SA 4.0 / CC BY-SA 2.1 JP / CC BY-NC-SA 4.0 等） | 原项目 `License.txt` 的 ATTRIBUTIONS 部分 |
| 本构建的代码改动 | 建议沿用目标仓库条款（`Blender-addons` 为 GPL-3.0） | — |

> 仓库文件对应关系：根目录 `LICENSE` = CC BY-SA 4.0 全文（数据与文档）；
> `patches/LICENSE-NOTE.md` = 说明代码补丁按 GPL-3.0 提供。

**含义：**

1. 引用他的词表必须**署名**（Dean Song / Dean-Song-1）并**保留 CC BY-SA 4.0**；
2. CC BY-SA 的 share-alike 要求派生数据（我们的 3350 条术语卡、25 行补充）**只能以兼容条款再分发**，不能只挂 GPL；
3. 因此提交上游时，数据文件应单独标注 `CC BY-SA 4.0`，代码补丁标注目标仓库条款，两者分开说明。

### 他的发布包 vs 本构建（同一词表，不同应用程度）

他的仓库 `Dean-Song-1/z-anatomy-` 里的 `z-anatomy中文版.zip`（83.2 MB，仅含 `Startup.blend`）实测：

| 项目 | Song-1 发布包 | 本构建 |
|---|---|---|
| 物体中文名 | 6309 / 7184 | **7036 / 7184** |
| 集合中文名 | 1699 / 1944 | **1719 / 1944** |
| 顶层编号系统 | 仍为英文（词表无对应行） | `1: 骨骼系统` …（补 9 行） |
| 中文文本条目 | **0** | 3350 条术语卡 + `使用方法` |
| 思源黑体 | 未打包 | 已打包 |
| 代码修复 | `blf.size` 仅改在 blend 内嵌副本（不生效） | 6 处修复在模板 `__init__.py`（生效） |

> 作者本人在 README 中也写明："中文标签显示对应词典自动化生成，可能有部分与指示部位不恰当，可供参考，但具体请以权威版本为准。" —— 引用时应保留这一质量声明。

---

## 五、如何自行核验

```bash
# 1. 取 PR #2 的词表
curl -L -o za.zip https://raw.githubusercontent.com/Dean-Song-1/Models-of-human-anatomy/add-chinese-translation/Z-Anatomy.zip
unzip -o za.zip "Z-Anatomy/Startup.blend"
# 2. 用 Blender 打开并导出 Translations
blender -b --factory-startup Z-Anatomy/Startup.blend \
  --python-expr "import bpy;open('Translations.txt','w',encoding='utf-8').write(bpy.data.texts['Translations'].as_string())"
# 3. 与 zh_terms_PR2.csv 逐字节比较
diff Translations.txt zh_terms_PR2.csv && echo "完全一致"
```

---

## 六、完整署名链（照录原文，勿删改）

以下内容摘自原项目 `License.txt`（原文见同目录 `License_Song1.txt`，为 Song-1 仓库内的副本）。**任何再分发都必须保留这些署名。**

### 6.1 引用格式（原文件要求的写法）

> **MODELS**
> - **"BodyParts3D - The Database Center for Life Science - CC-BY-SA 2.1 Japan"**
>   （原始模型：https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html）
> - **"Z-Anatomy - The libre 3D atlas of anatomy - CC-BY-SA 4.0"**

被引用/改编的第三方模型：

- "Brainder" 与 "White matter" — University of Washington
- "Cranial Nerves and Foramina" — University of Dundee, CAHID — **CC-BY 4.0**
- "Anatomy of the Inner Ear" — University of Dundee School of Medicine — **CC-BY-NC-SA 4.0**
- "Kidney" — Lissie Cowley — **CC-BY-NC 4.0**

### 6.2 DEFINITIONS

> **"Wikipedia - CC-BY-SA 3.0"** —— 原始网页链接置于每条定义末尾。
> *"Beware the errors created by the automatic translation of the english version."*

> ⚠️ 对我们的直接影响：**我们生成的 3350 条术语卡不含维基正文**（只有中文/英文/拉丁/法/西/葡名称），因此不引入维基内容的 CC BY-SA 3.0 义务；若将来补入中文维基摘要，必须另行标注。
> 原 `License.txt` 本身也警告了英文定义存在机器翻译错误——这一点与我们"术语卡仅供参考"的定位一致。

### 6.3 AUTHORS（原项目，照录）

```
Kousaku OKUBO (Original model 'BodyParts3D')
Gauthier KERVYN (Design, 3D, anatomy)
Marcin ZIELINSKI (Blender add-on)
Lluis VINENT (Unity development)
Ana Teresa BIGIO (Portuguese translation of the anatomical structures)
Carlos TORRES VILLAR (Spanish translation of the anatomical structures)
Paola Perin, Daniele Cossellu, Elisa Vivado (Italian translation of the anatomical structures)
Jadwiga Palosz (Polish translation of the anatomical structures)
Shariar Ahmadpour (Parsi translation of the anatomical structures)
```

### 6.4 简体中文支持的贡献者

| 贡献者 | 内容 | 许可 |
|---|---|---|
| **Dean Song（@Dean-Song-1）** | 简体中文词表 7284 行、`中文` 语言项集成、`blf.size` 兼容思路、发布包 `Dean-Song-1/z-anatomy-` | CC BY-SA 4.0 |

### 6.5 本次构建

| 贡献者 | 内容 |
|---|---|
| **@hendasheng** | 词表应用与归一化匹配、25 行补充词条、3350 条术语卡、`使用方法`、UI 中文化与语言下拉、6 处代码修复、字体打包 |

> 提交 PR 前请把 6.5 的占位符替换成你自己的名字或 GitHub 账号——署名链里不能有空白项。

### 6.6 中文词表的质量声明（原样引用，勿删除）

> *"中文标签显示对应词典自动化生成，可能有部分与指示部位不恰当，可供参考，但具体请以权威版本为准。"*
> —— Dean Song，`Dean-Song-1/z-anatomy-` README

---

## 七、一句话总结

- **数据**：CC BY-SA 4.0，作者 Dean Song，必须署名 + 同许可再分发；
- **模型**：沿用原项目混合许可，引用格式见 6.1；
- **代码**：按目标仓库条款（Blender-addons 为 GPL-3.0）；
- **我们的增量**：应用层、25 行补充、术语卡、UI 与 6 处修复 —— 代码部分不改变词表的许可归属。


