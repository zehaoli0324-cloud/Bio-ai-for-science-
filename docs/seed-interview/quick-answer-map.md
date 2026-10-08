# Seed STEM 模拟面试 Quick Answer Map

本文件用于面试前快速复习。详细内容见 `docs/seed-interview/README.md`。

## 1. 我的定位

我希望补的是 Seed 分子/蛋白设计之后的 **cellular functional feedback layer**：

`Protein/Molecule → Structure → Cellular State → Dynamic Phenotype → Experimental Feedback`

我原来的活细胞荧光成像经验使我比较熟悉真实 biological readout；近期 Benchmark / Agent 工作则让我更关注如何严格评价模型的科学有效性和能力边界。

## 2. 三个最重要的研究问题

### Q1：AI 在荧光成像中最有价值的地方是什么？

不是简单美化图像，而是把原始 fluorescence movie 转换成可靠、可量化、可预测的 biological state：从 segmentation/tracking，到 phenotype representation，再到 future-state prediction 和 experimental decision。

### Q2：为什么动态表型值得做？

静态 endpoint 会丢失 latency、amplitude、duration、recovery 和 cell-to-cell heterogeneity。两个候选在终点相同，动态轨迹可能完全不同，因此动态表型更接近功能机制，也更适合作为设计反馈。

### Q3：它和 Seed 的蛋白设计有什么关系？

结构/affinity 只能回答分子层问题，不能保证蛋白在细胞中表达、定位和信号功能正确。高内涵和活细胞成像可以提供 localization、signaling dynamics、toxicity、morphology、cell fate 等 functional reward，把设计闭环延伸到真实 cellular function。

## 3. Virtual Cell 核心回答

Virtual Cell 理想上是 `initial cell state + perturbation → future cell-state distribution`。当前多数工作只覆盖其中一部分，例如 transcriptome prediction。

对于 de novo protein，目前不能可靠完成 sequence → full cellular dynamics。更现实的研究路线是先用 protein sequence/structure embedding 表示扰动，再预测 transcriptome/morphology/dynamic phenotype，并严格测试 unseen-protein generalization。

Virtual Cell 与显微成像不是替代关系：前者负责 prediction，后者负责 measurement 和 functional validation。

## 4. 最值得讲的 JUMP 思路

JUMP ORF 提供 `protein/gene overexpression → Cell Painting morphology`。

可以进一步做：

`ESM embedding + structure embedding → morphology profile`

并采用 protein-family holdout，而不是随机切分，测试是否真的能泛化到未见蛋白。

## 5. AI 能力边界

按下面顺序判断：

`same lab → cross batch → cross microscope → cross cell line → cross species → unseen perturbation → unseen protein`

随机 test set 上表现好只说明 interpolation 能力。真正对 AI for Science 有意义的是 distribution shift 和 extrapolation。

同时始终区分：

`prediction ≠ explanation ≠ causality`

## 6. 图像模型科学验证

不能只看视觉指标。

恢复：PSNR/SSIM + spot count + distance + peak time + trajectory statistics + downstream biological decision。

分割：Dice/IoU + downstream morphology/intensity stability。

Embedding：必须检查 batch、microscope、exposure、plate-position shortcut。

## 7. Benchmark 能力怎么讲

我做 Benchmark 时比较关注：oracle 独立性、shortcut、hidden-state recovery、negative controls、process scoring、difficulty calibration 和 failure attribution。

这套能力可以迁移到 Virtual Cell：不是只问模型 accuracy 多高，而是明确模型在哪种 perturbation、哪种 distribution shift、哪种科学决策上开始失效。

## 8. 最后统一到闭环

最终希望做的是：

`Design → Predict → Experiment → Measure → Learn → Redesign`

一句话：**让活细胞成像成为 Virtual Cell 和真实细胞之间的功能验证层，并进一步成为蛋白/分子设计的反馈信号。**
