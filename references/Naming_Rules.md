# OTA 设计命名标准

## 1. 适用范围

本标准用于统一：

- OTA 设计白皮书中的组件命名
- Figma 中的组件与关键节点命名
- 结构化 YAML / JSON 中的设计标注
- AI、设计、产品、开发之间的协作引用

本标准只定义 4 个核心字段：

- `display_name`
- `page_id`
- `component_id`
- `variant_id`

## 2. 一句话规则

每个可复用或需要被引用的设计对象，都使用以下 4 个字段：

```yaml
display_name: 酒店商品卡/酒店名称=2行
page_id: LIST
component_id: LIST.HOTEL_CARD.HOTEL_NAME
variant_id: LONG_TEXT_2_LINES
```

对应的 Figma 可见名称统一写成：

```text
酒店商品卡/酒店名称=2行｜LIST.HOTEL_CARD.HOTEL_NAME#LONG_TEXT_2_LINES
```

如果没有状态或变体，则不写 `variant_id`：

```yaml
display_name: 酒店商品卡
page_id: LIST
component_id: LIST.HOTEL_CARD
```

## 3. 核心原则

### 3.1 一字段一职责

- `display_name` 负责给人看
- `page_id` 负责标识页面或场景
- `component_id` 负责标识组件身份
- `variant_id` 在存在状态或取值时负责标识状态或取值

### 3.2 身份和状态必须分开

`component_id` 回答“这是什么”，`variant_id` 回答“它现在是什么状态”。

错误：

```yaml
component_id: LIST.FILTER_BAR.SELECTED_PRICE_STAR_FILTER
```

正确：

```yaml
component_id: LIST.FILTER_BAR.PRICE_STAR_FILTER_TRIGGER
variant_id: SELECTED
```

### 3.3 命名必须稳定

命名不能依赖顺序、位置、颜色、尺寸或临时版本。

错误：

```text
01_LIST_CARD
RIGHT_TOP_RED_LABEL
BIG_PRICE_TEXT
```

正确：

```text
LIST.HOTEL_CARD
LIST.HOTEL_CARD.CAMPAIGN_BADGE
LIST.HOTEL_CARD.FINAL_PRICE
```

### 3.4 命名必须表达业务语义

命名要表达组件在业务中的角色，而不是视觉特征。

错误：

```text
RED_BLOCK
TOP_LEFT_ICON
SMALL_TEXT
```

正确：

```text
LIST.HOTEL_CARD.CAMPAIGN_BADGE
LIST.HOTEL_CARD.FAVORITE_BUTTON
LIST.HOTEL_CARD.LOCATION_TEXT
```

## 4. 四字段定义

### 4.1 `display_name`

`display_name` 是给人看的结构化中文名。

规则：

- 使用中文
- 一层组件直接使用 `模块`
- 子元素使用 `模块/元素`
- 如果当前对象本身就是变体，在末尾使用 `=变体名`
- 只有确实需要补充层级时，才扩展为 `模块/子模块/元素`
- 不写页面
- 不直接写英文状态码
- 不承担唯一身份

示例：

```yaml
display_name: 酒店商品卡
display_name: 酒店商品卡/酒店名称
display_name: 酒店商品卡/酒店名称=2行
```

### 4.2 `page_id`

`page_id` 负责标识页面；在用户明确说明时，也可标识跨页面复用的业务组件或基础资产。

规则：

- 使用英文
- 全大写
- 多词使用下划线连接
- 短、稳定、可复用
- 不使用中文
- 不使用顺序编号

推荐：

```text
HOME
LIST
DETAIL
```

### 4.2.1 共享命名域补充

默认情况下，`page_id` 仍用于页面，例如 `HOME`、`LIST`、`DETAIL`。

但在命名时用户明确说明目标属于共享域时，才允许使用以下补充值代替页面型 `page_id`：

- `COMMON`：跨页面复用的业务组件
- `FOUNDATION`：基础资产，如 `icon`、`divider`、`mask`、`bg`

示例：

```text
COMMON.QUICK_FILTER_BAR.NORMAL_FILTER
FOUNDATION.ICON.CLOSE
FOUNDATION.DIVIDER.HORIZONTAL
```

### 4.3 `component_id`

`component_id` 是最重要的身份字段，用于跨 Figma、白皮书、系统和 AI 稳定引用同一个组件。

规则：

- 使用英文
- 全大写
- 每段内部使用下划线连接
- 段与段之间使用 `.`
- 第一段必须等于 `page_id`，包括用户显式指定的 `COMMON` 或 `FOUNDATION`
- 必须表达业务身份
- 简洁、稳定、具有唯一性
- 不包含状态、顺序、颜色、尺寸、位置、临时版本

语法：

```text
PAGE.MODULE
PAGE.MODULE.SUB_COMPONENT
PAGE.MODULE.SUB_COMPONENT.ELEMENT
```

示例：

```text
LIST.HOTEL_CARD
LIST.HOTEL_CARD.IMAGE_AREA
LIST.HOTEL_CARD.HOTEL_NAME
```

### 4.4 `variant_id`

`variant_id` 负责表达同一组件的状态、取值、布局或内容条件。

规则：

- 使用英文
- 全大写
- 使用下划线连接
- 不承担组件身份
- 只在存在状态、取值、布局差异或内容差异时填写
- 在 Figma 中，只要两个节点 `component_id` 相同但状态不同，就必须用 `variant_id` 区分

示例：

```text
SELECTED
LONG_TEXT_2_LINES
NO_IMAGE
```

## 5. Figma 命名规则

### 5.1 默认格式

Figma 中有变体时，默认使用这一种可见名称格式：

```text
display_name=中文变体｜component_id#variant_id
```

如果没有变体，则写成：

```text
display_name｜component_id
```

示例：

```text
酒店商品卡｜LIST.HOTEL_CARD
酒店商品卡/图片区｜LIST.HOTEL_CARD.IMAGE_AREA
酒店商品卡/酒店名称=2行｜LIST.HOTEL_CARD.HOTEL_NAME#LONG_TEXT_2_LINES
```

### 5.2 分隔符规则

- `display_name` 中层级使用 `/`
- `display_name` 中的变体说明使用 `=`
- `component_id` 内部使用 `.`
- `display_name` 和机器标识之间使用 `｜`
- `component_id` 和 `variant_id` 之间使用 `#`

示例：

```text
酒店商品卡/酒店名称=2行｜LIST.HOTEL_CARD.HOTEL_NAME#LONG_TEXT_2_LINES
```

## 6. 禁用写法

不要把顺序写进身份：

```text
01_LIST_FILTER
02_LIST_CARD
```

不要把状态写进组件身份：

```text
LIST.FILTER_BAR.SELECTED
LIST.HOTEL_CARD.LOADING_PRICE
```

不要用视觉描述代替业务语义：

```text
RED_BLOCK
TOP_LEFT_ICON
SMALL_TEXT
```

不要在 `component_id` 中中英混写：

```text
LIST.酒店卡片
LIST.HOTEL_CARD.金牌
```

不要用临时版本和口语文案：

```text
LIST.HOTEL_CARD.FINAL_COPY
LIST.HOTEL_CARD.NEW_VERSION
LIST.HOTEL_CARD.SUPER_CHEAP_TAG
```

## 7. 结论

这份标准的最终结论很明确：

- 主标准只保留 `display_name`、`page_id`、`component_id`、`variant_id`
- `display_name` 负责人类阅读，有变体时使用 `=变体名`
- `component_id` 负责稳定身份
- `variant_id` 仅在存在变体时负责状态区分
- Figma 有变体时使用 `display_name=中文变体｜component_id#variant_id`
- Figma 无变体时使用 `display_name｜component_id`

这套结构的好处是：

- 对人清楚
- 对 AI 清楚
- 在 Figma 中不重名
- 在白皮书和系统中容易引用
- 后续扩展页面、组件和状态时不需要推翻现有命名体系
