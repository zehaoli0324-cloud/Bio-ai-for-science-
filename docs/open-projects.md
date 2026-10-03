# 官方公开仓库清单

核查日期：2026-10-04。公开仓库不一律等于标准开源；许可按下表处理。

| 目录 | 官方仓库 | 用途 | 许可边界 |
|---|---|---|---|
| openai/plugins | [openai/plugins](https://github.com/openai/plugins) | 生命科学研究与 NGS 分析插件；重点看 plugins/ngs-analysis，研究插件单独标为专有 | 混合：ngs-analysis 清单 MIT；life-science-research 清单 Proprietary；根目录未发现统一许可证 |
| anthropic/life-sciences | [anthropics/life-sciences](https://github.com/anthropics/life-sciences) | 生命科学技能及 MCP 插件目录；第三方服务器不一定在仓库内 | 按技能目录核查；根目录未发现统一许可证 |
| nvidia/bionemo-agent-toolkit | [NVIDIA-BioNeMo/bionemo-agent-toolkit](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit) | 科研 Agent 技能与 NIM/GPU 工具调用接口 | 代码 Apache-2.0；技能和文档 CC-BY-4.0 |
| nvidia/bionemo-recipes | [NVIDIA-BioNeMo/bionemo-recipes](https://github.com/NVIDIA-BioNeMo/bionemo-recipes) | 生物基础模型训练、适配和 GPU 加速配方 | Apache-2.0；模型权重另查 |
| nvidia/proteina | [NVIDIA-BioNeMo/proteina](https://github.com/NVIDIA-BioNeMo/proteina) | 流模型蛋白结构生成研究实现 | 自定义 NVIDIA License；不归为标准宽松开源 |
| nvidia/nvMolKit | [NVIDIA-BioNeMo/nvMolKit](https://github.com/NVIDIA-BioNeMo/nvMolKit) | GPU 分子相似度、构象生成及几何优化 | Apache-2.0 |
| nvidia/cuEquivariance | [NVIDIA/cuEquivariance](https://github.com/NVIDIA/cuEquivariance) | 等变神经网络及结构预测计算加速 | 仓库文件 Apache-2.0；外部 CUDA ops 另查 |
| nvidia/generative-virtual-screening | [NVIDIA-BioNeMo-blueprints/generative-virtual-screening](https://github.com/NVIDIA-BioNeMo-blueprints/generative-virtual-screening) | 生成式虚拟筛选工作流蓝图；运行依赖单独授权的服务 | Apache-2.0；NIM 服务授权另查 |

## 版本与来源

- openai/plugins: `5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f`；上游提交时间 2026-09-28T17:08:07Z。
- anthropics/life-sciences: `e96556b637b56d6cc3a5ad33987009be9e60aa5c`；上游提交时间 2026-05-08T16:54:54Z。
- NVIDIA-BioNeMo/bionemo-agent-toolkit: `0b322cd4203e5120889ec00aafa65319c04935fd`；上游提交时间 2026-10-01T21:52:17Z。
- NVIDIA-BioNeMo/bionemo-recipes: `4a287cbaf8ec633d4a3143027f1cb6f4b9d7787a`；上游提交时间 2026-10-01T16:51:42Z。
- NVIDIA-BioNeMo/proteina: `a44b407daf6a5358e43cd68907f3e3f1cbc65fdc`；上游提交时间 2025-07-24T19:05:40Z。
- NVIDIA-BioNeMo/nvMolKit: `f8216a390ce91bbcca597b3ced0552a37bca4bb7`；上游提交时间 2026-10-02T21:31:50Z。
- NVIDIA/cuEquivariance: `70674ada7a00372e88ebe99969c700a6dcddd08f`；上游提交时间 2026-09-24T00:25:54Z。
- NVIDIA-BioNeMo-blueprints/generative-virtual-screening: `f3f1d381a3605d4f8e3d5556ea523b6022394132`；上游提交时间 2025-11-07T19:16:17Z。

bionemo-framework 已重定向到 bionemo-recipes，仓库 ID 相同，不重复 fork。Proteina 使用自定义许可，OpenAI plugins 含专有组件，Anthropic 根目录缺少统一许可证：这些收录于公开源码类别，不将整个仓库重新授权为 MIT/Apache。

## 核查依据

- [OpenAI NGS 插件清单](https://github.com/openai/plugins/blob/main/plugins/ngs-analysis/.codex-plugin/plugin.json)
- [OpenAI 研究插件清单](https://github.com/openai/plugins/blob/main/plugins/life-science-research/.codex-plugin/plugin.json)
- [BioNeMo Recipes 许可证](https://github.com/NVIDIA-BioNeMo/bionemo-recipes/blob/main/LICENSE/license.txt)
- [Agent Toolkit 许可证](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit/blob/main/LICENSE)
- [nvMolKit 许可证](https://github.com/NVIDIA-BioNeMo/nvMolKit/blob/main/LICENSE/License.txt)
- [Proteina 许可证](https://github.com/NVIDIA-BioNeMo/proteina/blob/main/LICENSE)
- cuEquivariance 与虚拟筛选蓝图：各官方仓库 README 和 LICENSE。

建议在 fork 后保留所有 LICENSE/NOTICE 和模型条款；公开的 MCP 插件配置不表示远程服务器实现已开源。

