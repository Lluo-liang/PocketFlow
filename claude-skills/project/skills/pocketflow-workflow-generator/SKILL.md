---
name: pocketflow-workflow-generator
description: PocketFlow 智能 Skill 生成引擎 - 系统架构师主导的元 Skill 系统。基于自然语言描述，参考Cookbook Skills最佳实践，自动生成符合 Claude Skills 标准的定制化 Skill。支持智能角色选择、知识库集成、项目规范推断、约束驱动保证。适用于快速创建各类研发 Skills。
allowed-tools: [Read, Write, Edit, Bash, Task, Glob, Grep]
---

# PocketFlow 智能 Skill 生成引擎

## 重要说明

**这是一个元 Skill（Meta-Skill）**：用于生成其他 Claude Skills，而不是生成原始的 YAML 工作流。

生成的 Skill 遵循 PocketFlow Skills 架构：
- **SKILL.md**: 增强版 Skill 定义（包含详细执行指令）
- **workflow.yaml**: 完整的工作流定义（作为 Skill 的执行引擎）

## 触发场景

当用户说以下内容时自动激活：
- "帮我生成一个 Skill..."
- "我需要创建XX流程的 Skill..."
- "为我的项目定制一个 Skill..."
- "参考Cookbook生成 Skill..."
- "智能生成适合XX场景的 Skill..."
- "基于XX工作流创建 Skill..."

## ⚡ 执行指令（重要）

当此 Skill 被激活时，请严格按照以下步骤执行：

### 第一步：读取完整工作流定义

```
读取当前目录下的 workflow.yaml 文件，该文件包含完整的元工作流定义（3054行）
文件路径：skills/pocketflow/generators/workflow-generator/workflow.yaml
```

**重要性**: 这是一个**元工作流**（Meta-Workflow），用于生成其他工作流，逻辑非常复杂。

### 第二步：理解元工作流结构

workflow.yaml 包含以下关键配置：
- **主导角色**: system_architect（系统架构师）
- **执行模式**: 自主工作流生成（autonomous_workflow_generation）
- **核心能力**:
  - 智能角色选择引擎
  - Cookbook模式学习
  - 知识库集成
  - 项目规范自动推断
  - 约束驱动保证

### 第三步：依赖路径解析

**重要**：workflow.yaml 中的所有依赖路径都是相对于**项目根目录**的：

| workflow.yaml 中的路径 | 实际文件路径（从项目根目录） |
|----------------------|--------------------------|
| `agents/roles/system-architect.yaml` | `agents/roles/system-architect.yaml` |
| `agents/roles/tech-lead.yaml` | `agents/roles/tech-lead.yaml` |
| `agents/roles/*.yaml` | `agents/roles/` (所有角色) |
| `plugins/workflow-domain/` | `plugins/workflow-domain/` |
| `plugins/quality-domain/` | `plugins/quality-domain/` |
| `plugins/business-domain/` | `plugins/business-domain/` |
| `workflows/cookbook/` | `workflows/cookbook/` (参考模式) |

**从 Skill 目录访问这些文件**：
- 使用 `../../_shared/agents/roles/`
- 使用 `../../_shared/plugins/`
- 使用 `../../../workflows/cookbook/` (Cookbook参考)

**特别重要**：此工作流需要**读取整个 cookbook 目录**作为模式参考！

### 第四步：Cookbook Skills 模式学习（关键）

**这是元 Skill 的核心能力**：参考已有的高质量 Skills 作为模式。

#### Skills Cookbook 目录结构
```
skills/pocketflow/cookbook/
├── tdd-pipeline/
│   ├── SKILL.md (增强版，340行)
│   └── workflow.yaml (完整工作流定义)
├── branch-test-generator/
│   ├── SKILL.md (增强版，417行)
│   └── workflow.yaml (完整工作流定义)
└── ... (其他 Skills)
```

#### 学习内容（双层结构）

**1. SKILL.md 编写模式**
- **触发场景设计**: 如何定义自然语言触发条件
- **执行指令结构**: 8-9步详细执行指令的标准格式
- **路径解析说明**: 如何说明依赖文件的路径映射
- **核心特性描述**: 如何展示 Skill 的核心能力
- **使用示例编写**: 如何提供清晰的使用示例
- **约束说明方式**: 如何说明 PROHIBIT/REQUIRE/ALLOW
- **适用场景定义**: 如何明确适用和不适用场景

**2. workflow.yaml 结构模式**
- **角色配置模式**: 主导角色和后台角色的配置
- **阶段设计模式**: 任务阶段的分解和依赖
- **约束驱动模式**: 约束优先级和执行控制
- **质量门禁模式**: 质量标准的设置
- **依赖管理模式**: plugins 和 agents 的引用
- **变量定义模式**: 动态变量的定义和使用

#### 模式提取步骤
```
1. 扫描 skills/pocketflow/cookbook/ 目录
2. 读取所有已转换的 Skills（SKILL.md + workflow.yaml）
3. 分析 SKILL.md 的编写模式和结构
4. 分析 workflow.yaml 的设计模式
5. 提取可复用的双层架构设计
6. 应用到新 Skill 生成
```

**重要**: 现在参考的是 **Skills**，而不是原始的 workflow YAML！

### 第五步：强制约束执行（核心机制）

**这是防止AI随意发挥的关键机制！**

workflow.yaml 中定义了严格的约束规则（`mandatory_constraint_enforcement`）：

#### 工具使用约束
```yaml
- PROHIBIT_UNDEFINED_MCP_TOOLS: 禁止使用未验证的MCP工具
- REQUIRE_TOOL_AVAILABILITY_CHECK: 强制检查工具可用性
- PROHIBIT_EXTERNAL_TOOL_ASSUMPTIONS: 禁止假设外部工具存在
```

**执行时**: 只使用已验证的内置工具（Read, Write, Edit, Bash等）

#### 模板引用约束
```yaml
- REQUIRE_TEMPLATE_EXISTENCE_VALIDATION: 强制验证模板文件存在
- PROHIBIT_FICTIONAL_TEMPLATES: 禁止引用虚构的模板
- REQUIRE_TEMPLATE_DIRECTORY_SCAN: 强制扫描实际模板目录
```

**执行时**: 必须先扫描并验证模板文件实际存在

#### 角色分配约束
```yaml
- REQUIRE_ROLE_DEFINITION_VALIDATION: 强制验证角色定义存在
- PROHIBIT_INVALID_ROLE_COMBINATIONS: 禁止无效的角色组合
- REQUIRE_AUTHORITY_HIERARCHY_VALIDATION: 强制验证权威层次
```

**执行时**: 只使用 `agents/roles/` 中实际存在的角色

#### 架构合规约束
```yaml
- REQUIRE_POCKETFLOW_ARCHITECTURE_COMPLIANCE: 强制遵循PocketFlow 3.0架构
- PROHIBIT_ARCHITECTURE_VIOLATIONS: 禁止违反架构规范
- REQUIRE_COMPONENT_SEPARATION_VALIDATION: 强制验证组件分离
```

**执行时**: 生成的工作流必须符合PocketFlow架构规范

### 第六步：智能角色选择引擎

根据用户需求和工作流类型，智能选择合适的角色组合。

#### 工作流类型与角色映射
```yaml
development: [tech_lead, senior_engineer, quality_expert, sdet]
architecture_design: [system_architect, tech_lead, security_expert]
quality_assurance: [quality_expert, sdet, performance_expert]
security_review: [security_expert, tech_lead, quality_expert]
requirements_analysis: [business_analyst, product_owner, system_architect]
performance_optimization: [performance_expert, senior_engineer]
```

#### 角色选择算法
```
1. 分析用户需求中的关键词
2. 确定工作流类型
3. 匹配必需角色和可选角色
4. 评分并选择最优组合
5. 验证角色协作可行性
```

#### 评分权重
- 工作流上下文匹配: 35%
- 关键词相关性: 25%
- 协作协同效应: 20%
- 权限对齐度: 15%
- 专业化深度: 5%

### 第七步：项目规范自动推断

**新增能力**: 自动分析目标项目，推断技术栈和规范。

#### 推断步骤
```
1. 扫描项目结构（pom.xml, build.gradle, package.json等）
2. 识别技术栈（Java/Spring, Node.js, Python等）
3. 分析测试框架（JUnit, Mockito, Jest等）
4. 检测代码规范（Checkstyle, ESLint等）
5. 推断构建工具（Maven, Gradle, npm等）
```

#### 应用到工作流生成
- 自动配置合适的构建命令
- 选择对应的测试框架配置
- 应用相应的代码质量标准
- 设置合适的目录路径

### 第八步：严格按照元 Skill 定义执行

按照 workflow.yaml 中定义的阶段生成新 Skill：

#### 阶段1：需求理解与意图分析
- 解析用户自然语言需求
- 识别 Skill 类型和目标
- 确定关键功能和约束

#### 阶段2：Cookbook Skills 模式学习
- 扫描 skills/pocketflow/cookbook/ 目录
- 读取相似 Skills 的 SKILL.md 和 workflow.yaml
- 分析双层架构的设计模式
- 提取可复用的结构和规范

#### 阶段3：项目规范推断
- 分析目标项目结构
- 推断技术栈和工具
- 确定适配配置

#### 阶段4：智能角色选择
- 根据 Skill 类型选择角色
- 验证角色定义存在性
- 确定角色协作关系

#### 阶段5：知识库集成
- 扫描 knowledge/ 目录
- 匹配相关的知识文件
- 集成到 Skill 配置

#### 阶段6：SKILL.md 生成（增强版）
- **生成 SKILL.md 文件**（关键步骤）
- 编写触发场景描述
- 生成8-9步详细执行指令
- 创建路径解析映射表
- 编写核心特性说明
- 提供使用示例
- 定义适用场景

#### 阶段7：workflow.yaml 生成
- 生成主导角色配置
- 定义执行阶段
- 配置任务和依赖
- 应用约束规则

#### 阶段8：约束注入与质量验证
- 应用PROHIBIT/REQUIRE/ALLOW约束
- 设置质量门禁
- 验证 Skill 结构完整性
- 检查双层架构一致性

#### 阶段9：Skill 目录结构输出
- 创建 Skill 目录
- 输出 SKILL.md 文件
- 输出 workflow.yaml 文件
- 创建使用说明文档
- 提供示例和测试建议

### 第九步：输出成果

生成的 Skill 包含完整的双层架构：

**1. Skill 目录结构**
```
skills/pocketflow/cookbook/your-skill/
├── SKILL.md          # 增强版 Skill 定义
└── workflow.yaml     # 完整工作流定义
```

**2. SKILL.md 内容**（增强版格式）
- YAML frontmatter（name, description, allowed-tools）
- 触发场景描述
- ⚡ 执行指令（8-9步详细说明）
- 依赖路径解析表
- 核心特性说明
- 工作流阶段概览
- 使用示例
- 质量保证说明
- 适用/不适用场景

**3. workflow.yaml 内容**
- 完整的工作流定义
- 角色驱动执行配置
- 约束驱动保证机制
- 质量门禁设置
- 阶段和任务定义

**4. 文档**
- 使用说明
- 示例和测试建议

## 核心特性

### 🧠 智能角色选择引擎
- **多维度评分**: 基于上下文、关键词、协作、权限的综合评分
- **角色组合优化**: 自动选择最优角色协作组合
- **验证机制**: 确保选择的角色实际存在于系统中
- **协作分析**: 评估角色间协作可行性

### 📚 Cookbook 模式学习
- **模式提取**: 从现有高质量工作流中学习设计模式
- **结构分析**: 分析成功工作流的阶段设计
- **质量标准**: 继承Cookbook级别的质量标准
- **最佳实践**: 自动应用已验证的最佳实践

### 🔍 项目规范自动推断
- **技术栈识别**: 自动识别Java/Node.js/Python等技术栈
- **工具检测**: 检测Maven/Gradle/npm等构建工具
- **框架分析**: 识别Spring/Express/Django等框架
- **规范适配**: 自动适配项目特定的规范和配置

### 🛡️ 强制约束执行
- **工具验证**: 只使用实际可用的工具
- **模板验证**: 强制验证模板文件存在性
- **角色验证**: 确保角色定义真实存在
- **架构合规**: 强制遵循PocketFlow架构规范

### 🎯 知识库智能集成
- **自动发现**: 扫描knowledge目录匹配相关知识
- **语义匹配**: 基于语义相似度选择知识
- **上下文感知**: 根据工作流上下文集成知识
- **合规增强**: 自动注入相关合规要求

### 🎭 角色驱动架构
- **系统架构师主导**: 端到端自主生成流程
- **专家协作**: tech_lead, business_analyst, quality_expert后台支撑
- **层次验证**: 权威层次自动验证
- **职责清晰**: 每个角色有明确的职责范围

## Skill 生成流程

### 输入
用户提供自然语言描述：
```
"我需要一个Spring Boot项目的CI/CD Skill，
包含代码检查、单元测试、构建和部署。"
```

### 处理过程
1. **意图分析**: 识别为"CI/CD类型 Skill"
2. **技术栈**: 识别Spring Boot + Maven
3. **角色选择**: tech_lead, senior_engineer, quality_expert
4. **Cookbook Skills 参考**: 学习现有 Skills 的双层架构模式
5. **阶段设计**: 代码检查 → 测试 → 构建 → 部署
6. **SKILL.md 生成**: 编写增强版 Skill 定义
7. **workflow.yaml 生成**: 创建完整工作流定义
8. **约束注入**: 应用质量门禁和构建约束
9. **知识集成**: 集成Java编码规范
10. **Skill 输出**: 创建完整 Skill 目录结构

### 输出

**skills/pocketflow/cookbook/spring-boot-cicd/SKILL.md**:
```markdown
---
name: pocketflow-spring-boot-cicd
description: Spring Boot CI/CD Pipeline Skill - 技术负责人主导...
allowed-tools: [Read, Write, Edit, Bash, Task, Glob, Grep]
---

# Spring Boot CI/CD Pipeline

## 触发场景
- "执行Spring Boot CI/CD流程..."
- "构建并部署Spring Boot项目..."

## ⚡ 执行指令（重要）

### 第一步：读取完整工作流定义
读取当前目录下的 workflow.yaml...

### 第二步：理解工作流结构
workflow.yaml 包含以下关键配置...

### 第三步：依赖路径解析
... (完整的路径映射表)

... (其余执行指令)
```

**skills/pocketflow/cookbook/spring-boot-cicd/workflow.yaml**:
```yaml
id: spring-boot-cicd-pipeline
title: "Spring Boot CI/CD Pipeline"
primary_role:
  role_id: "tech_lead"
  execution_mode: "autonomous"

stages:
  - id: code-quality-check
  - id: unit-test-execution
  - id: build-and-package
  - id: deployment

constraint_driven_config:
  constraint_priority: ["PROHIBIT", "REQUIRE", "ALLOW"]
```

## 依赖说明

### 核心角色（从 _shared/agents 访问）
- `system-architect.yaml` - 系统架构师（主导角色）
- `tech-lead.yaml` - 技术负责人
- `business-analyst.yaml` - 业务分析师
- `quality-expert.yaml` - 质量专家
- `senior-engineer.yaml` - 高级工程师
- **所有其他角色** - 根据需要动态选择

### 必需插件（从 _shared/plugins 访问）
- `workflow-domain/` - 工作流转换和处理
- `doc-domain/` - 文档处理和模板
- `quality-domain/` - 质量分析引擎
- `infrastructure-domain/` - 基础设施验证
- `business-domain/` - 业务价值分析引擎

### Cookbook Skills 参考（关键依赖）
- `../../../skills/pocketflow/cookbook/` - 所有已转换的 Cookbook Skills
- 用于双层架构模式学习和质量标准参考
- **参考已有 Skills 的 SKILL.md 编写模式**
- **参考已有 Skills 的 workflow.yaml 结构**

### 知识库
- `../../_shared/knowledge/` - 行业知识、标准、规范

## 执行配置

- **执行模式**: 系统架构师主导 + 专家协作
- **生成模式**: 自主工作流生成（autonomous_workflow_generation）
- **约束级别**: 强制约束执行（BLOCKING）
- **模式学习**: Cookbook模式自动学习
- **规范推断**: 自动项目规范推断

## 输出成果

### Skill 目录结构
```
skills/pocketflow/cookbook/your-skill/
├── SKILL.md          # 增强版 Skill 定义（300-500行）
└── workflow.yaml     # 完整工作流定义（根据复杂度）
```

### SKILL.md 文件
- **YAML frontmatter**: name, description, allowed-tools
- **触发场景**: 5-10个自然语言触发示例
- **执行指令**: 8-9步详细指令（关键核心）
  - 读取 workflow.yaml
  - 理解工作流结构
  - 依赖路径解析（完整映射表）
  - 特定步骤（如动态变量、约束执行等）
  - 角色能力调用
  - 输出成果
- **核心特性**: 3-6个核心能力说明
- **工作流阶段概览**: 各阶段简要描述
- **依赖说明**: 角色、插件、约束框架
- **使用示例**: 3种使用方式
- **质量保证**: 质量标准说明
- **适用/不适用场景**: 明确使用范围

### workflow.yaml 文件
- 完整的YAML格式工作流定义
- 符合PocketFlow 3.0架构规范
- 角色驱动执行配置
- 约束驱动保证机制
- 质量门禁设置
- 阶段和任务详细定义

### 文档
- Skill 使用说明
- 角色职责说明
- 执行步骤文档
- 示例和测试建议

## 使用示例

### 示例1：生成CI/CD Skill
```
帮我生成一个Maven项目的CI/CD Skill，需要包含：
1. 代码质量检查（Checkstyle）
2. 单元测试（JUnit + JaCoCo）
3. 构建打包（mvn package）
4. Docker镜像构建
5. 部署到测试环境
```

**输出**: `skills/pocketflow/cookbook/maven-cicd/` 目录，包含 SKILL.md 和 workflow.yaml

### 示例2：生成需求分析 Skill
```
为我的团队创建一个需求分析 Skill，参考PocketFlow的intelligent-requirement-analysis模式，但要适配我们的Python项目。
```

**输出**: `skills/pocketflow/cookbook/python-requirement-analysis/` 目录

### 示例3：生成安全审查 Skill
```
生成一个安全审查 Skill，包含：
- 依赖漏洞扫描
- 代码安全审计
- 配置安全检查
- 安全测试用例
```

**输出**: `skills/pocketflow/cookbook/security-review/` 目录

## 约束和限制

### 强制约束（PROHIBIT）
- ❌ **禁止使用未验证的MCP工具** - 只使用builtin工具
- ❌ **禁止引用虚构的模板** - 必须验证模板存在
- ❌ **禁止无效的角色组合** - 只使用实际存在的角色
- ❌ **禁止违反架构规范** - 必须符合PocketFlow架构

### 必需要求（REQUIRE）
- ✅ **必须扫描Cookbook Skills目录** - 学习现有 Skills 模式
- ✅ **必须生成 SKILL.md 文件** - 增强版格式，包含执行指令
- ✅ **必须生成 workflow.yaml 文件** - 完整工作流定义
- ✅ **必须验证工具可用性** - 检查工具是否可用
- ✅ **必须验证角色存在性** - 确认角色定义存在
- ✅ **必须应用约束机制** - 生成的 Skill 包含约束

### 允许操作（ALLOW）
- ✅ **允许灵活的阶段设计** - 根据需求定制阶段
- ✅ **允许角色组合创新** - 在验证基础上创新组合
- ✅ **允许知识库扩展** - 集成额外的知识文件

## 质量保证

- ✅ **Cookbook Skills 模式保证** - 继承已验证的高质量 Skills 模式
- ✅ **双层架构一致性** - SKILL.md + workflow.yaml 结构一致
- ✅ **增强版 SKILL.md 格式** - 包含完整的8-9步执行指令
- ✅ **强制约束执行** - 防止生成不合规 Skill
- ✅ **角色验证机制** - 确保角色配置正确
- ✅ **架构合规检查** - 符合 PocketFlow + Claude Skills 双重规范
- ✅ **工具可用性验证** - 只使用可用的工具
- ✅ **文件存在性验证** - 确保引用的文件存在

## 工作流详细定义

**完整元工作流定义**：`workflow.yaml` (3054行)

该文件包含：
- 系统架构师主导的角色配置
- 智能角色选择引擎的完整实现
- Cookbook模式学习机制
- 项目规范自动推断逻辑
- 知识库集成引擎
- 强制约束执行机制
- 9个工作流生成阶段的详细定义
- 质量验证和输出规范

**执行时必须严格按照 workflow.yaml 中的定义执行，特别是：**
- 强制约束执行机制（mandatory_constraint_enforcement）
- Cookbook模式学习步骤
- 角色选择算法和评分规则
- 项目规范推断逻辑
- 架构合规验证

## 适用场景

- ✅ 快速创建定制化研发工作流
- ✅ 标准化团队开发流程
- ✅ 适配不同技术栈的项目
- ✅ 复用Cookbook最佳实践
- ✅ 企业级工作流规范化
- ✅ 新项目快速启动

## 不适用场景

- ❌ 简单任务（不需要完整工作流）
- ❌ 一次性脚本（工作流过于复杂）
- ❌ 非结构化任务（难以定义阶段）

## 技术亮点

### 1. 元编程能力
通过 Skill 生成 Skill，实现自动化的自动化

### 2. 双层架构生成
同时生成 SKILL.md（增强版）和 workflow.yaml（完整定义）

### 3. 模式学习机制
从 Cookbook Skills 中学习成功模式，避免重复设计

### 4. 智能角色匹配
多维度评分算法，自动选择最优角色组合

### 5. 约束驱动保证
强制约束执行，防止AI随意发挥产生不可用 Skill

### 6. 自适应配置
自动推断项目规范，无需手动配置

### 7. 知识库增强
智能集成相关知识，提升 Skill 质量

### 8. Claude Skills 标准兼容
生成的 Skill 完全符合 Claude Skills 最佳实践

---

**重要提示**:
1. 这是一个高级元 Skill，用于生成其他 Claude Skills（而非生成原始 YAML 工作流）
2. 执行时需要访问 `skills/pocketflow/cookbook/` 目录学习已有 Skills 模式
3. 生成的输出是**完整的 Skill 目录结构**：SKILL.md + workflow.yaml
4. 请确保 Cookbook Skills、知识库、agents、plugins 路径可访问
