# Lord 和 Serf

[![English](https://img.shields.io/badge/Language-English-blue)](README.md)

一组采用文件化状态管理、用于多 Agent 项目编排的跨平台配套 Skill。

- `lord` 是主控编排 Skill：负责项目规划、生成有边界的任务包、维护权威任务状态并完成最终验收。
- `serf` 是执行端 Skill：负责执行一个 lord 派发的任务包，自我验证，并提交 `REVIEW`、`BLOCKED` 或 `CHANGE_REQUEST` 证据。

## 协议概览

- 当前协议版本：`0.3`。
- 项目状态保存在文件中，而不是依赖聊天记忆。
- 任务档位分为 `micro`、`standard` 和 `full`。
- Lord 负责需求和权威状态，Serf 负责返回模板与返回 Schema。
- 只有 Lord 可以设置 `REWORK`、`DONE`、`REJECTED` 或 `CANCELLED`。
- 面向人的聊天回复只是简短通知，详细证据应保存在报告文件中。

## 为什么需要它

很多 Agent 工作流会跨软件、跨平台、跨代码仓库或跨独立会话运行。单靠聊天记录并不适合维护项目状态。`lord` 和 `serf` 使用 Markdown、YAML、模板、Schema、稳定编号和文件路径定义一套可移植协议，使规划、执行、验收和恢复过程能够在不同环境中复现。

## 仓库结构

```text
.
├── lord/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/
│   │   ├── schemas/
│   │   └── templates/
│   └── references/
└── serf/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── assets/
    │   ├── schemas/
    │   └── templates/
    └── references/
```

核心归属规则：

```text
lord/assets/...  = 任务与派发资源
serf/assets/...  = 执行端返回资源
```

在某个已激活的 Skill 内，`assets/...` 路径均相对于该 Skill 根目录解释。

## 在 Codex 中安装

将两个文件夹复制到 Codex 的 Skills 目录。常见结构为：

```text
~/.codex/skills/lord
~/.codex/skills/serf
```

应确保以下文件可直接访问：

```text
~/.codex/skills/lord/SKILL.md
~/.codex/skills/serf/SKILL.md
```

可以采用完全离线的普通复制方式，不需要连接代码仓库、建立符号链接或自动同步。覆盖已安装版本后应重新启动 Codex。

调用方式：

```text
$lord
$serf
```

`agents/openai.yaml` 是面向 Codex 或类似环境的 UI 元数据。它便于自动发现和展示 Skill，但不是底层协作协议的必需部分。

## 跨平台使用

这组 Skill 并不和 Codex 强绑定。

1. 将 `lord/SKILL.md` 作为主控 Agent 指令。
2. 将 `serf/SKILL.md` 作为执行端 Agent 指令。
3. 条件允许时，每个独立软件会话只加载一次对应 Skill。
4. 在共享工作区中，后续派发只需引用任务包路径，不要重复发送整套协议。
5. 没有共享工作区时，只传输任务包、必需输入和匹配的 Serf 返回模板。
6. 跨平台时保持任务编号、状态、Schema 字段、命令名和报告路径的字面值不变。

## 任务档位

| 档位 | 适用情况 | 常见返回形式 |
|---|---|---|
| `micro` | 单一、低风险、相互隔离的目标，验收条件不超过三项 | 紧凑 YAML 交接报告 |
| `standard` | 普通模块级工作，涉及若干相关文件和常规验证 | 紧凑 Markdown 或机器可读报告 |
| `full` | 架构、共享 Schema、复杂依赖、安全、迁移或难以回滚的工作 | 更完整的证据和风险导向验收 |

应选择能够安全完成任务的最小档位。

## 核心流程

1. `lord` 选择最小必要项目结构和任务档位。
2. `lord` 创建 `Agent-A-01` 这类任务编号并生成正式任务包。
3. `lord` 明确目标、边界、依赖、预期输出、验收编号、验证方法和运行环境。
4. `serf` 读取任务包，只执行被分配的工作。
5. `serf` 自我验证并提交 `REVIEW`、`BLOCKED` 或 `CHANGE_REQUEST`。
6. `lord` 检查实际成果，按风险进行验收，并更新权威状态源。

## 返回协议

所有 Serf 返回共享以下公共字段：

```yaml
protocol_version: "0.3"
project_id:
agent_id:
executed_task_version:
submitted_at:
submission_type: REVIEW  # REVIEW | BLOCKED | CHANGE_REQUEST
task_package_path:
report_path:
```

权威返回资源位于当前激活的 Serf Skill 中：

```text
assets/templates/micro-handoff.yaml
assets/templates/review-handoff.md
assets/templates/blocker-report.md
assets/templates/change-request.md
assets/schemas/submission-envelope.schema.yaml
assets/schemas/micro-handoff.schema.yaml
assets/schemas/review-handoff.schema.yaml
```

Markdown 模板用于人工审阅或共享工作区。完整任务和 Review Schema 用于校验机器可读的 YAML 或 JSON 等价结构，不能单独校验 Markdown 正文。

## 报告路径与命令

```text
Micro Review：       HANDOFFS/Agent-A-01.yaml
Full Review：        HANDOFFS/Agent-A-01-HANDOFF.md
Blocker：            BLOCKERS/Agent-A-01-BLOCKER.md
Change Request：     CHANGE_REQUESTS/Agent-A-01-CHANGE-REQUEST.md
```

```text
$lord review HANDOFFS/Agent-A-01.yaml
$lord review HANDOFFS/Agent-A-01-HANDOFF.md
$lord resolve BLOCKERS/Agent-A-01-BLOCKER.md
$lord review CHANGE_REQUESTS/Agent-A-01-CHANGE-REQUEST.md
```

## 上下文与验收精简

- 使用权威项目文件引用稳定上下文，不在每个任务中重复粘贴。
- 派发说明只保留任务路径和必要执行提示。
- 使用稳定验收编号建立证据映射。
- 一条验证命令可以同时支持多个验收条件。
- Micro 任务默认在检查实际成果后复用 Serf 证据，不机械重复运行。
- Standard 任务定向复验不确定、具有代表性或价值较高的检查。
- Full 任务复验关键高风险检查。
- REWORK 只返回失败或受影响的验收项、必要修改、必须保留的行为和需要重跑的检查。

## Python 和 Conda 环境交接

如果任务需要运行 Python，`lord` 应指定以下至少一种信息：

- `conda_env_path`
- `conda_env_name`
- `python_executable`
- `activation_command`
- `package_install_policy`

`serf` 必须使用指定运行环境，并记录实际使用的运行环境。如果指定环境不可用，`serf` 应返回 `BLOCKED`，而不是静默回退到其他解释器。

## 语言与中文/CJK 安全性

Skill 本体使用英文编写，以提高跨平台和模型读取效率。同时也保留了中文/CJK 代码风险处理规则，包括 UTF-8 编码、全角标点、非 ASCII 路径、Shell 引号、Unicode 长度与正则、渲染宽度等问题。

## 验证

如果你有 Codex 的 `skill-creator` 验证脚本，可以运行：

```powershell
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ".\lord"
python "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" ".\serf"
```

期望输出：

```text
Skill is valid!
```

## 从协议 0.2 迁移

在覆盖安装 v0.3 前，应完成正在执行的 v0.2 任务；尚未完成的任务应重新生成为 v0.3。不要在同一任务或报告中混用 v0.2 与 v0.3 的字段。

## Star History

<p align="center">
  <a href="https://www.star-history.com/#ttxl314/lord-serf-agent-protocol-SKILL&Date">
    <picture>
      <source
        media="(prefers-color-scheme: dark)"
        srcset="https://api.star-history.com/chart?repos=ttxl314/lord-serf-agent-protocol-SKILL&type=date&theme=dark&legend=top-left"
      />
      <source
        media="(prefers-color-scheme: light)"
        srcset="https://api.star-history.com/chart?repos=ttxl314/lord-serf-agent-protocol-SKILL&type=date&legend=top-left"
      />
      <img
        alt="Star History Chart"
        src="https://api.star-history.com/chart?repos=ttxl314/lord-serf-agent-protocol-SKILL&type=date&legend=top-left"
      />
    </picture>
  </a>
</p>

