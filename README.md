# 生物 AI for Science：Seed STEM 对标与开源项目地图

核查日期：2026-10-04。整理 Seed STEM 值得对标的国外团队、生命科学相关的官方公开项目、闭源产品和 benchmark 方向。

本仓库聚焦生物、结构生物学、蛋白设计、药物发现和科研 Agent，暂不纳入量子化学。Seed STEM 的完整对标建议先读 [Seed 对标地图](docs/seed-benchmark-map.md)，再查看下面固定版本的上游 submodule。

## 项目目录

| 公司 | 目录 | 内容 |
|---|---|---|
| OpenAI | openai/plugins | 科研与 NGS 插件；插件各自许可证不同 |
| Anthropic | anthropic/life-sciences | 生命科学技能及 MCP 插件目录 |
| NVIDIA | nvidia/bionemo-agent-toolkit | 科研 Agent 技能与计算工具接口 |
| NVIDIA | nvidia/bionemo-recipes | 生物基础模型训练及 GPU 加速配方 |
| NVIDIA | nvidia/proteina | 蛋白结构生成研究实现 |
| NVIDIA | nvidia/nvMolKit | 分子相似度、构象生成、几何优化 |
| NVIDIA | nvidia/cuEquivariance | 等变网络与结构预测计算加速 |
| NVIDIA | nvidia/generative-virtual-screening | 生成式虚拟筛选蓝图 |

## 使用

每个项目目录是引用官方上游的 Git submodule，固定到 projects.json 中记录的 commit。GitHub fork 是独立仓库，无法嵌套在文件夹内；此仓库采用上游 submodules，尚未创建个人 forks。GitHub 网页点击项目目录会跳转到对应的上游版本。

```bash
git clone --recurse-submodules https://github.com/zehaoli0324-cloud/Bio-ai-for-science-.git
cd Bio-ai-for-science-
```

如果已经普通克隆：

```bash
git submodule update --init --recursive
python3 scripts/verify_submodules.py
```

默认恢复固定版本，不追踪上游最新提交。修改后在项目自身提交，再在汇总仓库提交新的 submodule 指针。更新版本时同步 projects.json 的 SHA。

## 清单

- [Seed STEM 对标地图、具体开源项目与 benchmark 设计](docs/seed-benchmark-map.md)
- [官方公开项目与许可证](docs/open-projects.md)
- [闭源与受限项目](docs/closed-projects.md)
- [固定版本记录](projects.json)

bionemo-framework 已重定向到 bionemo-recipes，不重复收录。OpenAI plugins 收录整个上游，但重点是 plugins/ngs-analysis 和 plugins/life-science-research：前者清单标 MIT，后者标 Proprietary，不能把整个仓库视为标准开源。Proteina 采用自定义 NVIDIA License。代码、权重、数据及远程服务的许可分别判断。

## 验证范围

已核实来源仓库、提交 SHA、许可证边界，并检查汇总目录与版本记录一致。未运行上游项目、下载模型权重或调用付费服务；收录不代表科学效果或生产可用性已验证。
