# 📝 编程练习生成器

根据你想学习的知识点，自动生成渐进式练习题，帮助你边学边练。

## 功能特点

✅ **渐进式难度**：题目从简单到复杂，循序渐进
✅ **完整示例**：每道题都有输入输出示例
✅ **思考提示**：引导你独立思考解决方案
✅ **详细答案**：参考答案带详细注释
✅ **知识总结**：总结每道题的考察点
✅ **延伸练习**：建议更多变体练习

## 快速开始

### 基础用法

```bash
# 生成中等难度的练习（默认3道题）
python main.py "Python列表推导式"

# 指定难度
python main.py "二叉树遍历" --difficulty hard

# 指定题目数量
python main.py "SQL JOIN查询" --count 5

# 组合使用
python main.py "动态规划" -d hard -c 3
```

## 使用场景

- 🎓 学完概念后想做练习巩固
- 💪 准备面试，刷题训练
- 🎯 系统学习某个专题
- 📝 自己出题测试理解程度

## 使用示例

```bash
$ python main.py "Python装饰器" --difficulty easy --count 3

============================================================
📝 编程练习生成器
============================================================

🎯 主题：Python装饰器
📊 难度：easy
🔢 数量：3 道题
------------------------------------------------------------

⏳ 正在生成练习题，请稍候...

============================================================
# 📝 Python装饰器 - 练习题集

难度：初级（适合刚接触的学习者）

---

## 练习 1：基础计时装饰器

### 📋 题目描述
编写一个装饰器 `timer`，用于测量函数的执行时间...

[更多内容]
============================================================

💾 是否保存练习题？(y/n): y
✅ 已保存到：Python装饰器_easy_练习.md

💡 建议：找个编辑器打开文件，边看边练！
```

## 推荐学习流程

### 1. 先学概念
```bash
cd ../learning-explainer
python main.py "Python装饰器"
```

### 2. 再做练习
```bash
cd ../practice-generator
python main.py "Python装饰器" -d easy
```

### 3. 审查答案
```bash
cd ../code-reviewer
python main.py Python装饰器_easy_练习.md
```

### 4. 循环提升
完成简单题目后，逐步提高难度：
```bash
python main.py "Python装饰器" -d medium
python main.py "Python装饰器" -d hard
```

## 支持的主题示例

### Python 相关
- Python装饰器
- 列表推导式
- 生成器和迭代器
- 闭包
- 多线程/多进程
- 异步编程 (async/await)
- 元类

### 数据结构与算法
- 二叉树遍历
- 链表操作
- 动态规划
- 回溯算法
- 贪心算法
- 图算法
- 排序算法

### Web 开发
- RESTful API 设计
- 数据库查询优化
- 前端状态管理
- WebSocket 实时通信

### 系统设计
- 缓存策略
- 限流算法
- 分布式锁
- 消息队列

## 配置

使用 `learning-explainer` 的 LLM 配置。

## 扩展建议

### 改造成 PocketFlow 多节点流程

```python
# 可以添加以下节点：
1. AnalyzeTopicNode - 分析主题，判断类型
2. GenerateExercisesNode - 生成题目（BatchNode）
3. ValidateExercisesNode - 验证题目质量
4. FormatOutputNode - 格式化输出
```

### 添加交互式功能

```python
# 可以添加：
1. 在线评判 - 用户提交答案，自动判对错
2. 提示系统 - 做不出时给渐进式提示
3. 错题本 - 记录做错的题目
4. 进度追踪 - 记录完成情况
```

## 进阶用法

### 生成系列练习

```bash
# 创建一个完整的学习路径
python main.py "Python基础语法" -d easy -c 5
python main.py "Python函数进阶" -d medium -c 5
python main.py "Python装饰器" -d medium -c 3
python main.py "Python元类" -d hard -c 3
```

### 结合其他技能

```bash
# 1. 学概念
cd ../learning-explainer
python main.py "闭包"

# 2. 做练习
cd ../practice-generator
python main.py "闭包" -d easy

# 3. 审查代码（如果练习中有代码）
cd ../code-reviewer
python main.py my_closure_solution.py
```

## 技巧提示

1. **从简单开始**：不确定难度时，先用 `easy`
2. **少而精**：3道题比10道题效果更好
3. **独立思考**：看答案前先自己尝试
4. **变体练习**：完成后尝试延伸练习
5. **总结归纳**：做完写个小总结

## 许可

MIT License
