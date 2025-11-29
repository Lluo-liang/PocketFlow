---
name: pocketflow-workflow-generator
description: PocketFlow 轻量级工作流生成器 - 基于自然语言描述和 Cookbook 最佳实践,自动生成 PocketFlow 应用代码。支持智能模式识别、代码结构分析、自动化项目初始化。适用于快速创建 Agent、Workflow、RAG 等 LLM 应用。
allowed-tools: [Read, Write, Edit, Bash, Task, Glob, Grep]
---

# PocketFlow 轻量级工作流生成器

## 重要说明

这是一个**轻量级、可迁移**的 PocketFlow 应用生成器,不依赖复杂的外部配置。

核心理念:
- **自包含**: 不依赖 `_shared/agents/` 等外部目录
- **基于示例**: 从 cookbook/ 目录学习最佳实践
- **智能推断**: 自动识别技术栈和项目结构
- **即插即用**: 复制到任何 PocketFlow 项目即可使用

## 触发场景

当用户说以下内容时自动激活:
- "帮我生成一个 PocketFlow 应用..."
- "创建一个XX功能的智能体/工作流..."
- "参考 Cookbook 生成代码..."
- "我需要一个基于 PocketFlow 的XX系统..."
- "快速搭建一个XX应用..."

## ⚡ 执行指令（重要）

当此 Skill 被激活时,请严格按照以下步骤执行:

### 第一步:理解用户需求

**任务**: 从用户描述中提取关键信息

**提取内容**:
- 应用类型: Agent/Workflow/RAG/Map-Reduce/Batch 等
- 核心功能: 用户想要实现的具体功能
- 输入输出: 数据流向和格式
- 特殊需求: 异步/批处理/多智能体等

**输出**: 一份简洁的需求摘要

### 第二步:扫描 Cookbook 目录

**任务**: 扫描 `cookbook/` 目录,找到相似的参考示例

**执行操作**:
```bash
# 列出所有 cookbook 示例
ls -la /path/to/PocketFlow/cookbook/

# 读取相关示例的 README.md 和 main.py
```

**匹配策略**:
- Agent 类型 → 参考 `pocketflow-agent/`
- Workflow 类型 → 参考 `pocketflow-workflow/`
- RAG 类型 → 参考 `pocketflow-rag/`
- Batch 处理 → 参考 `pocketflow-batch/` 或 `pocketflow-batch-node/`
- 异步处理 → 参考 `pocketflow-async-basic/`

**输出**: 1-3个最相关的 cookbook 示例路径

### 第三步:分析参考示例

**任务**: 深入分析参考示例的代码结构

**分析内容**:
1. **Node 设计模式**: 如何划分节点,每个节点的职责
2. **Flow 连接方式**: Action 机制的使用
3. **Shared Store 结构**: 数据如何在节点间传递
4. **工具函数组织**: utils/ 目录的结构
5. **错误处理**: 重试和 fallback 的使用
6. **特殊模式**: Batch/Async/Multi-Agent 的实现方式

**输出**: 设计模式提取文档

### 第四步:设计应用架构

**任务**: 基于需求和参考示例,设计新应用的架构

**设计内容**:
1. **目录结构**:
```
my_app/
├── main.py              # 入口点
├── nodes.py             # 节点定义
├── flow.py              # 流程定义(可选,复杂流程时使用)
├── utils/               # 工具函数
│   ├── __init__.py
│   └── call_llm.py      # LLM 调用等
├── requirements.txt     # 依赖
└── README.md            # 使用说明
```

2. **Shared Store 结构**: 定义数据字段

3. **Node 列表**: 每个节点的名称、类型、职责

4. **Flow 图**: 使用 Mermaid 格式的流程图

**输出**: 架构设计文档(Markdown)

### 第五步:推断项目配置

**任务**: 分析当前环境,推断技术配置

**推断内容**:
- Python 版本 (检查 `python --version`)
- 虚拟环境管理 (检查是否存在 venv/conda)
- PocketFlow 安装位置
- LLM 提供商偏好 (检查环境变量 OPENAI_API_KEY/ANTHROPIC_API_KEY 等)

**输出**: 项目配置建议

### 第六步:生成代码

**任务**: 生成完整的应用代码

**生成顺序**:
1. **requirements.txt**: 列出所有依赖
2. **utils/*.py**: 工具函数(如 call_llm.py)
3. **nodes.py**: 所有节点定义
4. **flow.py** (可选): 复杂流程定义
5. **main.py**: 入口点和示例运行代码
6. **README.md**: 使用说明和示例

**代码风格**:
- 遵循 PocketFlow 的 prep-exec-post 三步模型
- 包含完整的 docstring 和注释
- 每个文件包含 `if __name__ == "__main__"` 测试代码
- 工具函数不捕获异常,利用 Node 的重试机制

**输出**: 完整的项目代码文件

### 第七步:生成文档

**任务**: 生成项目文档和使用说明

**文档内容**:
1. **README.md**:
   - 项目简介
   - 安装步骤
   - 快速开始
   - 配置说明
   - 示例用法
   - 架构说明(包含 Mermaid 图)

2. **inline 注释**:
   - 每个 Node 的详细说明
   - 关键逻辑的解释
   - Shared Store 字段说明

**输出**: 完整的项目文档

### 第八步:质量检查

**任务**: 检查生成的代码质量

**检查项**:
- ✅ 所有 import 都可用
- ✅ Node 遵循 prep-exec-post 模型
- ✅ exec 中不访问 shared
- ✅ BatchNode 的 post 正确处理 exec_res_list
- ✅ AsyncNode 配合 AsyncFlow 使用
- ✅ 工具函数包含测试代码
- ✅ README 完整清晰

**输出**: 质量检查报告

### 第九步:项目初始化(可选)

**任务**: 如果用户需要,帮助初始化项目环境

**初始化步骤**:
```bash
# 创建项目目录
mkdir -p my_app/utils

# 安装依赖
pip install -r my_app/requirements.txt

# 运行测试
cd my_app && python main.py
```

**输出**: 初始化完成确认

## 核心特性

### 🧠 智能模式识别
- 自动识别 Agent/Workflow/RAG/Batch 等模式
- 基于关键词和需求上下文智能匹配
- 无需用户明确指定应用类型

### 📚 Cookbook 模式学习
- 从现有高质量示例中学习设计模式
- 继承 PocketFlow 最佳实践
- 自动应用已验证的代码结构

### 🔍 自动项目推断
- 检测当前 Python 环境
- 识别 LLM 提供商配置
- 推荐合适的依赖和配置

### 🎯 轻量级设计
- 不依赖复杂的外部配置
- 自包含,可迁移到任何项目
- 仅使用 Claude Code 内置工具

### 📦 即插即用
- 复制 skill 文件夹即可使用
- 不需要安装额外依赖
- 兼容所有 PocketFlow 项目

## 依赖说明

### 必需资源
- **PocketFlow Cookbook**: `cookbook/` 目录(作为参考示例)
- **PocketFlow 核心**: `pocketflow/__init__.py`(框架代码)

### 可选资源
- **项目文档**: `docs/` 目录(辅助理解)
- **测试用例**: `tests/` 目录(参考测试模式)

### 工具依赖
- **Claude Code 内置工具**: Read, Write, Edit, Bash, Glob, Grep
- **无需外部 MCP 工具**

## 使用示例

### 示例1: 生成搜索智能体

**用户输入**:
```
帮我生成一个搜索智能体,能够根据用户问题,决定是搜索网络还是直接回答。
```

**执行流程**:
1. 识别为 Agent 类型
2. 参考 `cookbook/pocketflow-agent/`
3. 设计决策节点 + 搜索节点 + 回答节点
4. 生成完整代码到 `search_agent/`

**输出结构**:
```
search_agent/
├── main.py
├── nodes.py
├── utils/
│   ├── call_llm.py
│   └── search_web.py
├── requirements.txt
└── README.md
```

### 示例2: 生成文章写作工作流

**用户输入**:
```
创建一个文章写作工作流: 大纲 → 写作 → 审核 → 优化
```

**执行流程**:
1. 识别为 Workflow 类型
2. 参考 `cookbook/pocketflow-workflow/`
3. 设计线性流程节点
4. 生成完整代码到 `article_writer/`

### 示例3: 生成批量翻译应用

**用户输入**:
```
我需要批量翻译 Markdown 文件,每个文件翻译成多种语言
```

**执行流程**:
1. 识别为 BatchFlow 类型
2. 参考 `cookbook/pocketflow-batch-flow/`
3. 设计批处理流程
4. 生成完整代码到 `batch_translator/`

## 约束和限制

### 强制约束（PROHIBIT）
- ❌ **禁止引用不存在的文件** - 所有路径必须验证
- ❌ **禁止违反 PocketFlow 规范** - 遵循 prep-exec-post 模型
- ❌ **禁止过度工程** - 保持代码简洁
- ❌ **禁止在 exec 中访问 shared** - 严格遵守节点模型

### 必需要求（REQUIRE）
- ✅ **必须扫描 Cookbook 目录** - 学习参考示例
- ✅ **必须生成完整项目结构** - 包括 README 和测试
- ✅ **必须验证代码质量** - 运行质量检查
- ✅ **必须包含详细注释** - 代码可读性优先

### 允许操作（ALLOW）
- ✅ **允许灵活的目录结构** - 根据复杂度调整
- ✅ **允许选择 LLM 提供商** - 支持 OpenAI/Anthropic/本地模型
- ✅ **允许自定义工具函数** - 根据需求扩展

## 质量保证

- ✅ **Cookbook 模式保证** - 继承已验证的设计模式
- ✅ **架构合规检查** - 符合 PocketFlow 规范
- ✅ **代码风格一致** - 遵循项目惯例
- ✅ **完整文档生成** - README 和注释齐全
- ✅ **可运行性验证** - 生成的代码可直接运行

## 适用场景

- ✅ 快速创建 PocketFlow 应用原型
- ✅ 学习 PocketFlow 设计模式
- ✅ 标准化团队开发流程
- ✅ 复用 Cookbook 最佳实践
- ✅ 新项目快速启动

## 不适用场景

- ❌ 非 PocketFlow 框架的项目
- ❌ 需要复杂角色权限系统的企业场景
- ❌ 一次性脚本(不需要完整应用结构)

## 技术亮点

### 1. 轻量级设计
- 仅依赖 Cookbook 示例,无需复杂配置
- 自包含,可随项目迁移

### 2. 智能学习
- 从 Cookbook 中自动提取设计模式
- 基于需求智能匹配参考示例

### 3. 代码生成
- 生成符合规范的完整项目结构
- 包含测试、文档、工具函数

### 4. 质量保证
- 自动质量检查
- 遵循 PocketFlow 最佳实践

### 5. 即插即用
- 复制即用,无需配置
- 兼容所有 PocketFlow 项目

---

**重要提示**:
1. 这是一个轻量级、可迁移的 skill
2. 执行时需要访问 `cookbook/` 目录作为参考
3. 生成的输出是完整的 PocketFlow 应用项目
4. 不依赖复杂的外部配置,即插即用
