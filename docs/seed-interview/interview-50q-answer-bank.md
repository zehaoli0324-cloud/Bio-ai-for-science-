# Seed STEM 50 题模拟面试 Answer Bank

> 使用方式：每题先给结论，再解释机制，再用个人实验/项目例子，最后连接 Seed。这里保留的是答题骨架，模拟面试时可以扩成 30–90 秒口语答案。

## 1. 什么是高内涵成像？

高内涵成像不是简单拍大量荧光图，而是把标准化实验、多通道成像、自动分割、单细胞特征提取和统计分析连成一个可规模化的 phenotype measurement system。普通 fluorescence imaging 往往关注少量样本和某个局部现象，高内涵强调每个 cell 同时获得 morphology、intensity、texture、spatial distribution 等多维 readout。对 AI 来说，真正重要的是这些 readout 是否跨 batch 可重复，而不是图片数量。

## 2. AI 在荧光成像中的三类作用？

第一是 measurement：segmentation、spot detection、tracking；第二是 state interpretation：cell cycle、DNA damage、perturbation phenotype；第三是 restoration：denoising、deconvolution、super-resolution、unmixing。三类任务证据标准不同，不能用一套 image similarity metric 全部评价。

## 3. 为什么 fluorescence image 不能当普通 RGB？

因为 intensity 不是单纯颜色，而是 fluorophore、exposure、bleaching、PSF、background、detector noise 和 probe dynamics 的混合结果。同样 biology 换 microscope 就可能变 pixel distribution。所以模型必须显式考虑 imaging physics、batch effect 和 calibration。

## 4. 什么是 embedding？

Embedding 是模型把一张 cell image 映射成高维 vector，例如 768 维。它不是手工定义的 area/intensity，而是 learned representation，可以做 similarity、clustering、retrieval、classification。科学上最关键的是证明 embedding 编码的是 biology，而不是 experiment date 或 microscope。

## 5. CellProfiler feature 与 deep embedding 区别？

CellProfiler 是显式、可解释 feature，例如 area、texture、intensity；deep embedding 表达能力更强，但单维通常不容易解释。我会把 CellProfiler 当 interpretable baseline，再看 microscopy-pretrained embedding 在 cross-batch task 上是否增加稳定的 biological information。

## 6. 什么是 shortcut learning？

模型利用与标签相关但不是目标 biology 的技术线索。最清楚的例子是 control 全由 microscope A 拍，treatment 全由 microscope B 拍；模型可能只识别 background/noise。解决需要 randomized design、group-aware split、cross-batch/instrument validation 和 negative control。

## 7. 哪些 morphology 可以数字化？

Shape：area、perimeter、circularity、eccentricity、solidity；intensity：mean/integrated intensity；texture：contrast、entropy 等；spatial：radial distribution、colocalization、spot count。进一步可以形成 cell-level → well-level → perturbation-level profile。

## 8. 为什么 segmentation 是关键？

因为 downstream measurement 都依赖 object boundary。merge/split/miss 会改变 cell number、area、intensity、subpopulation。即使 Dice 很高，若困难亚群被系统漏掉，科学结论仍会偏。

## 9. Dice vs IoU？

Dice=`2 intersection/(A+B)`，IoU=`intersection/union`。两者都是 overlap metric，Dice 数值通常更高一些，但科学上更重要的是 object-level merge/split 和 downstream feature stability。

## 10. 为什么 restoration 不能只看 PSNR/SSIM？

PSNR/SSIM 主要衡量 pixel similarity。科学图像还要看 spot count、localization、event time、peak、duration、trajectory、candidate ranking 是否改变。更漂亮但改变 biological event statistics 的 restoration 应判为失败。

## 11. 什么是 dynamic phenotype？

不是只描述 cell 最后长什么样，而是描述 response trajectory：什么时候开始、幅度多大、持续多久、是否恢复、不同 cell 是否分化成不同轨迹。它把 phenotype 从 endpoint 扩展成 time-dependent state。

## 12. 为什么 dynamic phenotype 比 static Cell Painting 更有价值？

不是所有任务都更有价值，但对 signaling、damage repair、cell fate 等过程，endpoint 会丢失路径。两个 candidate 最后 morphology 相同，latency/duration/recovery 可能完全不同。动态信息因此能增加 mechanism discrimination 和 functional evaluation。

## 13. Live-cell tracking 核心问题？

不仅是把 frame 连起来，还包括 segmentation uncertainty、identity switch、division、occlusion、drift、blinking、defocus。对 DNA spot 还要考虑 localization precision。错误轨迹可能看起来非常平滑，所以必须有 trajectory-level QC。

## 14. 什么是 MSD？

Mean squared displacement 衡量不同时间间隔下位移平方的平均，可用于描述 diffusion/motion pattern。但 localization noise 和 motion blur 会影响短时 MSD；MSD curve 也不能单独证明唯一运动机制。

## 15. ERK pulse amplitude/duration/latency？

Amplitude 是 activation 相对 baseline 的高度；duration 是持续时间；latency 是 stimulus 到 response onset 的延迟。它们能区分 endpoint 相似但 signaling dynamics 不同的 perturbation。

## 16. Fraction of responding cells 为什么重要？

因为 population mean 会隐藏 heterogeneity。相同平均响应可能来自所有 cells 轻度响应，也可能来自少数 cells 强烈响应。responding fraction 能揭示这种群体结构。

## 17. Recovery time？

信号或 phenotype 从 perturbation-induced state 回到 baseline 附近所需时间。它可以反映 adaptation、reversibility 或 persistent damage。

## 18. Off-target morphology？

候选达到目标 readout 的同时出现非预期 morphology，例如 cell rounding、nuclear shrinkage、mitochondrial fragmentation、vacuolization、detachment。这可能提示 stress、toxicity 或 off-target pathway。

## 19. 为什么 DNA damage/chromatin 适合 dynamic imaging？

因为过程本身依赖时间。53BP1 focus formation、fusion、persistence、disappearance 代表不同 dynamics；enhancer-promoter proximity 也要考虑 contact duration 与 transcription timing。静态 snapshot 很难恢复这些顺序。

## 20. 什么是 Dynamic Cell Embedding？

先把每帧编码成 z_t，再用 temporal Transformer/state-space model 建模 z_1...z_T，得到 trajectory representation。目标是预测 future state / fate，而不是把视频简单平均成一个 static vector。

## 21. Virtual Cell 与 transcriptome prediction 区别？

Transcriptome prediction 是 Virtual Cell 的一个 readout。理想 Virtual Cell 要描述 perturbation 后多层 cellular state 随时间如何变化，包括 RNA、protein、localization、morphology、function 和 fate。目前多数工作只是 partial virtual cell。

## 22. 为什么 transcriptome 常作为 target？

因为数据规模大、标准化成熟、perturbation label 易获得，尤其 Perturb-seq。但它不能唯一表示 protein activity、localization、signaling dynamics 和 morphology。

## 23. 理想 Virtual Cell 对新蛋白预测什么？

理想链是 sequence → structure → interaction/target → localization → signaling → transcriptome/proteome → morphology → dynamics → fate/toxicity。现实中我会拆成可验证中间任务，而不会声称当前模型能完整预测整条链。

## 24. 对新药应预测什么？

Target engagement、pathway response、efficacy、selectivity、toxicity、adaptation/resistance，以及不同 cell context 下的 response distribution。Transcriptome 是其中一个 measurement layer。

## 25. Virtual Cell 能直接预测 in-vivo efficacy 吗？

不能直接等价。Cell model 缺少 PK/PD、tissue distribution、barrier、immune system、microenvironment 等层级。它更适合作为 candidate screening 和 mechanistic hypothesis 的一层。

## 26. 哪些模型可作为 prototype？

可以看 CPA/STATE 类 perturbation-response model、PIE 的 perturbation representation、PerturbNet 的 perturbation-to-cell-state distribution、MultiVCDiff 的 multimodal response、MorphGen 的 morphology generation。它们覆盖不同子问题，不是同一个 full Virtual Cell。

## 27. 为什么 PIE 对 new protein → cell response 有启发？

核心不是名字，而是 perturbation representation 与 unseen perturbation generalization。可以把 protein sequence/structure representation 作为 perturbation embedding，研究未见 protein 的 response prediction。

## 28. 为什么 PerturbNet 有启发？

因为它把 perturbation embedding 与 cell-state distribution 联系起来。概念上可以把简单 perturbation ID 替换为 protein representation，再预测 downstream cellular distribution。

## 29. MultiVCDiff / MorphGen 意义？

它们说明 Virtual Cell 不一定只输出 transcriptome，还可以把 perturbation、molecular state 和 morphology/image distribution 连接。但 generated morphology 必须和 prospective experiment 分开，不能当真值。

## 30. Virtual Cell 与 live-cell imaging 竞争吗？

不竞争。Virtual Cell 是 prediction layer，live-cell imaging 是 measurement/validation layer。最有价值的是让 prediction 被真实 trajectory 验证，并把 error 反馈给模型。

## 31. 为什么 binding affinity alone 不够？

高 affinity candidate 仍可能 expression 差、localization 错、aggregation、target inaccessible、signaling 不对、off-target 或 toxicity。因此 structure/affinity 不是 cellular function 的充分条件。

## 32. Fluorescence imaging 如何帮助 protein design？

它可以直接测 localization、interaction proxy、signaling dynamics、organelle state、toxicity、cell fate。这样设计模型的评价就从 molecular score 延伸到 cell function。

## 33. Image-derived functional reward？

把 imaging-derived readout 转换成 candidate fitness，例如 localization score、ERK dynamics、mitochondrial phenotype、DNA damage、viability、phenotype rescue。它可以用于 ranking 或 active learning。

## 34. Phenotype-in-the-loop Protein Design？

Design → express/deliver → high-content/live-cell imaging → quantify phenotype → reward → redesign。它是把 cellular function 加入 Design-Build-Test-Learn loop。

## 35. 为什么 dynamic phenotype 对 design 更有价值？

因为 candidate 不只需要“最后有效”，还需要正确 onset、duration、recovery 和 heterogeneity。动态 readout 能区分相同 endpoint 下的不同 functional quality。

## 36. 哪些 protein 特别需要 dynamic microscopy？

会改变 signaling dynamics、localization、condensate/self-assembly、DNA repair、organelle function 或 cell fate 的设计最适合，因为它们的功能天然是 time-dependent。

## 37. 新 protein 可以直接放进 Virtual Cell 吗？

研究上可以把 sequence/structure embedding 作为输入，但不能假设任意 de novo protein 都在训练分布内。必须定义 expression/context，做 family holdout/unseen-protein test，并允许 uncertainty。

## 38. New protein vs new drug 哪个更容易？

通常小分子 perturbation 的历史数据和 standardized assay 更多，因此短期更容易；new protein 涉及 expression、folding、localization、interaction network 等额外变量。但这正是 protein-to-cell modeling 的研究价值。

## 39. PUREdrop-like 工作为什么值得关注？

因为它代表“computational design 后接动态 fluorescence functional assay”的范式。面试时重点讲范式，不对未核实的具体性能做过度陈述。

## 40. Imaging 用于 molecular design 需要哪些计算技能？

Image processing、segmentation/tracking、representation learning、time-series modeling、statistics、multimodal learning、uncertainty/OOD evaluation，以及把实验 metadata 和 model provenance 工程化管理。

## 41. JUMP 是什么？

Joint Undertaking for Morphological Profiling，是大规模 Cell Painting 标准化和数据共享生态，不是一个单独 AI model。

## 42. CPJUMP1 vs JUMP ORF？

CPJUMP1 更适合作为整理过的 matched chemical/genetic morphology benchmark；JUMP ORF 的核心 perturbation 是 ORF overexpression，因此更直接形成 protein/gene expression → morphology。

## 43. 为什么 JUMP ORF 能接 Protenix？

因为可以把 ORF identity 换成 protein sequence/structure representation，学习 `protein representation → Cell Painting phenotype`。Protenix 提供结构层信息，JUMP ORF 提供 cellular phenotype readout；关键评价是 unseen protein/family generalization。

## 44. 什么是 Cell Painting？

多种 fluorescent dyes 标记 nucleus、cytoplasm、mitochondria、ER、cytoskeleton 等结构，再提取高维 morphology profile，用统一 readout 比较大量 perturbation。

## 45. Morphology similarity 能证明 same mechanism 吗？

不能。不同 mechanism 可以收敛到相似 endpoint，同一 mechanism 在不同 time/context 下也可表现不同。Morphology similarity 更适合 candidate organization 和 hypothesis generation，需要 genetics、rescue、orthogonal assay、time series 等验证。

## 46. Pearson vs Spearman？

Pearson 衡量 linear correlation；Spearman 基于 rank 衡量 monotonic relationship，对非线性单调关系/异常值通常更稳健。二者都不证明 causality。

## 47. 为什么 many cells ≠ many biological replicates？

同一个 well 的 cells 共享培养和处理条件，不独立。真正 replicate 可能是 well、culture、batch、donor。把 cell 数直接当 n 会 pseudoreplication，夸大 significance。

## 48. p-value / effect size / FDR？

p-value 描述 null 下当前或更极端数据的概率；effect size 描述差异大小；confidence interval 描述估计不确定性；FDR 用于 multiple testing。统计显著不等于生物学重要。

## 49. RNA-seq pipeline？

FASTQ → QC → STAR/Salmon → gene×sample matrix → normalization/QC → DESeq2 等 count model → log2FC + adjusted p → pathway/enrichment。核心是 sample-level design、replicate 和 multiple testing。

## 50. DNA-seq pipeline？

FASTQ → QC → BWA-MEM2 alignment → BAM processing → variant calling → VCF filtering → VEP annotation，并结合 coverage、base/mapping quality、allele balance、VAF 判断可信度和功能后果。

---

## 总答题原则

所有开放题尽量回到一条主线：

`可靠 measurement → phenotype → dynamics → prediction → intervention/design`

并主动区分：

`prediction ≠ explanation ≠ causality`

最终连接：

`Protein/Molecule → Structure → Cellular State → Dynamic Phenotype → Experimental Feedback`
