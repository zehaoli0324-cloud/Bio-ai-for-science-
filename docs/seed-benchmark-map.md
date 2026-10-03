# Seed STEM 对标地图：国外大厂的 Bio AI for Science

核查日期：2026-10-04。本页只讨论生物、结构生物学、蛋白设计、药物发现和科研 Agent；暂不纳入量子化学。这里的“开源”只描述仓库或组件的公开状态，代码、模型权重、训练数据、数据库和托管服务的许可必须分别核对。

## 先给结论

Seed STEM 最值得直接对标的是 **Google DeepMind/Isomorphic Labs 的生物基础模型与结构预测**、**Evolutionary Scale/Biohub 和 Baker Lab 的蛋白设计**、**Microsoft AI for Science 的蛋白动力学**，以及 **NVIDIA BioNeMo 的训练、部署和工作流平台**。OpenAI 和 Anthropic 更适合作为科研 Agent、工具调用、安全评测和科学工作流的上游参照，而不是 Protenix 或 PAR 的一比一模型对手。

从 Seed 的现有项目出发，可以形成以下优先级：

| 优先级 | 方向 | Seed 侧锚点 | 国外对标团队/项目 | 对标问题 |
|---|---|---|---|---|
| P0 | 生物分子复合物结构预测 | [Protenix](https://github.com/bytedance/Protenix) | Google DeepMind [AlphaFold 3](https://github.com/google-deepmind/alphafold3)、[OpenFold](https://github.com/aqlaboratory/openfold)、[Boltz](https://github.com/jwohlwend/boltz) | 蛋白-蛋白、蛋白-配体、核酸和共价修饰的结构精度、置信度校准、推理成本 |
| P0 | 蛋白生成与 binder 设计 | [PAR](https://github.com/ByteDance-Seed/par-protein) | Biohub [ESM](https://github.com/Biohub/esm)、Rosetta Commons [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion)、[ProteinMPNN](https://github.com/dauparas/ProteinMPNN)、Baker Lab [RoseTTAFold All-Atom](https://github.com/baker-laboratory/RoseTTAFold-All-Atom) | 设计性、结构可折叠性、表达/溶解度、结合亲和力、细胞或体外功能命中率 |
| P0 | 冷冻电镜与结构异质性 | [CryoFM](https://github.com/ByteDance-Seed/cryofm) | RELION、DeepEMhancer、EMReady、[Cryo-EM 方向说明](https://bytedance-seed.github.io/cryofm/) | 半图 FSC、局部分辨率、模型-密度一致性、异质性恢复和真实颗粒外部验证；目前没有一个完全对应的国外大厂公开模型，属于 Seed 可建立差异化的位置 |
| P0 | 药物发现与自由能工作流 | [Felis](https://github.com/ByteDance-Seed/felis) | NVIDIA [BioNeMo](https://www.nvidia.com/en-us/gpu-cloud/bionemo.md)、[OpenFE](https://github.com/OpenFreeEnergy/openfe)、商业对手 Isomorphic Labs/Schrödinger | 结合构象、虚拟筛选富集、自由能误差、端到端命中率、GPU 成本和可复现性 |
| P1 | 蛋白构象分布与动力学 | 暂无同等成熟的 Seed 锚点 | Microsoft [BioEmu](https://github.com/microsoft/bioemu) | 是否能从单序列生成合理的构象集合，而不是只生成一个静态结构；需要和实验 ensemble 或高质量模拟对比 |
| P1 | 基因组基础模型 | 可作为 Seed 生物模型的扩展方向 | Google DeepMind [AlphaGenome](https://github.com/google-deepmind/alphagenome) | 变异效应、调控元件和长序列上下文；同时评估公开 API/代码与模型访问条件 |
| P1 | 科研 Agent 与实验规划 | 可连接 Seed 模型、数据库和实验记录 | OpenAI [Science](https://openai.com/science/)、[GPT-Rosalind](https://openai.com/index/introducing-gpt-rosalind/)、[FrontierScience](https://openai.com/index/frontierscience/)，Anthropic [Life Sciences](https://www.anthropic.com/research/claude-for-life-sciences)，NVIDIA [BioNeMo Agent Toolkit](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit) | 证据检索、工具调用、可复现研究流程、实验设计质量和安全边界，而不只是通用问答分数 |
| P1 | 训练/推理基础设施 | Seed 模型训练和规模化服务 | NVIDIA [BioNeMo Recipes](https://github.com/NVIDIA-BioNeMo/bionemo-recipes)、[cuEquivariance](https://github.com/NVIDIA/cuEquivariance) | 多节点训练、等变算子、推理吞吐、显存占用、部署与模型版本管理 |

## 具体开源项目

### Seed 侧基线

| 项目 | 主要用途 | 公开状态 |
|---|---|---|
| [Protenix](https://github.com/bytedance/Protenix) | 高精度生物分子结构预测 | 仓库 Apache-2.0；不同版本的权重、数据和使用条款单独核对 |
| [PAR](https://github.com/ByteDance-Seed/par-protein) | 多尺度蛋白骨架生成 | 仓库 Apache-2.0 |
| [CryoFM](https://github.com/ByteDance-Seed/cryofm) | 冷冻电镜密度图生成基础模型 | 仓库 Apache-2.0 |
| [Felis](https://github.com/ByteDance-Seed/felis) | 蛋白-配体自由能计算 | 仓库 Apache-2.0 |

### 国外直接技术对标

| 项目 | 团队 | 适合放入本仓库的原因 | 开放程度 |
|---|---|---|---|
| [AlphaFold 3](https://github.com/google-deepmind/alphafold3) | Google DeepMind / Isomorphic Labs | 复合物结构预测的直接对标 | 推理代码 Apache-2.0；模型参数须从 Google 获取并遵守 [权重条款](https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md) |
| [AlphaFold 2](https://github.com/google-deepmind/alphafold) | Google DeepMind | 结构预测的可复现实验基线 | 代码 Apache-2.0；数据库、权重和运行资源另行核对 |
| [OpenFold](https://github.com/aqlaboratory/openfold) | AQLab | 可训练、GPU 友好的 AlphaFold 2 复现 | 仓库 Apache-2.0 |
| [Boltz](https://github.com/jwohlwend/boltz) | 独立研究团队 | 开放的生物分子相互作用预测基线 | 仓库 MIT；模型版本和权重条款单独记录 |
| [ESM](https://github.com/Biohub/esm) | Evolutionary Scale / Biohub | 蛋白语言模型、结构预测、设计和 Atlas 工作流 | 当前仓库与模型按各自发布条款核对；历史 [Meta FAIR ESM 仓库](https://github.com/facebookresearch/esm) 已归档 |
| [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion) | Rosetta Commons / Baker Lab | 目标约束的蛋白骨架生成 | 代码公开；仓库未声明标准 SPDX 许可证，使用前逐项核查 |
| [ProteinMPNN](https://github.com/dauparas/ProteinMPNN) | Baker Lab | 从骨架反推氨基酸序列 | MIT |
| [RoseTTAFold All-Atom](https://github.com/baker-laboratory/RoseTTAFold-All-Atom) | Baker Lab | 蛋白、配体和核酸的全原子建模 | 代码公开；许可证和模型权重按仓库说明核查 |
| [OpenFE](https://github.com/OpenFreeEnergy/openfe) | Open Free Energy | Felis 的开放自由能工作流参照 | MIT |
| [BioEmu](https://github.com/microsoft/bioemu) | Microsoft Research | 蛋白平衡构象集合生成 | MIT 代码与公开权重；训练数据和依赖按仓库说明核查 |
| [BioNeMo Recipes](https://github.com/NVIDIA-BioNeMo/bionemo-recipes) | NVIDIA | 生物模型训练、适配和 GPU 规模化配方 | 代码公开；不同模型权重和 NIM 服务有单独条款 |
| [BioNeMo Agent Toolkit](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit) | NVIDIA | 生物科研 Agent 技能、工具和部署接口 | 代码、技能和文档采用不同许可；以仓库 LICENSE 为准 |

### 不能直接 fork 的商业参照

| 团队/产品 | 应该对标什么 | 为什么不能当作开源项目 |
|---|---|---|
| Isomorphic Labs | 结构预测到药物设计的闭环、项目制交付和湿实验反馈 | 商业药物发现公司，没有等价的完整公开产品仓库 |
| OpenAI GPT-Rosalind / Rosalind Workbench | 生物证据整合、工具调用、研究协作和安全访问 | 模型与工作台通过受控服务提供，公开插件不等于模型开源 |
| Anthropic Claude for Life Sciences | 通用模型连接生物数据库、Benchling、实验设计和生物安全评测 | Claude 模型及后端工作台没有完整公开实现 |
| NVIDIA BioNeMo NIM | 模型托管、推理服务、企业部署和 GPU 生态 | NIM 是容器/服务产品；底层模型、服务和许可需要分别判断 |
| Schrödinger FEP+ | 商业级自由能和药物设计流程 | 付费软件，不是可 fork 的开源实现 |

## 建议的 benchmark 设计

不要只用单一公开测试集排名。每个方向至少同时报告以下五类指标，并固定模型版本、数据库版本、硬件、预算和随机种子：

1. **结构预测**：TM-score、DockQ、ligand RMSD、界面接触恢复、置信度校准，以及长序列/低同源/多链分层结果。
2. **蛋白设计**：设计性（designability）、序列恢复率、结构偏差、novelty/diversity、表达与溶解度、结合亲和力和功能命中率。
3. **药物发现**：pose 通过率、虚拟筛选 enrichment、自由能误差、排序稳定性、prospective hit rate、ADMET 和单个候选的计算成本。
4. **冷冻电镜与动力学**：half-map FSC、局部分辨率、模型-密度 FSC、外部颗粒验证、构象覆盖率和物理合理性。
5. **科研 Agent**：任务成功率、证据可追溯性、工具调用成功率、失败恢复、可复现性、实验方案可执行性和安全拒答质量。FrontierScience 这类科学推理 benchmark 可做上游能力指标，不能替代湿实验命中率。

推荐 Seed 优先做三套公开、可复现、能产生真实决策的面板：

- **P0 结构与设计面板**：Protenix、AlphaFold 3、Boltz、OpenFold、ESM、RFdiffusion/ProteinMPNN，在同一套时间切分和 blind targets 上比较。
- **P0 发现面板**：Felis、OpenFE、BioNeMo 工作流和商业参考结果，增加 prospective virtual screening 和盲态 hit rate。
- **P1 科研 Agent 面板**：把结构模型、检索、序列设计、打分器和实验记录串成端到端任务，评估“能否提出下一轮实验”，而不是只评估回答是否流畅。

大规模湿实验验证应作为独立的外部验证层：先用计算模型生成候选，再由盲态、预注册的实验协议验证表达、结合、特异性、稳定性和功能。论文中的离线分数与真实命中率分开记账，避免把模型自评当成药物发现效果。

## 官方入口

- [ByteDance Seed AI for Science](https://seed.bytedance.com/en/direction/ai_for_science)
- [Google DeepMind AlphaFold](https://deepmind.google/science/alphafold/)
- [Microsoft AI for Science / BioEmu](https://www.microsoft.com/en-us/research/workbench/project/bioemu/demo/)
- [NVIDIA BioNeMo](https://docs.nvidia.com/bionemo-framework/latest/main/index.html)
- [OpenAI Science](https://openai.com/science/)
- [Anthropic Biology and Biorisk](https://www.anthropic.com/research/biorisk)
- [Evolutionary Scale / Biohub ESM](https://www.evolutionaryscale.ai/)

本页是路线和项目索引，不代表已运行这些模型或验证其科学效果；真正比较时应在 `projects.json` 之外另存模型版本、权重来源、数据切分、执行日志和实验结果。
