# 设计文档：概念深度讲解器

## 需求

作为学习者，我经常遇到难以理解的概念（编程概念、算法、框架原理等）。
我需要一个智能助手能够：
1. 从多个角度解释概念（是什么、为什么、怎么用）
2. 提供生动的类比和例子
3. 给出实践建议和延伸学习资源

## 流程设计

### 适用设计模式
**Workflow（工作流）** - 将讲解任务分解为多个步骤

### 流程图

```mermaid
flowchart TD
    start[输入概念] --> analyze[分析概念]
    analyze --> explain[生成多角度解释]
    explain --> examples[生成类比和示例]
    examples --> practice[生成实践建议]
    practice --> format[格式化输出]
    format --> end[展示结果]
```

### 节点说明

1. **分析概念节点**：理解概念的类型和难度
2. **生成解释节点**：从"是什么、为什么、怎么用"三个角度解释
3. **生成类比节点**：创建生动的类比和代码示例
4. **实践建议节点**：提供学习路径和练习建议
5. **格式化节点**：整理成易读的 Markdown 格式

## 工具函数

1. **调用 LLM** (`utils/call_llm.py`)
   - 输入：prompt (str)
   - 输出：response (str)
   - 用途：所有节点都需要 LLM 调用

## 数据设计

### Shared Store 结构

```python
shared = {
    "concept": "",          # 用户输入的概念
    "analysis": {},         # 概念分析结果
    "explanation": {},      # 三个角度的解释
    "examples": [],         # 类比和示例
    "practice": {},         # 实践建议
    "final_output": ""      # 最终格式化的输出
}
```

## 节点设计

### 1. 分析概念节点 (AnalyzeConceptNode)
- **类型**：Regular Node
- **步骤**：
  - `prep`：读取 "concept"
  - `exec`：调用 LLM 分析概念类型（编程概念/算法/框架/理论等）和难度级别
  - `post`：写入 "analysis"

### 2. 生成解释节点 (GenerateExplanationNode)
- **类型**：Regular Node
- **步骤**：
  - `prep`：读取 "concept" 和 "analysis"
  - `exec`：调用 LLM 生成三个角度的解释
  - `post`：写入 "explanation"

### 3. 生成示例节点 (GenerateExamplesNode)
- **类型**：Regular Node
- **步骤**：
  - `prep`：读取 "concept" 和 "explanation"
  - `exec`：调用 LLM 生成类比和代码示例
  - `post`：写入 "examples"

### 4. 生成实践建议节点 (GeneratePracticeNode)
- **类型**：Regular Node
- **步骤**：
  - `prep`：读取 "concept" 和 "analysis"
  - `exec`：调用 LLM 生成学习路径和练习建议
  - `post`：写入 "practice"

### 5. 格式化输出节点 (FormatOutputNode)
- **类型**：Regular Node
- **步骤**：
  - `prep`：读取所有生成的内容
  - `exec`：格式化为 Markdown
  - `post`：写入 "final_output" 并打印
