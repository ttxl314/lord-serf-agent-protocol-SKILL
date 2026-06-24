# Lord 和 Serf

一组用于多 Agent 项目编排的跨平台配套 Skill。

- `lord` 是主控编排 Skill：负责复杂项目规划、任务拆分、边界与验收标准定义、任务派发、状态权威源维护和最终验收。
- `serf` 是外部执行 Skill：负责接收 lord 派发的任务包，读取必要上下文，在边界内执行任务，自我验证，并返回可供 lord 验收的交接报告、阻塞报告或变更请求。

English version: [README.md](README.md)

## 为什么需要它

很多 Agent 工作流会跨软件、跨平台、跨独立会话运行。单靠聊天记录并不适合维护项目状态。`lord` 和 `serf` 使用 Markdown、YAML、模板和 schema 定义一套可移植协议，让主控 Agent 与外部执行 Agent 能在不同平台中协作，而不依赖某一个供应商或运行环境。

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

## 在 Codex 中使用

把两个文件夹安装到 Codex skills 目录：

```text
~/.codex/skills/lord
~/.codex/skills/serf
```

然后可以这样调用：

```text
$lord
$serf
```

`agents/openai.yaml` 是面向 Codex 或类似环境的 UI 元数据。它方便 Codex 自动发现和展示 Skill，但不是底层协作协议的必需部分。

## 跨平台使用

这组 Skill 并不和 Codex 强绑定。迁移到其他平台时：

1. 把 `lord/SKILL.md` 作为主控 Agent 的 system instruction 或 project instruction。
2. 把 `serf/SKILL.md` 作为外部执行 Agent 的 system instruction 或 project instruction。
3. 按需提供 `references/` 中的参考文件。
4. 使用 `assets/templates/` 中的任务包、交接、阻塞和变更请求模板。
5. 需要结构化 YAML 或 JSON 校验时，使用 `assets/schemas/`。

跨平台时应保持这些字面值不变：任务编号、状态值、文件路径、schema key、命令名和运行环境路径。

## 核心流程

1. `lord` 分析项目，并选择最小必要项目结构。
2. `lord` 创建 `Agent-A-01` 这类任务编号，并生成正式任务包。
3. `lord` 明确必读文件、工作边界、依赖、验证方法、预期输出，以及必要的 Python/conda 运行环境。
4. `serf` 接收任务包，只执行被分配的任务。
5. `serf` 自我验证，并返回 `REVIEW`、`BLOCKED` 或变更请求。
6. `lord` 审阅实际成果，只有 `lord` 可以确认 `DONE`。

## Python 和 Conda 环境交接

如果任务需要运行 Python，`lord` 应指定以下至少一种信息：

- `conda_env_path`
- `conda_env_name`
- `python_executable`
- `activation_command`
- `package_install_policy`

`serf` 必须使用指定运行环境，并在交接报告中记录实际使用的运行环境。如果指定环境不可用，`serf` 应返回阻塞报告，而不是静默回退到 system Python 或其他 conda 环境。

## 语言与中文/CJK 安全性

Skill 本体使用英文编写，以提高跨平台和模型读取效率。同时也保留了中文/CJK 代码风险处理规则，包括 UTF-8 编码、全角标点、非 ASCII 路径、shell 引号、Unicode 长度/正则、渲染宽度等问题。

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

## 推荐上传到 GitHub 的内容

建议提交：

- `lord/`
- `serf/`
- `README.md`
- `README.zh-CN.md`
- `.gitignore`

旧 zip 包和本地临时文件通常不需要提交。
