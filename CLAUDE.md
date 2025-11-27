# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

PocketFlow 是一个仅有 100 行代码的极简 LLM 框架，用于构建智能体（Agents）、工作流（Workflow）、RAG 等 LLM 应用。

**核心理念**：
- **极致轻量**：核心代码仅 100 行（pocketflow/__init__.py），零依赖，零供应商锁定
- **强大表达力**：支持智能体、工作流、RAG、Map-Reduce、批处理、异步等所有主流设计模式
- **智能体编程**：框架设计简洁，便于 AI 辅助人类构建复杂的 LLM 应用

**核心抽象**：Graph（图）+ Shared Store（共享存储）
- Node：处理简单的 LLM 任务
- Flow：通过 Actions（动作）连接节点
- Shared Store：节点间通信的共享数据存储
- Batch：批处理节点/流
- Async：异步节点/流

## 开发环境设置

### 安装依赖
```bash
# 安装框架（开发模式）
pip install -e .

# 运行单个测试
python -m pytest tests/test_flow_basic.py -v

# 运行所有测试
python -m pytest tests/ -v
```

### 项目结构
```
PocketFlow/
├── pocketflow/
│   └── __init__.py          # 核心框架（仅 100 行！）
├── tests/                   # 单元测试
│   ├── test_flow_basic.py
│   ├── test_batch_node.py
│   ├── test_async_flow.py
│   └── ...
├── cookbook/                # 示例应用
│   ├── pocketflow-agent/
│   ├── pocketflow-rag/
│   ├── pocketflow-workflow/
│   └── ...
├── docs/                    # 文档（重要！）
└── .cursor/rules/           # Cursor AI 规则
```

## 核心架构理解

### 1. Node 的三步执行模型

每个 Node 都遵循 `prep -> exec -> post` 三步执行模型：

```python
class MyNode(Node):
    def prep(self, shared):
        # 第一步：从 shared store 读取数据并预处理
        return shared["data"]

    def exec(self, prep_res):
        # 第二步：执行计算逻辑（通常是 LLM 调用）
        # ⚠️ 不要在这里访问 shared
        # ⚠️ 不要捕获异常，让 Node 的重试机制处理
        return call_llm(f"Process: {prep_res}")

    def post(self, shared, prep_res, exec_res):
        # 第三步：将结果写回 shared store
        shared["result"] = exec_res
        return "default"  # 返回 action 决定下一个节点
```

**关键原则**：
- `prep`：只负责读取和预处理数据
- `exec`：只负责计算逻辑，不访问 shared，不捕获异常
- `post`：负责写入数据和决定流程走向

### 2. Flow 的 Action 机制

Flow 通过 Action（字符串）来决定节点之间的转换：

```python
# 默认转换（post 返回 None 或 "default"）
node_a >> node_b

# 条件转换（post 返回特定 action）
check_node - "positive" >> positive_handler
check_node - "negative" >> negative_handler

# 循环（节点可以指向自己或之前的节点）
retry_node - "retry" >> retry_node
retry_node - "success" >> next_node
```

### 3. 通信方式

**Shared Store（主要方式）**：
- 全局共享的数据结构（通常是字典）
- 所有节点通过 `prep()` 读取，通过 `post()` 写入
- 适用于几乎所有场景

**Params（仅用于 Batch）**：
- 每个节点的局部参数，由父 Flow 传递
- 不可变，用于标识任务（如文件名、ID）
- 主要在 BatchFlow 中使用

### 4. 批处理模式

**BatchNode**：
```python
class ProcessFiles(BatchNode):
    def prep(self, shared):
        # 返回可迭代对象
        return shared["files"]  # ["file1.txt", "file2.txt", ...]

    def exec(self, file):
        # 对每个元素执行一次
        return process_single_file(file)

    def post(self, shared, prep_res, exec_res_list):
        # exec_res_list 是所有结果的列表
        shared["results"] = exec_res_list
```

**BatchFlow**：
```python
class ProcessAllFiles(BatchFlow):
    def prep(self, shared):
        # 返回参数字典列表
        return [{"filename": f} for f in shared["files"]]

# BatchFlow 会为每个参数字典运行一次内部流程
```

### 5. 异步模式

**AsyncNode**：使用 `prep_async`、`exec_async`、`post_async`
**AsyncFlow**：必须用 `run_async()` 运行
**AsyncParallelBatchNode**：并行执行所有 exec_async

```python
class AsyncSummary(AsyncNode):
    async def exec_async(self, text):
        return await call_llm_async(f"Summarize: {text}")

# 必须使用 AsyncFlow 包装
flow = AsyncFlow(start=node)
await flow.run_async(shared)
```

## Agentic Coding 工作流

在开发 PocketFlow 应用时，遵循以下步骤：

### 1. 需求分析（Requirements）
- 理解用户需求，判断是否适合用 LLM 解决
- 从用户视角描述问题，而不是列举功能
- 优先实现高价值、低复杂度的功能

### 2. 流程设计（Flow Design）
- 识别适用的设计模式（Agent、Workflow、RAG、Map-Reduce）
- 为每个节点编写一句话描述
- 绘制 Mermaid 流程图
- **核心原则**：如果人类无法明确指定流程，AI 也无法自动化它

### 3. 工具函数（Utilities）
- 识别需要的外部 API 和工具
- 每个工具函数应该：
  - 单独放在一个文件中（如 `utils/call_llm.py`）
  - 包含 `if __name__ == "__main__"` 测试代码
  - 不要在工具函数中捕获异常（让 Node 的重试机制处理）

### 4. 数据设计（Data Design）
- 设计 shared store 的结构
- 简单系统用内存字典，复杂系统用数据库
- 避免数据冗余

### 5. 节点设计（Node Design）
- 为每个节点指定类型（Regular、Batch、Async）
- 描述 prep、exec、post 的职责
- 明确读写哪些数据

### 6. 实现（Implementation）
- **保持简单**：避免过度工程
- **快速失败**：利用 Node 的重试和 fallback 机制
- 添加日志便于调试

### 7. 优化（Optimization）
- 先用人类直觉评估
- 重新设计流程（回到步骤 3）
- 微优化：提示工程、上下文学习

### 8. 可靠性（Reliability）
- 在 exec 中验证输出，增加 max_retries
- 记录所有尝试并可视化
- 添加 LLM 驱动的自我评估节点

## 标准项目结构

```
my_project/
├── main.py              # 入口点
├── nodes.py             # 所有节点定义
├── flow.py              # 流程定义
├── utils/               # 工具函数
│   ├── __init__.py
│   ├── call_llm.py      # LLM 调用
│   └── search_web.py    # 其他工具
├── requirements.txt     # 依赖
└── docs/
    └── design.md        # 设计文档（高层次，无代码）
```

**design.md 应包含**：
- 需求描述
- 流程设计（Mermaid 图）
- 工具函数列表（输入/输出/用途）
- Shared Store 结构
- 每个节点的详细设计（类型、prep、exec、post）

## 设计模式快速参考

### Agent（智能体）
```python
# 决策节点根据上下文选择动作
decide - "search" >> search_node
decide - "answer" >> answer_node
search_node >> decide  # 循环回决策
```

### Workflow（工作流）
```python
# 线性任务分解
outline >> write >> review
```

### RAG（检索增强生成）
```python
# 离线：chunk >> embed >> store
# 在线：embed_query >> retrieve >> generate
```

### Map-Reduce
```python
# BatchNode 处理所有项，然后 reduce
map_node = SummarizeFiles(BatchNode)
reduce_node = CombineSummaries(Node)
map_node >> reduce_node
```

## 测试指南

### 运行测试
```bash
# 单个测试文件
python -m pytest tests/test_flow_basic.py -v

# 特定测试函数
python -m pytest tests/test_flow_basic.py::TestFlowBasic::test_branching_positive -v

# 所有测试
python -m pytest tests/ -v

# 带覆盖率
python -m pytest tests/ --cov=pocketflow --cov-report=html
```

### 测试节点
```python
# 单独测试节点（不运行后续节点）
node.run(shared)  # 只执行 prep->exec->post

# 测试整个流程
flow = Flow(start=node)
flow.run(shared)  # 执行完整流程
```

### 调试技巧
```python
# 在节点中添加日志
class DebugNode(Node):
    def prep(self, shared):
        print(f"Prep: {shared}")
        return shared["data"]

    def exec(self, prep_res):
        print(f"Exec input: {prep_res}")
        result = process(prep_res)
        print(f"Exec output: {result}")
        return result
```

## 常见陷阱和注意事项

### ❌ 不要这样做

**在 exec 中访问 shared**：
```python
def exec(self, prep_res):
    # ❌ 错误
    data = self.shared["data"]
```

**在工具函数中捕获异常**：
```python
def call_llm(prompt):
    try:  # ❌ 错误
        return client.call(prompt)
    except Exception:
        return "error"
```

**在 Batch 模式中混淆 exec_res 和 exec_res_list**：
```python
class MyBatchNode(BatchNode):
    def post(self, shared, prep_res, exec_res):
        # ❌ 错误：BatchNode 的 post 接收 exec_res_list（列表）
        shared["result"] = exec_res
```

**忘记 AsyncNode 必须用 AsyncFlow**：
```python
node = AsyncNode()
flow = Flow(start=node)  # ❌ 错误
flow.run(shared)  # 会报错

# ✅ 正确
flow = AsyncFlow(start=node)
await flow.run_async(shared)
```

### ✅ 最佳实践

**利用 Node 的重试机制**：
```python
class RobustNode(Node):
    def exec(self, prep_res):
        # 在这里验证结果，失败就抛出异常
        result = call_llm(prep_res)
        if not is_valid(result):
            raise ValueError("Invalid result")
        return result

# 创建时指定重试
node = RobustNode(max_retries=3, wait=2)
```

**使用 fallback 优雅降级**：
```python
class SafeNode(Node):
    def exec(self, prep_res):
        return call_llm(prep_res)  # 可能失败

    def exec_fallback(self, prep_res, exc):
        # 所有重试失败后的降级方案
        return "Unable to process, please try again"
```

**分离关注点**：
```python
# ✅ 好的设计
class DataNode(Node):
    def prep(self, shared):
        return read_data()  # 数据操作

    def post(self, shared, prep_res, exec_res):
        write_data(exec_res)  # 数据操作

class ProcessNode(Node):
    def exec(self, prep_res):
        return process(prep_res)  # 纯计算
```

## 示例应用参考

参考 `cookbook/` 目录下的示例：
- `pocketflow-agent/`：搜索智能体
- `pocketflow-workflow/`：文章写作工作流
- `pocketflow-rag/`：检索增强生成
- `pocketflow-batch/`：批量翻译
- `pocketflow-multi-agent/`：多智能体协作

每个示例都包含：
- `README.md`：说明和用法
- `main.py`：入口点
- `nodes.py` 或内联节点定义
- `docs/design.md`（某些示例）：设计文档

## 重要提醒

1. **先读文档**：修改代码前，先阅读 `.cursorrules` 和 `docs/` 中的相关文档
2. **保持简单**：不要过度工程，PocketFlow 的哲学是简洁
3. **测试驱动**：修改核心代码后，运行测试确保不破坏现有功能
4. **设计优先**：对于复杂应用，先编写 `docs/design.md`，再实现代码
5. **参考 cookbook**：不确定如何实现时，参考 cookbook 中的类似示例

## 文档资源

- **核心文档**：`.cursor/rules/guide_for_pocketflow.mdc` 包含完整的 Agentic Coding 指南
- **在线文档**：https://the-pocket.github.io/PocketFlow/
- **GitHub**：https://github.com/The-Pocket/PocketFlow
