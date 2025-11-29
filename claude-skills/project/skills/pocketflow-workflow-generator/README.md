# PocketFlow Workflow Generator - 改造说明

## 改造概述

这个 skill 已被改造为**轻量级、可迁移**版本,解决了以下问题:

### 原有问题 ❌
1. **依赖不存在的文件结构**:
   - `_shared/agents/roles/` (不存在)
   - `_shared/plugins/` (不存在)
   - `knowledge/` (不存在)
   - `workflows/cookbook/` (路径错误)

2. **过于复杂**:
   - workflow.yaml 3000+ 行
   - 包含大量针对特定项目的配置
   - 硬编码路径无法迁移

3. **无法复用**:
   - 复制到其他项目无法使用
   - 需要配置复杂的外部依赖

### 改造方案 ✅

1. **自包含设计**:
   - 仅依赖 PocketFlow 项目的 `cookbook/` 目录
   - 不需要 agents/plugins/knowledge 等外部结构
   - 使用 Claude Code 内置工具

2. **简化 workflow.yaml**:
   - 从 3000+ 行简化到 442 行
   - 移除所有不存在的依赖引用
   - 保留核心工作流逻辑

3. **通用化 SKILL.md**:
   - 清晰的9步执行指令
   - 基于 cookbook 示例学习
   - 适用于任何 PocketFlow 项目

## 文件结构

```
pocketflow-workflow-generator/
├── SKILL.md           # 执行指令(354行,清晰明了)
├── workflow.yaml      # 工作流定义(442行,简洁实用)
└── README.md          # 本文件
```

## 核心改进

### 1. 依赖管理

**之前**:
```yaml
role_definition: "$ref: ../../_shared/agents/roles/system-architect.yaml"  # 不存在
plugins_directory: "../../_shared/plugins/"  # 不存在
```

**现在**:
```yaml
requires:
  pocketflow_framework:
    path: "pocketflow/__init__.py"  # 总是存在
  cookbook_directory:
    path: "cookbook/"  # 总是存在
```

### 2. 执行流程

**9步执行流程**:
1. 理解用户需求
2. 扫描 Cookbook 目录
3. 分析参考示例
4. 设计应用架构
5. 推断项目配置
6. 生成代码
7. 生成文档
8. 质量检查
9. 项目初始化(可选)

### 3. Cookbook 匹配

**智能匹配规则**:
```yaml
cookbook_matching:
  keywords_to_examples:
    agent: ["pocketflow-agent", "pocketflow-supervisor"]
    workflow: ["pocketflow-workflow"]
    rag: ["pocketflow-rag"]
    batch: ["pocketflow-batch", "pocketflow-batch-node"]
    # ... 更多匹配规则
```

## 使用方法

### 前置条件

确保你的项目有以下结构:
```
YourProject/
├── pocketflow/
│   └── __init__.py          # PocketFlow 核心
├── cookbook/
│   ├── pocketflow-agent/     # 示例1
│   ├── pocketflow-workflow/  # 示例2
│   └── ...                   # 更多示例
└── claude-skills/
    └── project/
        └── skills/
            └── pocketflow-workflow-generator/  # 本 skill
```

### 激活 Skill

在 Claude Code 中说:
```
"帮我生成一个搜索智能体,能够根据用户问题决定是搜索还是直接回答"
```

或者:
```
"创建一个文章写作工作流: 大纲 → 写作 → 审核"
```

### 预期输出

Skill 会生成完整的项目结构:
```
my_app/
├── main.py              # 入口点
├── nodes.py             # 节点定义
├── utils/
│   ├── __init__.py
│   └── call_llm.py
├── requirements.txt     # 依赖列表
└── README.md            # 使用说明
```

## 迁移到其他项目

### 步骤1: 复制 skill 文件夹

```bash
# 复制整个 skill 目录到目标项目
cp -r pocketflow-workflow-generator /path/to/target/project/claude-skills/project/skills/
```

### 步骤2: 确认依赖

确保目标项目有:
- `cookbook/` 目录(包含 PocketFlow 示例)
- `pocketflow/__init__.py`(PocketFlow 核心框架)

### 步骤3: 直接使用

无需任何配置,直接在 Claude Code 中激活即可!

## 技术亮点

### 1. 零配置
- 不需要配置文件
- 不需要环境变量
- 复制即用

### 2. 智能学习
- 自动从 cookbook 学习设计模式
- 基于关键词智能匹配示例
- 继承最佳实践

### 3. 完整输出
- 生成可直接运行的代码
- 包含完整文档和测试
- 符合 PocketFlow 规范

### 4. 质量保证
- 自动质量检查
- 验证代码规范
- 确保可运行性

## 对比表

| 特性 | 原版本 | 改造版本 |
|-----|--------|---------|
| **文件大小** | 3000+ 行 | 442 行 |
| **外部依赖** | agents, plugins, knowledge | 仅 cookbook |
| **可迁移性** | ❌ 无法迁移 | ✅ 即插即用 |
| **复杂度** | ⚠️ 高度复杂 | ✅ 简洁清晰 |
| **文档完整性** | ⚠️ 分散 | ✅ 集中清晰 |
| **使用门槛** | ⚠️ 需要配置 | ✅ 零配置 |

## 约束和限制

### ✅ 适用场景
- 快速创建 PocketFlow 应用
- 学习 PocketFlow 设计模式
- 标准化开发流程
- 新项目快速启动

### ❌ 不适用场景
- 非 PocketFlow 项目
- 需要复杂角色权限系统
- 一次性脚本

## 质量保证

### 代码质量
- ✅ 遵循 PocketFlow 架构规范
- ✅ prep-exec-post 三步模型
- ✅ 完整的 docstring 和注释
- ✅ 包含测试代码

### 文档质量
- ✅ README 完整清晰
- ✅ 架构图(Mermaid)
- ✅ 使用示例

### 功能质量
- ✅ 生成的代码可直接运行
- ✅ 符合用户需求
- ✅ 继承 Cookbook 最佳实践

## 常见问题

### Q1: 如何添加新的 Cookbook 匹配规则?

编辑 `workflow.yaml` 的 `cookbook_matching` 部分:
```yaml
cookbook_matching:
  keywords_to_examples:
    your_keyword: ["pocketflow-your-example"]
```

### Q2: 生成的代码可以自定义吗?

可以!编辑 `workflow.yaml` 的 `templates` 部分来修改代码模板。

### Q3: 如何处理复杂的多智能体应用?

Skill 会自动匹配 `pocketflow-multi-agent` 示例并学习其模式。

### Q4: 可以生成异步应用吗?

可以!Skill 会识别异步需求并参考 `pocketflow-async-basic` 示例。

## 维护和更新

### 添加新的 Cookbook 示例

当 PocketFlow 项目添加新的 cookbook 示例时:
1. Skill 会自动扫描并发现
2. 可选:更新 `cookbook_matching` 规则以优化匹配

### 更新模板

编辑 `workflow.yaml` 的 `templates` 部分:
```yaml
templates:
  node_template: |
    # 你的自定义节点模板
```

## 贡献

欢迎提交改进建议!

改进方向:
- 更多 Cookbook 匹配规则
- 更丰富的代码模板
- 更智能的需求分析

## 许可

与 PocketFlow 项目相同

---

**改造完成时间**: 2025-11-29
**改造者**: Claude Code
**版本**: 2.0-lightweight
