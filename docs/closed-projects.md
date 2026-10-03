# 闭源与受限项目清单

核查日期：2026-10-04。范围是当前对话涉及的生物 AI for Science 产品及组件，不是三家公司所有闭源资产的完整盘点。闭源状态基于官方发布方式及未提供完整公开实现的观察；不推断内部架构。

| 公司 | 项目或组件 | 能否 fork 完整产品 | 可访问方式及边界 | 官方来源 |
|---|---|---|---|---|
| OpenAI | GPT-Rosalind 模型系列 | 未发现官方完整模型源码及权重仓库 | 合资格组织通过 trusted-access 使用；插件不包含模型 | https://openai.com/index/introducing-gpt-rosalind/ |
| OpenAI | Rosalind Workbench | 未发现完整工作台实现仓库 | 托管科研工作空间；公开插件可复用程度另看许可 | https://developers.openai.com/blog/rosalind-workbench |
| OpenAI | life-science-research 插件 | 官方仓库公开，但不能标成标准开源 | plugin.json 的 license 为 Proprietary；与 MIT 的 ngs-analysis 区分 | https://github.com/openai/plugins/blob/main/plugins/life-science-research/.codex-plugin/plugin.json |
| Anthropic | Claude 模型系列 | 未发现完整模型实现及权重官方仓库 | API 或 Claude 产品；life-sciences 仓库不包含模型 | https://www.anthropic.com/research/claude-for-life-sciences |
| Anthropic | Claude Science | 未发现完整工作台实现仓库 | 科研工作台产品；公开技能与后端产品分离 | https://www.anthropic.com/news/claude-science-ai-workbench |
| NVIDIA | BioNeMo NIM 推理容器及托管接口 | 不等于 fork 底层模型开源代码 | 按具体容器、模型与产品条款访问；底层模型有些开源、有些开放权重 | https://docs.nvidia.com/bionemo-framework/latest/models/evo2/ |
| NVIDIA | Parabricks GPU 实现及分发容器 | 未发现完整产品源码官方仓库 | 容器分发；免费使用不等于开源，支持服务可能收费；不要沿用旧版强制收费表述 | https://docs.nvidia.com/clara/parabricks/about-parabricks/end-user-license-agreements |
| NVIDIA | cuEquivariance 外部 CUDA ops 包 | 本仓库 Apache-2.0 不自动覆盖外部二进制包 | README 分开安装 frontend 与 ops；各安装包许可另查 | https://github.com/NVIDIA/cuEquivariance |

## 不能误分类的项目

- BioNeMo Recipes 和 Agent Toolkit 具有公开代码及明确许可，不能把整个 BioNeMo 品牌归为闭源。
- Proteina 仓库公开，但使用自定义 NVIDIA License；源代码与权重许可都应单独判断。
- Claude for Life Sciences 是产品及生态整合，不等于一个独立开源生物模型；其中第三方数据服务也不是 Anthropic 自有闭源模型。
- Anthropic 的科研实验室、OpenAI 的研究合作及 NVIDIA/Lilly 的计算设施不是可 fork 的软件产品；不列为普通闭源代码项目。
- Evo 2、Boltz、OpenFold 等由外部研究团队开发或合作开发；接入 BioNeMo 不改变其原始作者及许可。

## 对你后续工作的意义

可优先迁移的是公开科研技能的输入输出、流程路由、证据记录和计算调用方式。模型科研能力、完整工作台、远程数据库及实验设施不能靠 fork 获得。用于自己的 benchmark 时，应单独记录模型版本、服务版本、预算、数据来源和实际执行结果。
