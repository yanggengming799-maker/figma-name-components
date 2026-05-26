---
name: figma-name-components
description: |
  给已有 Figma 页面或模块做组件命名审查、批量修正和冲突确认报告。
  触发示例：
  - "用 figma-name-components 给这个页面做组件命名"
  - "批量检查这个 Figma 页面组件名"
  - "修正这页组件命名并生成冲突报告"
  - "audit component names in this Figma page"
  - "rename Figma components and generate a conflict HTML report"
  ✅ 适用：已有 Figma URL / node-id，需要按 Naming_Rules 与 Naming_Component_Notes 审核、修正、出单份 HTML 冲突报告
  ❌ 不适用：纯文本层改名、页面首层分区命名、没有 Figma MCP 时执行写回
metadata:
  short-description: "按 Naming_Rules 字段规则和 Naming_Component_Notes 执行口径命名 Figma 组件"
---

# Figma 组件自动命名

使用这个 skill 时，按项目命名规则审计、确认、修正 Figma 组件命名。

## 作者意图与运行时适配

- 加载方式：manual，通过用户显式调用或 description 命中触发。
- 模型策略：runtime_default，不强制指定模型。
- 工具策略：inherit，按当前 Codex 运行环境继承可用工具。
- 规则来源：本包已内置命名规则文档，默认读取 `references/Naming_Rules.md` 与 `references/Naming_Component_Notes.md`。

## 必读来源

命名前先读取：

- `references/Naming_Rules.md`
- `references/Naming_Component_Notes.md`

来源分工：

- `Naming_Rules.md` 只负责 4 个命名字段和基础命名语法，不直接裁决本项目 Figma 兼容写回时的 machine-side 变体分隔符。
- `Naming_Component_Notes.md` 是本项目全部执行类说明的唯一主入口。
- 用户如果要求调整流程、确认方式、报告样式、`COMPONENT_SET` 处理规则、用户展示文案或保护规则，默认改 `Naming_Component_Notes.md`，不要改 `Naming_Rules.md`。
- 这个 `SKILL.md` 只保留工具编排和最小工作流，不额外维护执行细则；如果这里和 `Naming_Component_Notes.md` 有差异，一律以 `Naming_Component_Notes.md` 为准。
- 每次调用 `use_figma` 前，必须先加载本地 `figma-use` skill，并在 `use_figma` 调用里传 `skillNames: "figma-use"`。

## 最小工作流

### 1. 读取规则

- 先读取两个必读来源。
- 具体的命名范围、跳过规则、`COMPONENT_SET` 处理、`属性名=` 处理、自动修正边界、人工确认边界、HTML 报告字段和写回规则，全部按 `Naming_Component_Notes.md` 执行。

### 2. 建立候选集

- 用 `get_metadata` 理解目标页面或区域的层级。
- 需要补充设计上下文时，用 `get_design_context`。
- 需要视觉比对时，用 `get_screenshot`。
- 候选集除了独立 `COMPONENT` 外，还要按 `Naming_Component_Notes.md` 把父组件内部明显对应独立组件的实现层纳入同名检查与命名流程。
- 如果父组件内部某层只写了基础组件名，没有写出 `=中文变体`，但它明显承载某个具体变体实例，也必须纳入候选集；不要因为它像“容器名”就跳过。
- 如果候选节点是 `INSTANCE`，不能只读取原始 `name`；必须结合 `mainComponent` 与 `componentProperties` 还原它当前实际选中的变体语义，再参与同名检查。
- 候选集和最终校验必须按 `Naming_Component_Notes.md` 执行全量 `INSTANCE` 扫描、写回后实例回扫和零残留校验；没有完成这三步，不允许宣称任务完成。
- `COMPONENT_SET` 只用于读取变体结构和属性名，不是命名或改名目标。
- 但每次执行都必须额外检查：`COMPONENT_SET` 的共享语义名，是否与其子 `COMPONENT` 左侧 `Property name` 一致；如果不一致，必须把这一组子 `COMPONENT` 纳入自动修正计划。

### 3. 生成标准字段

对每个真正需要命名的目标节点生成：

- `display_name`
- `page_id`
- `component_id`
- `variant_id`

生成命名时，必须按 `Naming_Component_Notes.md` 的全局命名优先级执行：在保证 `component_id` 唯一、业务语义明确、变体可区分、长期稳定的前提下尽量简洁，删除无意义重复，但不要压缩到影响 AI 检索或人工理解。

然后运行：

```bash
python3 scripts/build_figma_name.py \
  --display-name "酒店商品卡/酒店名称=2行" \
  --page-id "LIST" \
  --component-id "LIST.HOTEL_CARD.HOTEL_NAME" \
  --variant-id "LONG_TEXT_2_LINES"
```

如果当前节点是承担 Figma 变体识别职责的子 `COMPONENT`，脚本输出的完整名称格式为：`属性名=中文变体｜component_id#variant_id`。

写回时按 `Naming_Component_Notes.md` 处理 `属性名=` 左侧字段：

- 如果当前组内 `Property name` 已与 `COMPONENT_SET` 共享语义名一致，则保留
- 如果不一致，则以 `COMPONENT_SET` 共享语义名为准整体修正该组子 `COMPONENT` 的左侧字段
- 中文侧继续用 `=` 表达变体，英文 machine side 改用 `#` 表达变体

### 4. 分流与输出

- 自动修正和人工确认如何分流，按 `Naming_Component_Notes.md` 执行。
- 遇到“父组件内部实现层只写了基础组件名，但页面里另一处已有同组件家族的具体变体名”时，不能静默跳过；必须先归一化，再决定自动修正或进入确认。
- 给用户展示组件名、标准名、当前名、建议名或修正结果时，始终按 `Naming_Component_Notes.md` 使用“完整名称”。
- 如果需要列出待确认冲突组、自动修正清单、跳过清单或 HTML 标题，也必须直接写完整名称，不能只写英文 `component_id`。
- 生成 HTML 报告前，必须先按 `Naming_Component_Notes.md` 读取并确认样式参考源；如果固定样式节点失效，先在同一 Figma 文件里搜索现存参考节点，再生成报告。
- 需要用户确认时，输出单份 HTML 报告，不写入 Figma 画板。

### 5. 写回

- 只写回真正的命名目标节点。
- 不要重命名 `COMPONENT_SET`。
- 如果是 Figma 变体子组件，仍然直接写回完整名称：`属性名=中文变体｜component_id#variant_id`。
- 不要脱离 `COMPONENT_SET` 语义随意改左侧 `Property name`。
- 如果子 `COMPONENT` 左侧 `Property name` 与其 `COMPONENT_SET` 共享语义名不一致，则这是默认必修项，直接整体修正。
- 右侧的中文变体值和英文 machine id 继续按标准规则修正。
- 写回后必须按 `Naming_Component_Notes.md` 回扫目标范围内所有 `INSTANCE`，同步所有可由 `mainComponent` / `componentProperties` 明确还原的实例名；最终零残留校验未通过时不得结束。

### 6. 结果说明

每次执行结束后，最终回复至少包含：

- 自动修正清单
- 跳过清单
- 待确认冲突组清单
- HTML 报告路径（如果本次生成了报告）
- 写回后 `INSTANCE` 回扫数量、同步数量和未同步残留数量

说明要求：

- 对用户展示组件名时，始终使用完整名称
- 如果某项被跳过是因为它是 `COMPONENT_SET`，要明确说明它是“变体容器，非命名目标”
- 如果本次没有冲突组，也要明确说明“无待确认冲突”
- 如果本次没有未同步实例，也要明确说明“未同步 INSTANCE 残留：0”

## 用户可见名称格式

普通节点：

```text
display_name｜component_id
display_name=中文变体｜component_id#variant_id
```

承担 Figma 变体识别职责的子 `COMPONENT`，用户侧展示格式：

```text
属性名=中文变体｜component_id#variant_id
```

说明：

- Figma 写回时保留 `属性名=`。
- Figma 变体子组件直接利用 `属性名=` 作为中文组件基名，不要重复写成 `属性名=display_name=中文变体｜component_id#variant_id`。
- 用户侧展示完整名称时，按 `Naming_Component_Notes.md` 使用“中文侧 `=`、machine side `#`”版完整短名称。

## 资源

- `references/project_naming_sources.md`
- `references/Naming_Rules.md`
- `references/Naming_Component_Notes.md`
- `references/html_conflict_report_style.md`
- `scripts/build_figma_name.py`
