# Lord 和 Serf

[![English](https://img.shields.io/badge/Language-English-blue)](README.md)

一组采用文件化状态管理、用于复杂多执行端项目编排的跨平台配套 Skill。

- `lord` 是编排 Skill：负责规划、生成任务包、派发 Serf 执行端、维护权威任务状态并作出审阅决策。
- `serf` 是执行 Skill：负责执行一个 Lord 派发的任务包、验证实际产物并生成一份提交报告。

## 协议 0.5

统一流程为：

```text
规划 → 打包 → 派发 → 执行 → 提交 → 审阅 → 决策
```

统一使用以下名称：

| 概念 | 规范名称 |
|---|---|
| 编排角色 | Lord |
| 执行角色 | Serf |
| 需求载体 | 任务包（task package） |
| 启动指令 | 派发指令（dispatch instruction） |
| 执行证据 | 提交报告（submission report） |
| 项目状态权威 | 权威状态源（authoritative state source） |
| 稳定工作编号 | `Task-A-01` 形式的任务 ID |

聊天只用于通知；项目状态、需求、证据和决策都应保存在文件中。

## 仓库结构

```text
.
├── .editorconfig
├── .gitattributes
├── .github/workflows/validate.yml
├── lord/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/{schemas,templates}/
│   └── references/
├── serf/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/{schemas,templates}/
│   └── references/
├── scripts/validate_repo.py
└── requirements-dev.txt
```

Lord 负责任务与派发资源，Serf 负责提交资源。`assets/` 下的路径均相对于当前激活的 Skill 根目录解释。

## 在 Codex 中安装

将两个 Skill 文件夹复制到 Codex Skills 目录：

```text
~/.codex/skills/lord
~/.codex/skills/serf
```

覆盖已安装版本后重启 Codex，然后调用：

```text
$lord
$serf
```

该协议也可在 Codex 之外使用：编排端加载 `lord/SKILL.md`，执行端加载 `serf/SKILL.md`，保持字段名和路径字面值不变，后续任务只传递任务包路径。

## 任务档位

| 档位 | 适用情况 | REVIEW 报告 |
|---|---|---|
| `micro` | 单一、低风险、相互隔离且验收条件不超过三项 | 紧凑 YAML |
| `standard` | 普通模块级工作和常规验证 | Markdown 或机器可读等价结构 |
| `full` | 架构、共享 Schema、复杂依赖、安全、迁移或难回滚工作 | 风险导向的 Markdown 或机器可读等价结构 |

应选择能够安全完成任务的最小档位。

## 协议命名空间

| 命名空间 | 值 |
|---|---|
| `task_status` | `PENDING`、`READY`、`IN_PROGRESS`、`BLOCKED`、`REVIEW`、`REWORK`、`DONE`、`REJECTED`、`CANCELLED` |
| `submission_type` | `REVIEW`、`BLOCKED`、`CHANGE_REQUEST` |
| 验证结果 | `PASS`、`FAIL`、`SKIPPED` |
| 变更决策 | `APPROVE_CHANGE`、`REJECT_CHANGE`、`REQUEST_INFO` |

提交类型不是任务状态。只有 Lord 可以更新权威任务结果。

## 核心流程

1. Lord 选择项目结构和任务档位。
2. Lord 分配 `Task-A-01` 形式的任务 ID 并生成任务包。
3. Lord 定义边界、依赖、预期产物、验收 ID、验证方法、运行环境和 `submission_path`。
4. Lord 使用仅引用任务包的简短派发指令启动 Serf 执行端。
5. Serf 只执行被分配的工作，并提交 `REVIEW`、`BLOCKED` 或 `CHANGE_REQUEST`。
6. Lord 审查实际产物与证据，然后更新权威状态源。

## 公共字段

任务包使用以下共享字段：

```yaml
protocol_version: "0.5"
profile:  # micro | standard | full
project_id:
task_id:
task_version:
updated_at:
task_status:
objective:
inputs: []
allowed_paths: []
forbidden_paths: []
expected_outputs: []
acceptance_criteria: {}
validation_methods: []
depends_on: []
inherits: []
execution_environment:
  requires_python: false
submission_path:
```

`standard` 和 `full` 任务包增加以下字段；`output_language` 可选：

```yaml
target_adapter:  # generic-chat | coding | document | api | shared-workspace
dispatch_mode:  # direct | semi-automatic | manual-copy
authoritative_state_source:  # 例如 PROJECT_PLAN.md
output_language:
```

Serf 提交共享以下 Envelope：

```yaml
protocol_version: "0.5"
profile:
project_id:
task_id:
executed_task_version:
submitted_at:
submission_type: REVIEW  # REVIEW | BLOCKED | CHANGE_REQUEST
task_package_path:
report_path:
```

## 权威提交资源

```text
serf/assets/templates/micro-review-report.yaml
serf/assets/templates/review-report.md
serf/assets/templates/blocker-report.md
serf/assets/templates/change-request-report.md
serf/assets/schemas/submission-envelope.schema.yaml
serf/assets/schemas/micro-review-report.schema.yaml
serf/assets/schemas/review-report.schema.yaml
```

## 报告路径与命令

```text
micro REVIEW：             REVIEWS/Task-A-01-REVIEW.yaml
standard/full REVIEW：     REVIEWS/Task-A-01-REVIEW.md
BLOCKED：                  BLOCKERS/Task-A-01-BLOCKER.md
CHANGE_REQUEST：           CHANGE_REQUESTS/Task-A-01-CHANGE-REQUEST.md
```

```text
$lord review REVIEWS/Task-A-01-REVIEW.yaml
$lord review REVIEWS/Task-A-01-REVIEW.md
$lord resolve BLOCKERS/Task-A-01-BLOCKER.md
$lord resolve CHANGE_REQUESTS/Task-A-01-CHANGE-REQUEST.md
```

## 运行环境与语言

Python 任务由 Lord 指定 Conda 环境路径、准确 Python 可执行文件或激活命令。Serf 必须使用该环境；若环境不可用，则提交 `BLOCKED`。

输出语言默认跟随当前会话语言。Skill 还包括 UTF-8、中文/CJK 文本、本地化路径、Shell 引号、Unicode 检查和渲染宽度风险指导。

## 验证

```text
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
```

校验器会检查 UTF-8/LF 格式、Skill 与 UI 元数据、规范术语、本地引用、YAML 和 JSON Schema、模板与档位兼容性，以及代表性协议载荷。GitHub Actions 会在 push 和 pull request 时运行相同命令。

如果 Windows 上还安装了 Codex 的 `skill-creator` 校验器，请先强制启用 UTF-8：

```powershell
$env:PYTHONUTF8 = "1"
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ".\lord"
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ".\serf"
```

## 迁移到协议 0.5

从协议 0.4 升级时，应使用 `protocol_version: "0.5"` 重新生成未完成的任务包和报告。协议 0.5 为每个任务包增加简短的项目上下文索引，并在提交 Envelope 中拒绝弃用的 v0.3 字段名。

对于协议 0.3 用户，0.5 保留了 0.4 引入的规范命名：

| v0.3 | v0.5 |
|---|---|
| `agent_id`、`Agent-A-01` | `task_id`、`Task-A-01` |
| `status` | `task_status` |
| `target_agent_type` | `target_adapter` |
| `required_files` | `inputs` |
| `allowed_changes` | `allowed_paths` |
| `return_path`、`handoff_path` | `submission_path` |
| `acceptance` | `acceptance_criteria` |
| 任务 `validation` | `validation_methods` |
| 提交 `changed`、`result`、`validation` | `changed_outputs`、`results`、`validation_results` |
| `HANDOFFS/` | `REVIEWS/` |
| `agent-task.md` | `task-package.md` |
| `micro-handoff.yaml`、`review-handoff.md` | `micro-review-report.yaml`、`review-report.md` |

`$lord` 命令属于聊天/传输层，不以 `lord_invocation` 存入机器可读报告。升级前应完成正在执行的旧协议工作，或将未完成的任务包和报告重新生成为 v0.5。
