"""
学习讲解器的节点定义
"""
from pocketflow import Node
from utils.call_llm import call_llm
import yaml


class AnalyzeConceptNode(Node):
    """分析概念的类型和难度"""

    def prep(self, shared):
        return shared["concept"]

    def exec(self, concept):
        prompt = f"""
分析以下概念的类型和难度级别：

概念：{concept}

请以 YAML 格式输出：
```yaml
type: [编程概念/算法/框架/理论/其他]
difficulty: [初级/中级/高级]
domain: [具体领域，如：Python/前端/数据库等]
```
"""
        response = call_llm(prompt)

        # 解析 YAML
        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            analysis = yaml.safe_load(yaml_str)
            return analysis
        except:
            # 如果解析失败，返回默认值
            return {
                "type": "编程概念",
                "difficulty": "中级",
                "domain": "通用"
            }

    def post(self, shared, prep_res, exec_res):
        shared["analysis"] = exec_res
        print(f"✓ 概念分析完成：{exec_res['type']} | {exec_res['difficulty']}")


class GenerateExplanationNode(Node):
    """从三个角度生成解释"""

    def prep(self, shared):
        return shared["concept"], shared["analysis"]

    def exec(self, inputs):
        concept, analysis = inputs

        prompt = f"""
请从三个角度深入解释以下{analysis['difficulty']}{analysis['type']}：

概念：{concept}

以 YAML 格式输出：
```yaml
what: |
  这个概念是什么？（定义、本质）

why: |
  为什么需要这个概念？（解决什么问题、存在的意义）

how: |
  如何使用这个概念？（应用场景、基本用法）
```

要求：
- 语言通俗易懂，避免过度专业术语
- 每个角度 3-5 句话
- 重点突出核心思想
"""
        response = call_llm(prompt)

        # 解析 YAML
        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            explanation = yaml.safe_load(yaml_str)
            return explanation
        except:
            return {
                "what": "解析失败",
                "why": "解析失败",
                "how": "解析失败"
            }

    def post(self, shared, prep_res, exec_res):
        shared["explanation"] = exec_res
        print(f"✓ 多角度解释生成完成")


class GenerateExamplesNode(Node):
    """生成类比和代码示例"""

    def prep(self, shared):
        return shared["concept"], shared["analysis"], shared["explanation"]

    def exec(self, inputs):
        concept, analysis, explanation = inputs

        prompt = f"""
为概念"{concept}"生成生动的类比和代码示例。

背景：
- 类型：{analysis['type']}
- 领域：{analysis['domain']}

以 YAML 格式输出：
```yaml
analogy: |
  一个生动的生活类比（帮助理解概念）

code_example: |
  实际的代码示例（如果适用）
  包含注释说明关键点

explanation: |
  解释示例如何体现概念
```

要求：
- 类比要贴近日常生活，易于理解
- 代码示例简洁清晰，突出核心
- 如果不适用代码示例，可以用文字示例替代
"""
        response = call_llm(prompt)

        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            examples = yaml.safe_load(yaml_str)
            return examples
        except:
            return {
                "analogy": "解析失败",
                "code_example": "解析失败",
                "explanation": "解析失败"
            }

    def post(self, shared, prep_res, exec_res):
        shared["examples"] = exec_res
        print(f"✓ 类比和示例生成完成")


class GeneratePracticeNode(Node):
    """生成实践建议和学习路径"""

    def prep(self, shared):
        return shared["concept"], shared["analysis"]

    def exec(self, inputs):
        concept, analysis = inputs

        prompt = f"""
为学习"{concept}"（{analysis['difficulty']}）提供实践建议。

以 YAML 格式输出：
```yaml
learning_path:
  - 步骤1：xxx
  - 步骤2：xxx
  - 步骤3：xxx

practice_ideas:
  - 练习1：xxx
  - 练习2：xxx

resources:
  - 资源1：xxx
  - 资源2：xxx

common_pitfalls:
  - 常见误区1：xxx
  - 常见误区2：xxx
```

要求：
- 学习路径循序渐进，适合{analysis['difficulty']}水平
- 练习想法具体可行
- 资源推荐实用（官方文档、教程、工具等）
- 指出初学者容易犯的错误
"""
        response = call_llm(prompt)

        try:
            yaml_str = response.split("```yaml")[1].split("```")[0].strip()
            practice = yaml.safe_load(yaml_str)
            return practice
        except:
            return {
                "learning_path": ["解析失败"],
                "practice_ideas": ["解析失败"],
                "resources": ["解析失败"],
                "common_pitfalls": ["解析失败"]
            }

    def post(self, shared, prep_res, exec_res):
        shared["practice"] = exec_res
        print(f"✓ 实践建议生成完成")


class FormatOutputNode(Node):
    """格式化最终输出"""

    def prep(self, shared):
        return {
            "concept": shared["concept"],
            "analysis": shared["analysis"],
            "explanation": shared["explanation"],
            "examples": shared["examples"],
            "practice": shared["practice"]
        }

    def exec(self, data):
        # 格式化为 Markdown
        output = f"""
# 📚 概念深度讲解：{data['concept']}

---

## 📊 概念分析

- **类型**：{data['analysis']['type']}
- **难度**：{data['analysis']['difficulty']}
- **领域**：{data['analysis']['domain']}

---

## 💡 多角度理解

### 🔍 是什么？（What）

{data['explanation']['what']}

### 🤔 为什么？（Why）

{data['explanation']['why']}

### 🛠️ 怎么用？（How）

{data['explanation']['how']}

---

## 🎯 类比和示例

### 生活类比

{data['examples']['analogy']}

### 代码示例

```
{data['examples']['code_example']}
```

### 示例说明

{data['examples']['explanation']}

---

## 📝 实践建议

### 学习路径

{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(data['practice']['learning_path']))}

### 练习想法

{chr(10).join(f'- {idea}' for idea in data['practice']['practice_ideas'])}

### 推荐资源

{chr(10).join(f'- {resource}' for resource in data['practice']['resources'])}

### ⚠️ 常见误区

{chr(10).join(f'- {pitfall}' for pitfall in data['practice']['common_pitfalls'])}

---

*生成完成！祝学习愉快！* 🎓
"""
        return output

    def post(self, shared, prep_res, exec_res):
        shared["final_output"] = exec_res
        print("\n" + "="*60)
        print(exec_res)
        print("="*60)
