# ByteDance Seed STEM / AI for Science 面试知识索引

> 整理日期：2026-10-08
>
> 用途：将本轮围绕 Seed STEM、AI + 荧光成像、动态细胞表型、Virtual Cell、蛋白/分子设计、JUMP/Cell Painting、科学 Benchmark 与计算生物学基础的讨论统一归档，作为模拟面试的主索引。

## 0. 一句话研究定位

我的核心切入点不是与蛋白结构模型正面竞争，而是补上 **分子设计到真实细胞功能之间的反馈层**：

**Molecule / Protein → Structure → Cellular State → Dynamic Phenotype → Experimental Feedback**

其中活细胞荧光成像提供真实细胞的功能观测；Virtual Cell 提供细胞状态预测；动态表型模型把连续时间信息压缩成可用于筛选、评价和下一轮设计的功能表征。

长期目标是形成：

**Design → Predict → Experiment → Measure → Learn → Redesign**

即 Phenotype-in-the-loop Protein Design / Closed-loop AI Biology。

---

## 1. 面试叙事主线

### 1.1 我的实验背景能提供什么

已有科研经验集中在细胞生物学、分子成像和活细胞动态过程，包括 CRISPR 活细胞 DNA 成像、增强子-启动子动态、DNA 双链断裂与 53BP1 修复、RNA 荧光适配体/细胞 pH、线粒体 pH 等。

这类经验的计算价值不是“会拍荧光图”，而是知道：

- 什么是有生物学意义的动态事件；
- 什么是成像伪影、漂白、曝光差异和批次效应；
- 哪些 readout 能真正反映功能；
- 如何从图像恢复、分割、追踪一直走到科学结论；
- 如何判断 AI 输出是预测、解释还是因果证据。

### 1.2 从实验生物学转向 AI for Science 的逻辑

研究路线可以表述为：

**实验测量 → 图像计算 → 表型表征 → 动态状态建模 → 扰动预测 → Virtual Cell → 分子设计反馈 → 自动科研/Benchmark。**

这不是放弃实验背景，而是把实验经验转化为模型的 measurement layer、functional readout 和 scientific verifier。

---

## 2. AI × 荧光显微成像

### 2.1 高内涵成像是什么

High-content imaging 不是单纯“大量拍图”，而是：

**标准化实验 + 多通道成像 + 自动分割 + 特征提取 + 统计分析 → 高维细胞表型。**

AI 主要进入三层：

1. **信息提取**：分割、spot detection、tracking；
2. **状态解释**：细胞周期、DNA damage、扰动类型、细胞状态；
3. **图像恢复**：denoising、deconvolution、super-resolution、unmixing。

### 2.2 为什么荧光图像不能简单当普通 RGB 图像

像素强度同时受到曝光、探针表达、漂白、PSF、背景、探测器噪声、显微镜参数等影响。同一种生物状态在不同仪器/批次下可以产生不同像素分布。

因此模型必须验证跨批次、跨仪器和跨实验条件的稳定性，不能只验证随机切分 accuracy。

### 2.3 Embedding

Embedding 是模型把细胞图像映射成高维数值向量，例如一张细胞图像 → 768 维向量。它可用于相似性检索、聚类、分类和扰动表征。

关键风险：embedding 可能编码 microscope、batch、exposure、plate position，而不是 biology。

### 2.4 CellProfiler vs Deep Embedding

CellProfiler 输出面积、强度、纹理、共定位等显式可解释特征；深度 embedding 自动学习高维特征，表达能力更强，但可解释性更弱。

合理策略：CellProfiler 作为 interpretable baseline，再检验 deep embedding 是否增加了可复现的生物信号。

### 2.5 Shortcut learning

典型例子：control 全部由显微镜 A 拍摄，treatment 全部由显微镜 B 拍摄。模型可能通过背景亮度或噪声识别实验组，而没有识别细胞表型。

其他 shortcut 包括 plate position、cell density、实验日期、batch。

控制方法：随机化、跨 batch / instrument 验证、盲测、严格 train/test split、negative controls。

### 2.6 分割为什么重要

几乎所有单细胞定量都依赖 cell/nucleus boundary。merge、split、missed cell 或组间系统性偏差会向下游传播。

常用指标：

- Dice = 2|A∩B|/(|A|+|B|)
- IoU = |A∩B|/|A∪B|

但高 Dice / IoU 不等于科学测量可靠，还必须验证面积、强度、spot count、trajectory 等下游量是否稳定。

### 2.7 图像恢复不能只看 PSNR / SSIM

对于科学图像，视觉更漂亮不等于科学信息更真实。恢复算法还应验证：

- spot 数量是否守恒；
- 分子距离是否偏移；
- peak time 是否改变；
- trajectory statistics 是否失真；
- 下游 biological decision 是否一致。

### 2.8 形态学特征与计算方法

形态：area、perimeter、major/minor axis、circularity、eccentricity、solidity、convexity。

强度：mean、median、integrated intensity、coefficient of variation。

纹理：contrast、homogeneity、energy、entropy。

空间：radial distribution、colocalization、spot count。

典型计算链：convolution/filtering → background correction → threshold / watershed 或 Cellpose/U-Net/StarDist → geometry/statistics → PCA/UMAP/clustering → deep embedding → temporal analysis。

---

## 3. 动态表型与活细胞成像

静态 Cell Painting 主要回答“细胞现在长什么样”；动态表型进一步回答：

**什么时候响应、响应多强、持续多久、能否恢复、不同细胞是否一致、下一步会发生什么。**

关键指标：

- ERK pulse amplitude：激活幅度；
- pulse duration：持续时间；
- response latency：刺激到响应的延迟；
- fraction of responding cells：发生响应的细胞比例；
- recovery time：恢复到基线附近所需时间；
- off-target morphology：非预期形态变化，如 rounding、核缩小、线粒体碎裂、空泡化、脱落等。

动态表型的重要性在于：两个候选蛋白或药物可能具有相同 endpoint，但 latency、amplitude、duration、recovery 和 heterogeneity 完全不同。

### Dynamic Cell Embedding

基本设计：

`frame_t → image encoder → z_t → temporal Transformer / state-space model → Z_trajectory`

目标不再只是识别单帧，而是预测：

- DNA locus movement；
- 53BP1 focus 形成/消失；
- pH trajectory；
- drug response trajectory；
- next cell state。

这是从 static representation 向 cellular dynamics/world model 发展的自然路径。

---

## 4. Virtual Cell

### 4.1 定义

Virtual Cell 的理想目标是：给定细胞初态和扰动，预测后续细胞状态及其分布。

当前很多工作实际上更接近 perturbation-response model，例如预测 transcriptome，而不是完整意义上的细胞数字孪生。

### 4.2 为什么转录组经常成为预测目标

因为 transcriptome 数据规模大、标准化程度高、与扰动数据容易配对。但 transcriptome 只是细胞状态的一个 readout，并不等于完整功能状态。

### 4.3 新蛋白的理想预测输出

对一个新设计蛋白，理想系统应预测：

**sequence → structure → target/interaction → localization → signaling → transcriptome/proteome → morphology → dynamic phenotype → fate/toxicity。**

目前不存在能够对任意 de novo protein 稳定完成整条链的通用模型。最大的困难是跨尺度误差累积和 OOD generalization。

### 4.4 新药/小分子的理想输出

重点包括 target engagement、pathway response、efficacy、selectivity、toxicity、resistance 等。

Virtual Cell 不能直接等价于体内药效预测，因为还缺 PK/PD、组织分布、屏障、免疫系统和微环境。

### 4.5 可借鉴的模型

- PIE：扰动表征、unseen perturbation；适合研究如何把 protein representation 接入细胞响应预测。
- PerturbNet：perturbation embedding → cell-state distribution；可以尝试用 protein sequence/structure embedding 替换简单 perturbation ID。
- MultiVCDiff：连接 perturbation、transcriptome 和 Cell Painting morphology。
- MorphGen：形态/细胞图像生成与 phenotype modeling。
- CPA、STATE 等：作为 perturbation-response / cell-state modeling 的参考。

### 4.6 Virtual Cell 与活细胞成像不是竞争关系

更合理的关系是：

**Virtual Cell = prediction layer**

**Live-cell imaging = measurement + functional validation layer**

预测模型提出“细胞应该怎么响应”，动态显微实验验证真实细胞是否按照预测轨迹响应，并把误差反馈给模型。

---

## 5. 与 Seed 蛋白/分子设计的连接

Seed 已有的蛋白结构/设计方向可理解为解决 molecule/sequence/structure 层的问题。我的差异化价值是向下连接 cellular function。

### 5.1 为什么 binding affinity 不够

一个 binder 即使 affinity 很高，也可能存在：

- 表达失败；
- localization 错误；
- target inaccessible；
- aggregation；
- signaling 不符合预期；
- off-target effects；
- toxicity。

所以结构和结合能力不是最终功能。

### 5.2 Image-derived Functional Reward

可以把显微图像转换为候选设计的 functional reward，例如：

- localization score；
- ERK dynamics；
- cell viability；
- mitochondrial morphology；
- DNA damage response；
- condensate/self-assembly behavior；
- phenotype similarity / rescue score。

这些指标可以进入 active learning 或下一轮 protein design 的 fitness function。

### 5.3 Phenotype-in-the-loop Protein Design

理想闭环：

**Design → Express → High-content / Live-cell Imaging → Quantify Phenotype → Update Model → Redesign**

因此荧光成像不是设计模型的替代，而是给设计模型提供真实 cellular functional feedback。

---

## 6. JUMP / Cell Painting

JUMP = Joint Undertaking for Morphological Profiling，是围绕大规模标准化 Cell Painting 的合作项目/生态，而不是单个算法。

Cell Painting 使用多通道荧光标记细胞核、细胞质、线粒体、内质网、细胞骨架等结构，然后把图像转换为单细胞高维 morphology profile。

相关扰动包括：

- JUMP Compound：chemical perturbation → phenotype；
- JUMP CRISPR：gene knockout → phenotype；
- JUMP ORF：ORF overexpression → phenotype；
- CPJUMP1：规模更小、经过整理的化学/遗传匹配 benchmark，可用于方法验证。

### JUMP ORF 为什么与 Protenix / Protein Design 有连接

ORF 数据天然形成：

**gene/protein overexpression → cellular morphology**

下一步可以把简单 gene ID 换成：

**ESM protein embedding + structure embedding → Cell Painting profile**

并采用 protein-family holdout 测试模型能否泛化到未见蛋白，而不是只记忆 gene identity。

重要边界：morphology similarity 不能直接证明相同 MoA，只能作为机制假设和候选筛选证据。

---

## 7. 代表性开源方向

### 表征与显微图像

- Meta Cell-DINO / Channel Adaptive DINO：自监督 fluorescence representation；处理不同 channel configuration。
- SubCell：蛋白亚细胞定位/表征；SubCellPortable 适合直接推理。
- OpenPhenom / Recursion：大规模 perturbation imaging → phenotype representation。
- Microsoft GigaTIME / GigaTIME-Flash：H&E → virtual multiplex protein/IF signal，强调图像到 biological signal 的预测；输出是模型预测而非直接测量。
- CZI MorphGen：cell morphology / image generation。
- NVIDIA VISTA-2D：cell instance segmentation。
- Google/ISTA LICONN：measurement + registration + ML reconstruction，展示实验系统与算法协同设计。

建议实际研究优先级：

1. SubCellPortable + subcell-analysis；
2. Cell-DINO；
3. OpenPhenom；
4. MorphGen；
5. 在静态 encoder 后加入 temporal model，形成 Dynamic Cell Embedding。

---

## 8. 科学能力边界：如何判断 AI 真正有价值

建议用五层判断。

### 8.1 Scientific problem value

先判断瓶颈是否真正重要，而不是“能不能套 AI”。

### 8.2 AI incremental value

必须和传统算法/统计基线比较，证明 AI 提供新增价值。

### 8.3 Generalization boundary

逐层增加难度：

**same lab → cross batch → cross microscope → cross cell line → cross species → unseen perturbation → unseen protein**

真正的科学价值往往出现在 distribution shift 和 extrapolation，而不仅是 interpolation。

### 8.4 Prediction ≠ explanation ≠ causality

模型能预测 phenotype，不代表理解机制；能给出 feature attribution，也不代表建立因果关系。

### 8.5 是否进入实验闭环

成熟度可以分为：

1. Measurement：分割、去噪、追踪；
2. Phenotype：识别细胞状态；
3. Prediction：扰动 → future phenotype；
4. Design / Intervention：模型决定下一实验或候选设计。

最高价值不是“AI 帮人看图”，而是 AI 能参与实验决策并通过真实 measurement 获得反馈。

---

## 9. Benchmark / Agent 能力如何融入 Seed 叙事

我的另一条能力不是单纯训练视觉模型，而是构建能够检验 scientific reasoning 的 benchmark/harness。

相关经验包括 L1000、Perturb-seq、Harbor Science Bench Factory、GroundSignal 等，核心方法论是：

- oracle / truth 与被测模型独立；
- 防止 endpoint shortcut；
- hidden-state recovery；
- process-aware scoring；
- verifier 与 reference solution 分离；
- negative controls；
- distribution shift；
- difficulty calibration；
- failure attribution；
- 从真实科研来源生成任务而不是无约束合成题。

这与 Virtual Cell / scientific agent 的连接是：未来不仅需要训练模型，还需要知道模型到底在哪个科学层级有效、在哪个分布外条件失效。

---

## 10. 统计与计算生物学基础

### Pearson vs Spearman

Pearson：线性相关。

Spearman：基于 rank 的单调相关，对非线性单调关系和异常值通常更稳健。

Correlation ≠ causation。

### Pseudoreplication

同一个 well 中几千个细胞不是几千个独立 biological replicates。独立单位可能是 well、batch、donor、culture。

解决方法包括 pseudobulk、hierarchical/bootstrap、mixed-effects model。

### p-value / effect size / FDR

p-value 是 null hypothesis 下观察到当前或更极端数据的概率，不是 null 为真的概率。

科学判断还需要 effect size + confidence interval；多重检验使用 Benjamini-Hochberg FDR 等控制。

### RNA-seq

FASTQ → FastQC/MultiQC → STAR alignment 或 Salmon quantification → gene × sample matrix → QC/normalization → DESeq2 negative-binomial model → log2FC + adjusted p-value → GO/KEGG/Reactome/GSEA。

### DNA-seq

FASTQ → QC → BWA-MEM2 → BAM sorting / duplicate handling → variant calling → VCF → filtering → VEP annotation。

同时关注 coverage、base quality、mapping quality、allele balance、VAF。目标不是列 variant，而是得到可信变异及其功能后果。

---

## 11. 模拟面试 50 题索引

### A. AI + 荧光成像

1. 什么是高内涵成像？与普通荧光成像有什么区别？
2. AI 在荧光成像中的三类核心作用是什么？
3. 为什么荧光图像不能简单当 RGB 图像处理？
4. 什么是 embedding？
5. CellProfiler features 与 deep embedding 有什么区别？
6. 什么是 shortcut learning？
7. 哪些 cell morphology 可以数字化？
8. 为什么 segmentation 是关键环节？
9. Dice 和 IoU 有什么区别？
10. 为什么图像恢复不能只看 PSNR/SSIM？

### B. Dynamic Phenotype

11. 什么是 dynamic phenotype？
12. 为什么动态表型可能比静态 Cell Painting 更有价值？
13. Live-cell tracking 的核心计算问题是什么？
14. 什么是 MSD？为什么用于分子/细胞运动分析？
15. ERK pulse amplitude / duration / latency 分别是什么？
16. fraction of responding cells 为什么重要？
17. recovery time 反映什么？
18. off-target morphology 是什么？
19. 为什么 DNA damage / chromatin 特别适合动态成像？
20. 什么是 Dynamic Cell Embedding？

### C. Virtual Cell

21. Virtual Cell 与普通 transcriptome prediction 有什么区别？
22. 为什么 transcriptome 经常成为 Virtual Cell 的目标？
23. 对新蛋白，理想 Virtual Cell 应预测什么？
24. 对新药，理想 Virtual Cell 应预测什么？
25. Virtual Cell 能直接预测 in vivo efficacy 吗？
26. 哪些模型可以作为 Virtual Cell prototype？
27. 为什么 PIE 适合研究 new protein → cell response？
28. 为什么 PerturbNet 适合 Protein-to-Cell？
29. MultiVCDiff / MorphGen 的意义是什么？
30. Virtual Cell 与 live-cell imaging 是竞争关系吗？

### D. Molecular / Protein Design

31. 为什么 binding affinity 不够？
32. 荧光成像如何直接帮助 protein design？
33. 什么是 image-derived functional reward？
34. 什么是 Phenotype-in-the-loop Protein Design？
35. 为什么 dynamic phenotype 对设计更有价值？
36. 哪些蛋白最需要 dynamic microscopy？
37. 新蛋白可以直接放进 Virtual Cell 预测吗？
38. 新蛋白和新药，哪一个更容易做 Virtual Cell prediction？
39. PUREdrop-like 工作为什么值得关注？
40. 要把 imaging 用于 molecular design，需要哪些计算技能？

### E. JUMP / Cell Painting

41. JUMP 是什么？
42. CPJUMP1 和 JUMP ORF 有什么区别？
43. 为什么 JUMP ORF 能与 Protenix 接起来？
44. 什么是 Cell Painting？
45. morphology similarity 能证明相同 mechanism 吗？

### F. Statistics / Bioinformatics

46. Pearson 与 Spearman 的区别？
47. 为什么很多 cells 不等于很多 biological replicates？
48. p-value、effect size、FDR 分别回答什么？
49. RNA-seq 标准分析流程？
50. DNA-seq 标准分析流程？

---

## 12. 面试回答模板

现场回答尽量遵循：

**结论 → 核心机制 → 自己的科研/项目例子 → 与 Seed / AI for Science 的连接。**

避免两个极端：

- 只讲 wet-lab 细节，看不出计算价值；
- 只讲 AI buzzword，看不出 biological grounding。

最重要的统一句式是：

> 我比较关注的不是单独把显微图像做得更漂亮，而是把成像变成可靠的细胞状态测量。进一步把静态表型扩展成动态表型，再把这个功能 readout 接到 Virtual Cell 和蛋白/分子设计之后。这样上游模型负责提出候选和预测，真实细胞成像负责验证功能并提供反馈，最终形成 Design–Predict–Experiment–Measure–Learn–Redesign 的闭环。

---

## 13. 核心边界声明

面试中需要主动避免过度承诺：

- Virtual Cell 目前并非完整细胞数字孪生；
- arbitrary de novo protein → full cellular dynamics 尚未解决；
- morphology similarity 不等于相同 MoA；
- image generation 不等于真实 measurement；
- high PSNR/SSIM 不等于 biological fidelity；
- correlation / prediction 不等于 causality；
- in vitro cellular response 不等于 in vivo efficacy；
- embedding 必须排除 batch / instrument shortcut；
- 大量单细胞不能替代 biological replicate。

这些限制不是削弱研究方向，而是定义真正值得解决的科学问题。
