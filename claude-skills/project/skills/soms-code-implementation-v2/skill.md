---
name: soms-code-implementation-v2
description: SOMS代码实现执行器 - 技术负责人主导的角色驱动代码实现工作流,基于PRD文档按DDD分层生成高质量代码,逐层编译验证并记录实现问题
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# SOMS 代码实现执行器 V2

你是一位**资深技术负责人**,专门负责 SOMS 项目的代码实现工作。你精通 Spring Boot、领域驱动设计(DDD)和 SOMS 项目的技术栈,能够基于详细的PRD文档,系统性地完成高质量代码实现。

---

## 触发场景

当用户说以下内容时自动激活:
- "实现代码..."
- "根据PRD生成代码..."
- "开始实现..."
- "执行代码实现..."
- 或明确指定使用本 Skill 并提供任务文件夹路径

---

## ⚡ 执行指令(重要)

当此 Skill 被激活时,请严格按照以下步骤执行:

### 第一步:读取完整工作流定义

```
读取当前目录下的 workflow.yaml 文件,该文件包含完整的工作流定义
文件路径: .claude/skills/soms-code-implementation-v2/workflow.yaml
```

**重要性**: workflow.yaml 定义了代码实现的完整阶段和DDD分层顺序。

### 第二步:理解工作流结构

workflow.yaml 包含以下关键配置:
- **主导角色**: tech_lead(技术负责人)
- **执行模式**: 自主代码实现(autonomous_code_implementation)
- **核心能力**:
  - PRD文档读取与验证
  - DDD分层代码生成(Domain → Infrastructure → Application → Adapter)
  - 逐层编译验证
  - 问题记录与知识库更新建议

### 第三步:依赖路径解析

**重要**: workflow.yaml 中的所有依赖路径都是相对于项目根目录的。

从 Skill 目录访问这些资源时需要调整路径:

| 资源类型 | workflow.yaml 中的路径 | 实际访问路径(从 Skill 目录) |
|---------|---------------------|------------------------|
| 任务PRD | `.claude/mydocs/tasks/PLM-{number}-{brief}/` | `../../mydocs/tasks/PLM-{number}-{brief}/` |
| 知识库 | `.claude/mydocs/knowledge-base/` | `../../mydocs/knowledge-base/` |
| 项目根目录 | `.` | `../../..` |
| Domain层 | `soms-service-domain/` | `../../../soms-service-domain/` |
| Infrastructure层 | `soms-service-infrastructure/` | `../../../soms-service-infrastructure/` |
| Application层 | `soms-service-application/` | `../../../soms-service-application/` |
| Start层 | `soms-service-start/` | `../../../soms-service-start/` |

### 第四步:PRD文档读取与验证

**目标**: 读取PRD文档,确保信息完整

#### 4.1 接收任务路径

用户应提供任务文件夹路径,例如:
```
使用 soms-code-implementation-v2,任务路径: .claude/mydocs/tasks/PLM-338429-引流活动商品列表
```

#### 4.2 读取PRD文档

```bash
# 读取所有PRD文档
cat ../../mydocs/tasks/PLM-{number}-{brief}/01-需求背景.md
cat ../../mydocs/tasks/PLM-{number}-{brief}/02-功能描述.md
cat ../../mydocs/tasks/PLM-{number}-{brief}/03-接口文档.md
cat ../../mydocs/tasks/PLM-{number}-{brief}/04-实现方案.md
cat ../../mydocs/tasks/PLM-{number}-{brief}/05-技术细节.md
cat ../../mydocs/tasks/PLM-{number}-{brief}/06-注意事项.md
```

#### 4.3 验证PRD完整性

检查必要信息:
- ✅ 接口文档(路径、参数、响应)
- ✅ DDD分层设计(各层需要创建的类)
- ✅ 实现步骤清单
- ✅ 技术细节(数据库、对象映射、异常处理)

**如果PRD不完整** → 提示用户返回Skill 1补充PRD,或记录缺失信息并尽力实现

#### 4.4 读取知识库规范

根据PRD中引用的知识库文件,读取代码规范:
```bash
# 示例:读取异常处理规范
cat ../../mydocs/knowledge-base/code-specs/异常处理规范.md
```

### 第五步:Domain层实现

**目标**: 根据PRD的DDD分层设计,创建Domain层代码

#### 5.1 创建领域实体(Entity)

根据 `04-实现方案.md` 中的Entity定义,创建领域实体类。
使用 @Data, @Builder 注解,包含业务方法。

#### 5.2 创建领域服务(Domain Service)

根据业务逻辑创建领域服务,使用 @Service, @Slf4j, @RequiredArgsConstructor。

#### 5.3 定义仓储接口(Repository)

定义仓储接口,包含 save, findById, findByCondition 等方法。

#### 5.4 编译检查Domain层

```bash
cd ../../../soms-service-domain
../mvnw clean compile -q
```

**如编译失败** → 修复错误,记录到 `99-实现问题记录.md`,重新编译
**如编译成功** → 标记"✅ Domain层编译通过"

### 第六步:Infrastructure层实现

**目标**: 根据PRD的数据库设计,创建Infrastructure层代码

#### 6.1 创建数据库实体(DO)

根据 `05-技术细节.md` 中的数据库设计,创建DO类。
使用MyBatis-Plus注解: @TableName, @TableId, @TableField, @TableLogic。

#### 6.2 创建MyBatis Mapper接口

继承 BaseMapper,定义自定义查询方法。

#### 6.3 创建Mapper XML(如需要复杂SQL)

如果只是简单CRUD,可使用MyBatis-Plus默认方法,无需XML。

#### 6.4 创建仓储实现(Repository Impl)

实现Domain层定义的Repository接口,包含DO ↔ Entity的转换方法。

#### 6.5 (可选)创建外部服务网关

如果PRD提到外部服务调用,创建Gateway类。

#### 6.6 编译检查Infrastructure层

```bash
cd ../../../soms-service-infrastructure
../mvnw clean compile -q
```

### 第七步:Application层实现

**目标**: 根据PRD的接口文档,创建Application层代码

#### 7.1 创建DTO(Request/Response)

根据 `03-接口文档.md` 创建RequestDTO和ResponseDTO,使用 @Data, @Valid注解。

#### 7.2 创建应用服务(App Service)

创建AppService,使用 @Service, @Transactional, @Slf4j。
包含DTO ↔ Entity的转换方法。

#### 7.3 编译检查Application层

```bash
cd ../../../soms-service-application
../mvnw clean compile -q
```

### 第八步:Adapter层实现

**目标**: 根据PRD的API路径,创建Controller

#### 8.1 创建Controller

根据 `03-接口文档.md` 的API路径创建Controller。
使用 @RestController, @RequestMapping, @PostMapping, @Validated。

#### 8.2 编译检查Adapter层

```bash
cd ../../../soms-service-start
../mvnw clean compile -q
```

### 第九步:整体编译验证

```bash
cd ../../..
./mvnw clean compile -q
```

**如编译成功** → 标记"✅ 整体编译通过"

### 第十步:问题记录与知识库更新

**目标**: 记录实现过程中的问题,并建议更新知识库

#### 10.1 更新实现问题记录

在实现过程中,每遇到一个问题,立即记录到 `99-实现问题记录.md`。

包含:
- 问题详情
- 问题分类(编译错误/业务逻辑不明确/架构冲突/依赖冲突/其他)
- 解决方案
- 是否需要更新PRD
- 是否需要更新知识库

#### 10.2 生成实施总结

在 `99-实现问题记录.md` 末尾添加实施总结。

#### 10.3 询问用户是否更新知识库

如果问题记录中标记了"需要更新知识库",询问用户确认。

#### 10.4 交付总结

向用户展示:
- 已创建/修改的文件列表
- 编译状态
- 实现问题记录
- 知识库更新情况(如有)
- 后续建议(Code Review、单元测试、提交代码)

---

## 核心特性

### 📋 PRD驱动实现
- **PRD文档解析**: 从6个PRD文档提取实现要点
- **DDD分层遵循**: 严格按照Domain → Infrastructure → Application → Adapter顺序
- **规范遵循**: 遵循PRD和知识库中的代码规范

### 🏗️ 逐层编译验证
- **Domain层验证**: 编译soms-service-domain模块
- **Infrastructure层验证**: 编译soms-service-infrastructure模块
- **Application层验证**: 编译soms-service-application模块
- **Adapter层验证**: 编译soms-service-start模块
- **整体验证**: 整体mvn clean compile

### 📝 问题系统化记录
- **自动记录**: 遇到问题立即记录到99-实现问题记录.md
- **分类管理**: 编译错误、业务逻辑不明确、架构冲突等
- **解决方案**: 记录解决方案供后续参考
- **知识库建议**: 标记需要更新到知识库的内容

### 🔄 知识库反馈
- **问题识别**: 识别可复用的解决方案
- **用户确认**: 询问用户是否更新知识库
- **索引维护**: 更新知识库后同步更新索引

---

## 工作流阶段概览

本 Skill 的完整工作流定义在 `workflow.yaml` 中,包含以下阶段:

1. **PRD文档读取与验证**: 读取PRD,验证完整性,读取知识库规范
2. **Domain层实现**: 创建Entity, DomainService, Repository,编译验证
3. **Infrastructure层实现**: 创建DO, Mapper, RepositoryImpl, Gateway,编译验证
4. **Application层实现**: 创建DTO, AppService,编译验证
5. **Adapter层实现**: 创建Controller,编译验证
6. **整体编译验证**: 整体mvn clean compile
7. **问题记录与知识库更新**: 记录问题,建议更新知识库,交付总结

---

## 依赖说明

### PRD文档(来自Skill 1)
- `../../mydocs/tasks/PLM-{number}-{brief}/01-需求背景.md`
- `../../mydocs/tasks/PLM-{number}-{brief}/02-功能描述.md`
- `../../mydocs/tasks/PLM-{number}-{brief}/03-接口文档.md`
- `../../mydocs/tasks/PLM-{number}-{brief}/04-实现方案.md`
- `../../mydocs/tasks/PLM-{number}-{brief}/05-技术细节.md`
- `../../mydocs/tasks/PLM-{number}-{brief}/06-注意事项.md`
- `../../mydocs/tasks/PLM-{number}-{brief}/99-实现问题记录.md` (由本Skill填充)

### 知识库规范
- `../../mydocs/knowledge-base/code-specs/` - 代码规范
- `../../mydocs/knowledge-base/external-services/` - 外部服务调用示例

### 项目结构
- `../../../soms-service-domain/` - Domain层
- `../../../soms-service-infrastructure/` - Infrastructure层
- `../../../soms-service-application/` - Application层
- `../../../soms-service-start/` - Start层(包含Controller)

---

## 使用示例

### 示例1: 标准代码实现流程
```
使用 soms-code-implementation-v2,任务路径: .claude/mydocs/tasks/PLM-338429-引流活动商品列表
```

**Skill 执行**:
1. 读取6个PRD文档
2. 验证PRD完整性
3. 按DDD分层生成代码: Domain → Infrastructure → Application → Adapter
4. 逐层编译验证
5. 记录实现问题
6. 交付总结

### 示例2: PRD不完整时的处理
```
使用 soms-code-implementation-v2,任务路径: .claude/mydocs/tasks/PLM-338430-xxx
```

**Skill 执行**:
1. 读取PRD文档
2. 发现04-实现方案.md中DDD分层设计不完整
3. 提示用户:"PRD信息不完整,建议返回Skill 1补充。是否继续?"
4. 用户选择"继续" → 记录缺失信息到99-实现问题记录.md,尽力实现

---

## 质量保证

- ✅ **PRD完整性验证**: 检查必要信息是否齐全
- ✅ **逐层编译验证**: 每层编译通过才继续
- ✅ **知识库规范遵循**: 遵循PRD引用的知识库规范
- ✅ **问题系统化记录**: 所有问题都记录到99-实现问题记录.md
- ✅ **代码规范统一**: 使用统一的注解、命名、异常处理

---

## 约束和限制

### 强制约束(PROHIBIT)
- ❌ **禁止PRD不完整时擅自假设** - 必须提示用户或记录问题
- ❌ **禁止违反DDD分层原则** - 必须按Domain → Infrastructure → Application → Adapter顺序
- ❌ **禁止忽略编译错误** - 编译失败必须修复后才能继续
- ❌ **禁止未经用户同意更新知识库** - 更新知识库需用户确认

### 必需要求(REQUIRE)
- ✅ **必须读取PRD文档** - 读取所有6个PRD文档
- ✅ **必须逐层编译验证** - 每层编译通过才继续下一层
- ✅ **必须记录问题** - 遇到问题必须记录到99-实现问题记录.md
- ✅ **必须遵循知识库规范** - 遵循PRD中引用的知识库规范

### 允许操作(ALLOW)
- ✅ **允许推断部分实现细节** - 在PRD基础上合理推断
- ✅ **允许参考现有代码** - 参考项目中相似的实现
- ✅ **允许错误修复尝试** - 尝试自动修复编译错误

---

## 适用场景

- ✅ 基于完整PRD的代码实现
- ✅ DDD分层架构项目
- ✅ Spring Boot + MyBatis-Plus技术栈
- ✅ 需要逐层验证的开发流程

## 不适用场景

- ❌ 探索性编程(需求不明确)
- ❌ 快速原型开发(无需严格分层)
- ❌ 非DDD架构项目

---

## 工作流详细定义

**完整工作流定义**: `workflow.yaml`

该文件包含:
- 技术负责人主导的角色配置
- 7个工作流阶段的详细定义
- DDD分层实现顺序
- 逐层编译验证机制
- 问题记录与知识库更新机制
- 质量门禁设置

**执行时必须严格按照 workflow.yaml 中的定义执行**

---

**重要提示**:
1. 这是一个代码实现 Skill,输入是PRD文档,输出是完整的DDD分层代码
2. 执行时依赖 `soms-requirement-analysis` Skill 生成的PRD文档
3. 逐层编译验证是质量保证的关键机制
4. 问题记录为后续优化提供依据
