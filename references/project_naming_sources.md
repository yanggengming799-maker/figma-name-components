# 项目命名来源

命名或重命名任何 Figma 节点前，先读取：

- `references/Naming_Rules.md`
- `references/Naming_Component_Notes.md`

使用规则：

- `Naming_Rules.md` 只负责 4 个核心字段和基础命名语法，是只读字段规范。
- `Naming_Component_Notes.md` 负责全部执行类说明，也是本项目 Figma 可见名称与写回格式的唯一操作说明入口。
- 如果两份文档对“Figma 最终可见名称”或“写回格式”的表述不完全一致，以 `Naming_Component_Notes.md` 为准。
- 如果用户要求调整不命名范围、`属性名=` 处理、自动修正策略、人工确认机制、HTML 报告样式或写回保护规则，默认改 `Naming_Component_Notes.md`，不要改 `Naming_Rules.md`。
- 除非用户明确要求更新文档，否则不要修改这两个文件。

操作时不要在这个参考文件里补写流程细节。所有执行细节统一回到 `Naming_Component_Notes.md` 查看和维护，包括：

- `COMPONENT_SET` 是否跳过
- 用户侧组件名是否展示完整名称
- 中文侧是否保留 `=`、machine side 是否使用 `#`
- HTML 报告字段和输出口径
