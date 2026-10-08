# Seed STEM / Bio AI for Science 对话完整归档（主题重组版）

> 目的：尽可能完整保留本轮面试准备对话形成的知识、判断、例子、研究设想和问答，而不是只做摘要。
>
> 说明：本文件按主题重组，而非逐字聊天 transcript。已把现有对话、此前 Seed STEM 准备记录以及《荧光成像中的人工智能与高通量计算生物学》长综述中的相关讨论统一归档。公开项目事实与个人研究设想分开表达，避免把 proposal 写成已有成果。

# 1. 总体研究叙事

核心问题不是“AI 能不能把荧光图做得更漂亮”，而是：**能否把显微观测转化成可靠的细胞状态测量，再把这种测量用于预测、干预和分子设计反馈。**

统一链路：

`Protein / Molecule → Structure → Cellular State → Dynamic Phenotype → Experimental Feedback`

长期闭环：

`Design → Predict → Experiment → Measure → Learn → Redesign`

在 Seed 语境下，上游可以是 Protenix / protein design / molecular design；中间是 Virtual Cell 或 perturbation-response model；下游是真实 cellular phenotype。活细胞荧光成像最适合作为 Virtual Cell 与真实细胞之间的 functional validation layer。

个人差异化不是与结构模型团队竞争，而是补“结构/分子 → 真实细胞功能”之间缺失的一段。

# 2. 为什么个人实验背景能转成计算生物学优势

已有背景包括 CRISPR 活细胞 DNA 成像、增强子-启动子动态、DNA 双链断裂与 53BP1、RNA 荧光适配体/细胞 pH、线粒体 pH。这些体系共同特点是：信号不是普通 RGB 纹理，而是带有测量物理、传感器动力学、空间定位误差和时间结构的 biological readout。

因此实验经验能用于定义：

- 哪个信号是真正的 biological endpoint；
- 哪些变化可能来自 bleaching、focus drift、probe expression、PSF、background；
- 哪些模型输出可以作为 measurement，哪些只能作为 hypothesis；
- 什么 reference / orthogonal assay 才能验证模型；
- 如何把模型误差传播到最终科学结论。

例如：

- pH sensor 的 fluorescence intensity 不能未经校准直接等价成 pH；
- 53BP1 focus number/size 可以作为 DNA damage response readout，但不能单独等价为 repair efficiency 或 cell fate；
- 两个 CRISPR DNA spots 靠近是空间测量，不自动证明 enhancer-promoter functional contact。

因此 AI for Science 的关键是维持证据链：**measurement → statistical inference → mechanism hypothesis → experimental validation。**

# 3. High-content imaging 与高通量

High-content imaging 不等于“拍很多照片”。它更接近：

`标准化实验 → 多通道成像 → segmentation → per-cell feature extraction → QC → aggregation → statistics → phenotype`

高内涵强调每个样本有丰富 readout；高通量强调处理样本的规模。两者可以同时存在，但不是同义词。

真正高通量系统还必须保留 experiment / plate / well / field / cell / time / channel 层级，以及 acquisition setting、analysis version、model weight、parameter 和 QC provenance。

# 4. AI 在荧光成像中的三层能力

## 4.1 Measurement / information extraction

回答“在哪里、多少、怎么移动”：

- segmentation
- spot detection
- localization
- tracking
- intensity measurement

## 4.2 Phenotype / state interpretation

回答“这些结构和动态意味着什么”：

- cell cycle
- DNA damage state
- morphology phenotype
- perturbation classification
- protein localization
- cell-state representation

## 4.3 Restoration / inverse problem

回答“噪声、模糊、通道不足时还能恢复什么”：

- denoising
- deconvolution
- super-resolution
- inpainting
- semantic unmixing

三层不能混用同一个评价指标。图像变清楚不代表 mechanism prediction 更准确。

# 5. 为什么荧光图不能简单当普通 RGB 图像

荧光像素由真实 fluorophore distribution、optical PSF、photon statistics、detector noise、background、exposure、probe expression、probe maturation、binding dynamics、local environment 等共同决定。

同一 biological state 在不同 microscope / exposure / batch 下可以产生明显不同 pixel distribution；相反，不同 biological states 也可能得到相似形态。

所以必须防止模型学习 microscope、plate、date、cell density 等 shortcut。

# 6. Shortcut learning：面试最清楚的例子

假设 control 全部由显微镜 A 拍摄，treatment 全部由显微镜 B 拍摄。A/B 在 background brightness、noise pattern 或 illumination 上有差异。模型即使完全不看细胞，也可能把两组分类得很好。

这时 accuracy 很高，但模型学到的是 microscope identity，不是 drug response。

其他 shortcut：

- plate position；
- experiment date；
- batch；
- cell density；
- imaging setting；
- preprocessing difference。

控制：randomization、cross-batch validation、cross-instrument test、blind evaluation、group-aware split、negative controls。

# 7. CellProfiler、显式特征与 Deep Embedding

CellProfiler 适合作为 interpretable baseline。典型显式特征包括：

形态：area、perimeter、major/minor axis、circularity、eccentricity、solidity、convexity。

强度：mean、median、integrated intensity、coefficient of variation。

纹理：contrast、homogeneity、energy、entropy。

空间：radial distribution、colocalization、spot count。

Deep embedding 则是模型将图像映射成高维向量，例如 768-D vector。单个维度通常不像“面积”那样直接可解释，但整个向量可以用于 clustering、retrieval、classification、perturbation similarity 和 multimodal alignment。

合理实验不是直接假设 deep embedding 更强，而是：CellProfiler baseline → general vision embedding → microscopy-pretrained embedding → small supervised model，并按 batch/perturbation 严格划分，比较谁保留更多可复现 biology。

# 8. Embedding 到底是什么

可把 embedding 理解为模型学习的“细胞状态坐标”。输入一张细胞图像 x，encoder 输出 z=f(x)。z 不是自然语言标签，而是压缩后的高维表示。

相似 phenotype 往往在 latent space 中更接近，因此可做 nearest-neighbor、clustering、linear probing 等。

但 latent similarity 只表示模型认为两者相似，不自动证明两者共享 molecular mechanism。

# 9. Segmentation 为什么是基础

所有 per-cell measurement 都依赖 object boundary。典型错误：

- merge：两个细胞合成一个；
- split：一个细胞拆成多个；
- miss：漏检；
- boundary bias：边界系统偏移。

例如 dividing nuclei 被 merge 会改变 cell-cycle statistics；死亡细胞更难分割，如果被系统性排除，会低估 drug toxicity。

常用指标：

`Dice = 2|A∩B|/(|A|+|B|)`

`IoU = |A∩B|/|A∪B|`

但高 Dice/IoU 不足以证明科学可靠。还要检查 segmentation error 是否改变 area、intensity、spot count、subpopulation frequency 和 downstream decision。

可用 Cellpose、StarDist、microSAM、U-Net 等作为工具/基线。

# 10. 细胞形态提取背后的数学与图像计算

图像级处理：convolution、Gaussian filtering、background subtraction、flat-field correction、thresholding、morphological operation。

传统 segmentation：threshold + connected components + watershed。

几何：area、perimeter、aspect ratio、eccentricity；circularity 常写为 `4πA/P²`。

统计：distribution、effect size、confidence interval、hypothesis testing、FDR。

高维：PCA、UMAP、clustering、distance/similarity metric。

AI：CNN、Vision Transformer、self-supervised learning、masked autoencoder。

动态：tracking、time-series analysis、state-transition model、temporal Transformer、state-space model。

关键不是“把算法串起来”，而是确保每层误差不会无审计地传播到最终 biological conclusion。

# 11. Tracking：细胞与分子斑点不是同一个问题

Ultrack、Trackastra 更偏 cell-object tracking；TrackMate、trackpy 更适合作为 point/particle tracking 起点。

CRISPR DNA locus tracking 要考虑：localization error、stage drift、spot blinking、defocus、mis-association。看似连续轨迹可能来自错误连接。

运动分析还需考虑 motion blur 与 localization noise。可计算 MSD（mean squared displacement）等，但 MSD pattern 本身也不能无条件映射到唯一物理机制；constrained diffusion、anomalous diffusion、active motion 等需要结合实验条件。

# 12. 图像恢复：denoising、deconvolution、super-resolution、unmixing

简化观测模型可写成真实 fluorescence distribution 经过 optical system convolution，再加 photon/detector noise 和 background。

逆问题通常非唯一，因此 neural network 实际使用 learned prior 选择一个 plausible solution。prior 可以恢复弱结构，也可能把罕见结构“纠正”成训练集中常见形态。

代表方向：CARE、Noise2Void、CAREamics、DeepInterpolation、DeepCAD-RT、DeepSeMi、SUPPORT、ZS-DeconvNet、DL-SR/BioSR、MicroSplit。

## 为什么不能只看 PSNR / SSIM

科学图像评价必须进入 downstream readout：

- spot count 是否改变；
- localization / distance 是否偏移；
- event onset / peak time 是否改变；
- amplitude 是否压缩；
- duration 是否被平滑；
- trajectory / MSD 是否改变；
- treatment ranking 是否改变。

如果图像更漂亮但改变事件统计，应判为失败。

尤其时序去噪可能利用 future frames；这种离线 restoration 不能冒充 real-time prediction。

# 13. 普通显微镜 + AI 能否变成 SIM

必须区分两件事：

1. SIM 利用多角度/多相位结构光采集带来的额外物理信息进行重建；
2. 单张/普通采集图像的 neural super-resolution 更多依赖训练分布 prior。

网络生成更细 filament 或把一个 spot 分成两个，不代表样本中这些细节被真实测到。真正科研使用必须对 OOD、低信号、异常结构做独立验证。

所以目标应是“在明确任务上提高可测信息/降低光剂量”，而不是宣称普通宽场被无条件变成 SIM。

# 14. Dynamic Phenotype：为什么是核心方向

静态 endpoint 回答“最后长什么样”；动态 phenotype 回答：

- 什么时候开始响应；
- 响应多强；
- 持续多久；
- 能否恢复；
- 多少细胞响应；
- 细胞之间是否分化成不同轨迹；
- 下一状态是什么。

两个 perturbation 最终产生同样 endpoint，过程可能完全不同；相反，同一 pathway 不同时间阶段也可能看起来不同。

因此动态信息能补静态 Cell Painting 的缺口。

# 15. 动态表型关键指标

ERK pulse amplitude：activation 相对 baseline 的幅度。

ERK pulse duration：activation 持续时间。

Response latency：stimulus 到 response onset 的时间。

Fraction of responding cells：发生响应的细胞比例。平均值相同的两个群体，可能一个是全部细胞弱响应，另一个是少数细胞强响应。

Recovery time：信号返回 baseline 附近所需时间，反映 response reversibility/adaptation。

Off-target morphology：非预期的细胞形态改变，例如 rounding、nuclear shrinkage、mitochondrial fragmentation、vacuolization、detachment，可提示 stress、toxicity 或非靶向效应。

# 16. Dynamic Cell Embedding

静态模型：

`frame_t → encoder → z_t`

动态扩展：

`frame_1...frame_T → encoder → z_1...z_T → temporal Transformer / state-space model → Z_trajectory`

Z_trajectory 应尽量表示 trajectory-level state，而不是单帧 appearance。

可预测：

- DNA locus movement；
- 53BP1 formation/disappearance；
- pH trajectory；
- drug response；
- future cell state；
- fate probability。

这可以形成 live-cell world-model / dynamic cell representation 的研究原型，但目前是研究设想，不应表述成已经成熟的通用模型。

# 17. 动态表型干预与闭环

进一步不是只识别 phenotype，而是：

`observe z(t) → predict future → choose intervention → perturb → re-image → update`

这就是 dynamic phenotype intervention / adaptive experiment。

例如模型预测某个细胞即将进入 DNA damage persistent state，可以提高采样频率、增加另一个 reporter 或选择干预；但真实闭环需要考虑 microscope interface、latency、photon budget、phototoxicity 和 missed-event cost。

# 18. Virtual Cell：应该怎样定义

理想 Virtual Cell：

`initial cellular state + perturbation + context + time → future cell-state distribution`

它不应被缩窄成“预测转录组”，也不应把所有静态 image generation 都叫 full virtual cell。

当前多数模型只覆盖完整细胞系统的一部分，例如 perturbation → transcriptome，或 transcriptome → morphology，或 perturbation → image distribution。

# 19. 为什么 transcriptome 常成为 Virtual Cell target

因为 scRNA-seq / perturb-seq 数据规模大、标准化相对成熟、扰动标签容易配对，适合学习 cell state response。

但 transcriptome 不是完整 cellular function。蛋白 localization、post-translational regulation、signaling dynamics、organelle state、morphology 和 fate 可能无法从 endpoint transcriptome 唯一确定。

# 20. 新蛋白进入 Virtual Cell：理想链与现实边界

理想链：

`sequence → structure → interaction/target → expression/localization → signaling → transcriptome/proteome → morphology → dynamics → fate/toxicity`

现实中不存在能对任意 de novo protein 稳定完成整条链的通用模型。

主要困难是跨尺度误差累积、数据稀缺和 OOD generalization。

因此更现实的研究是把 protein sequence/structure embedding 作为 perturbation representation，先预测一个可验证 readout，例如 transcriptome、Cell Painting profile 或动态 reporter。

# 21. 新药 Virtual Cell 应预测什么

高价值输出包括：

- target engagement；
- pathway response；
- efficacy；
- selectivity；
- toxicity；
- resistance / adaptation。

Transcriptome 是 readout 之一，不是最终目标。

Virtual Cell 不能直接等价于 in-vivo efficacy prediction，因为后者还受到 PK/PD、distribution、tissue barrier、immune system、microenvironment 等影响。

# 22. Virtual Cell 模型原型

讨论过的参考路线包括 STATE、CPA、PIE、PerturbNet、MultiVCDiff、MorphGen 等。

PIE 的启发：学习 perturbation representation，并研究 unseen perturbation generalization；适合考虑把 gene/perturbation identity 换成 protein representation。

PerturbNet 的启发：perturbation embedding → cell-state distribution；可把 protein sequence/structure embedding 接入。

MultiVCDiff 的启发：连接 perturbation、transcriptome 与 Cell Painting morphology。

MorphGen 的启发：条件 cellular morphology/image generation；但 generation 不是 experimental fact。

这些项目是 prototype/组件，不是已经解决 full Virtual Cell。

# 23. Virtual Cell 与 live-cell imaging 的关系

不是竞争关系。

`Virtual Cell = prediction layer`

`Live-cell imaging = measurement + validation layer`

模型预测细胞会怎么响应，真实成像检验 trajectory 是否发生；误差再反馈给模型。

这正是实验背景进入 computational biology / protein design 的接口。

# 24. JUMP / Cell Painting

JUMP = Joint Undertaking for Morphological Profiling，是大规模标准化 Cell Painting 的协作生态，不是一个算法。

Cell Painting 通过多种染色读出 nucleus、cytoplasm、mitochondria、ER、cytoskeleton 等结构，再将图像转换为 high-dimensional morphology profile。

JUMP 相关数据可包含 compound、CRISPR、ORF perturbation。

CPJUMP1 可理解为较小、整理过的 matched chemical/genetic benchmark 数据，适合方法学比较。

JUMP ORF：ORF overexpression → Cell Painting phenotype。

JUMP Compound：chemical perturbation → phenotype。

JUMP CRISPR：gene knockout → phenotype。

# 25. 为什么 JUMP ORF 与 Protenix / protein design 特别有连接

JUMP ORF 天然给出：

`protein/gene overexpression → cell morphology`

可进一步研究：

`protein sequence embedding + structure embedding → morphology profile`

例如 sequence 用 ESM-like embedding，structure 用 Protenix/structure-derived representation，再预测 Cell Painting profile。

评价不能只 random split。更关键的是 protein-family holdout / unseen-protein split，检验模型是否真正 generalize，而不是记住 gene identity。

# 26. 蛋白设计为什么不能只看 binding affinity

高 affinity 不代表细胞中有效。还可能出现：

- expression failure；
- mislocalization；
- aggregation；
- target inaccessible；
- wrong signaling dynamics；
- off-target effect；
- toxicity。

因此 molecular structure / affinity 是上游必要条件，但不是 cellular function 的充分条件。

# 27. Image-derived Functional Reward

可把 imaging readout 转换为 design reward / fitness：

- localization score；
- ERK pulse pattern；
- viability；
- mitochondrial morphology；
- DNA damage response；
- condensate/self-assembly behavior；
- phenotype rescue；
- dynamic response score。

这样 protein generator 不只是优化 structure/affinity，还可以在 active learning 中逐步优化真实 cell function。

# 28. Phenotype-in-the-loop Protein Design

概念闭环：

`Protein generator → candidate → expression/delivery → live-cell/high-content imaging → phenotype quantification → reward → redesign`

长期就是 Design-Build-Test-Learn。

动态表型的优势是同一 endpoint 下还能比较 latency、amplitude、duration、recovery 和 heterogeneity。

# 29. PUREdrop-like 工作为什么值得关注

讨论中的价值不在于某一个具体系统，而在于展示一种思路：computational protein design 之后，用 synthetic-cell / droplet / fluorescence time-lapse 等实验体系测 functional dynamics，而不是只看 structure score。

在面试中应把它作为“设计与动态功能 readout 连接”的例子，不要把未核实的具体性能或系统细节讲成确定事实。

# 30. 前沿机构：谁在 AI + microscopy / cell phenotype 上投入

## Meta：Cell-DINO / Channel Adaptive DINO

重点是 fluorescence microscopy self-supervised representation 和不同 channel number/configuration 的适配。适合研究多通道输入、自监督目标、cross-task/cross-batch representation。

边界：static representation 不等于 dynamics 或 mechanism。

## Microsoft：GigaTIME / GigaTIME-Flash

H&E pathology → virtual multiplex immunofluorescence / spatial protein signal。代表 image → biological signal prediction。

边界：predicted protein channel ≠ measured protein channel；而且主要是 fixed tissue/pathology，不是 live-cell dynamics。

## NVIDIA：VISTA-2D

cell instance segmentation / morphology analysis，属于 measurement foundation layer。

边界：segmentation 不等于 pathway understanding。

## Google Research + ISTA：LICONN

expansion microscopy + fluorescence labeling + registration + ML/FFN reconstruction，目标是 neural/synaptic connectivity reconstruction。

重要启发：measurement system 和 AI co-design，而不是假设软件能凭空补齐没有观测的信息。

## Recursion：Phenom / OpenPhenom / MAE microscopy

大规模 perturbation imaging → representation → candidate relationship / screening。最接近 phenotype-driven drug discovery 的工业范式。

边界：公开 OpenPhenom 不等于 Recursion 整个内部研发系统。

## CZI / Biohub：MorphGen / SubCell / Virtual Cells Platform / Virtual Biology Initiative

覆盖 cell image generation、protein localization representation、model distribution 和多模态 virtual-cell ecosystem。

边界：生成图像不是实验事实；Virtual Biology Initiative 是进行中的计划，不等于 full virtual cell 已完成。

## Anthropic / OpenAI

对话中没有找到与上述项目同等明确的、专门面向 fluorescence microscopy 的公开主项目。Anthropic 的 Claude Science 更偏科研工具/analysis workflow。不能因为公司做 biology AI 就推断其有专门显微成像模型。

# 31. 为什么通用 AI 大厂不一定大量做 fluorescence-specific model

原因包括：

- 高质量 microscopy data 强依赖实验系统；
- measurement protocol、instrument、label、cell type 差异大；
- ground truth 难；
- wet-lab feedback loop 成本高；
- 通用 AI lab 更擅长 general foundation model / agent；
- 专业 biotech / imaging lab 更接近真实数据和验证闭环。

因此这个领域的壁垒不是单纯模型参数，而是 experiment-model co-design 和 trustworthy measurement。

# 32. 可直接研究/扒代码的开源项目

基础测量与 profiling：CellProfiler、CytoTable、pycytominer、DeepProfiler。

分割：Cellpose、StarDist、microSAM。

追踪：Ultrack、Trackastra、TrackMate、trackpy。

RNA/spot：Big-FISH、DECODE。

动态 phenotype：SPOT。

恢复：CSBDeep/CARE、Noise2Void、CAREamics、DeepInterpolation、DeepCAD-RT、DeepSeMi、SUPPORT、ZS-DeconvNet、DL-SR/BioSR、MicroSplit。

高通量筛选：Brieflow / brieflow-analysis、Fractal/OME-NGFF。

表征/生成：Cell-DINO、Recursion maes_microscopy/OpenPhenom、SubCell、MorphoDiff、MorphGen。

其他：Google FFN、NVIDIA VISTA-2D。

个人阅读/复现优先级曾收敛为：

1. SubCellPortable + subcell-analysis；
2. Cell-DINO；
3. OpenPhenom；
4. MorphGen；
5. 在 static encoder 后加入 temporal model，探索 Dynamic Cell Embedding。

# 33. Seed 相关公开项目与叙事连接

讨论过 Seed 的 Protenix / PXDesignBench，以及更广泛的 AI4Science / agent / benchmark 工作。

Protenix：多分子结构预测方向。面试连接点不是说 Protenix 已经做 cell imaging，而是问：结构预测/设计之后如何进入 cell-function validation。

PXDesignBench：蛋白设计评价，涉及 self-consistency、confidence、geometry、diversity、novelty、experimental-oracle calibration 等思路。连接点是：结构层 benchmark 之后，能否增加 cellular phenotype layer。

Seed for Seed：作为 auto-research / AI-for-science agent 方向的讨论背景。

CryoFM：生成式 3D cryo-EM density prior，用于 denoising、inpainting、anisotropy correction、style enhancement 等 inverse problems。对 fluorescence 的启发是 learned prior 必须受 experimental likelihood / measurement constraint 约束，不能把 hallucination 当 measurement。

EdgeBench / Agent-World 类工作：强调 agent 在环境反馈中持续学习、任务不能过早达到 ceiling、trajectory 评价和 verifier。可迁移到 scientific agent / experimental agent。

# 34. 个人可以向 Seed 提出的研究切入

## 方向 A：Dynamic Cell Benchmark

建立对 live-cell model 的科学评价：是否保留真实 event timing、motion、response dynamics，而不是只评 image quality。

## 方向 B：Protein-to-Phenotype

Protein sequence/structure embedding → morphology / reporter / dynamic phenotype。

先从 JUMP ORF 等公开数据验证 static phenotype，再逐步加入 time-lapse data。

## 方向 C：Phenotype-in-the-loop design

把 imaging-derived functional reward 接到 protein design / candidate ranking。

## 方向 D：Virtual Cell validation layer

Virtual Cell 输出未来 cellular state；live-cell imaging 提供 prospective experimental verification。

## 方向 E：Adaptive acquisition / experiment agent

模型根据 uncertainty / predicted event 决定何时提高 frame rate、曝光或增加 readout，优化 photon budget 与 biological information。

# 35. 如何判断 AI 在一个学科中的应用价值

五层框架：

1. **Scientific problem value**：解决的是不是领域真正瓶颈？
2. **AI incremental value**：相比传统算法/统计是否提供新增价值？
3. **Generalization boundary**：在哪个 distribution shift 下仍有效？
4. **Prediction vs explanation vs causality**：模型到底证明了什么？
5. **Experimental loop**：模型是否能影响下一步实验并被真实结果验证？

能力成熟度可分：

Level 1 Measurement：segmentation、denoising、tracking。

Level 2 Phenotype：cell-state recognition / representation。

Level 3 Prediction：perturbation → future phenotype。

Level 4 Design / Intervention：模型选择 candidate、实验或 intervention。

# 36. Generalization ladder

评价模型不要只 random split，应逐层问：

`same lab → cross batch → cross microscope → cross cell line → cross species → unseen perturbation → unseen protein`

前几层主要测试 robustness；后几层逐渐进入 extrapolation。

真正 AI for Science 的高价值常常不是 IID accuracy，而是能否在明确边界内处理 distribution shift，并知道何时不确定。

# 37. Prediction、Explanation、Causality

Prediction：给定 x 能否预测 y。

Explanation：哪些输入因素与 prediction 有关，或模型能否提出机制假说。

Causality：改变某因素是否导致 outcome 改变，需要 intervention / counterfactual logic / experimental validation。

模型预测 phenotype 很准，不代表它理解 mechanism；feature attribution 也不自动等于 causality。

# 38. AI fluorescence 的三层能力边界

物理边界：观测中没有的信息无法无条件恢复。未采样的快速事件、无法分开的重叠来源、严重损伤的数据只能依靠 prior 估计。

统计边界：microscope、cell type、label、drug、batch 改变会造成 distribution shift。

生物学边界：morphology 与 mechanism 多对一，molecular state 与 fate 也不唯一。

因此可靠系统应允许 uncertainty / abstention，而不是所有输入都给高置信结论。

# 39. 统计基础：Pearson vs Spearman

Pearson：衡量 linear relationship。

Spearman：先转换为 rank，再衡量 monotonic relationship；对非线性单调关系和异常值通常更稳健。

二者都是 association，不等于 causation。

# 40. Pseudoreplication

同一 well 中 5000 个 cells 不是 5000 个 independent biological replicates。

独立单位可能是 well、culture、batch、donor。

否则 cell-level n 极大，会把极小 technical difference 变成极显著 p-value。

可采用 pseudobulk、hierarchical/bootstrap、mixed-effects model、batch-level resampling 等。

# 41. p-value、effect size、CI、FDR

p-value：在 null hypothesis 成立时，观察到当前或更极端数据的概率；不是“null hypothesis 为真的概率”。

Effect size：差异有多大。

Confidence interval：effect estimate 的不确定范围。

FDR：大量 hypothesis testing 时控制 expected false discovery proportion；常用 Benjamini-Hochberg。

面试中应强调 statistical significance ≠ biological significance。

# 42. RNA-seq pipeline

`FASTQ → FastQC/MultiQC → STAR alignment 或 Salmon quantification → gene × sample matrix → QC/normalization → DESeq2 negative-binomial modeling → log2FC + adjusted p-value → GO/KEGG/Reactome/GSEA`

重点不是背软件，而是知道 sample-level replicate、normalization、multiple testing 和 pathway-level interpretation。

# 43. DNA-seq pipeline

`FASTQ → QC → BWA-MEM2 → BAM sort / duplicate handling → variant calling → VCF → filtering → VEP annotation`

关注 coverage、base quality、mapping quality、allele balance、VAF。最终目标是 credible variant + functional consequence，而不是只输出 variant list。

# 44. Benchmark / Agent 经验如何与 Seed STEM 连接

近期 benchmark/harness 工作包括 L1000、Perturb-seq、Harbor Science Bench Factory、GroundSignal 等。

核心能力：

- oracle / truth independence；
- endpoint shortcut detection；
- hidden-state recovery；
- negative control；
- process-aware scoring；
- verifier/reference separation；
- difficulty calibration；
- failure attribution；
- real-data / literature grounding；
- scientific task generation and audit。

迁移到 Virtual Cell 的问题就是：模型到底在哪种 cell type、perturbation、batch、OOD condition 下失效？有没有 shortcut？有没有真正 generalize？

# 45. L1000 / Perturb-seq 可以怎样讲

L1000 benchmark 的核心不是追求一个 endpoint score，而是研究 MoA / hidden perturbation state recovery、避免 endpoint shortcut、做过程评分和 calibration。此前实验暴露过 amplitude/potency shortcut、PI3K↔mTOR confusion 等问题，这类经验可以转化为对 Virtual Cell representation 的审计思维。

Perturb-seq 双扰动任务关注 perturbation validity、batch confounding、differential expression 和 non-additivity。交互 estimand 可写作：

`Δ_int=(AB−C)−(A−C)−(B−C)`

这体现了用户不仅做视觉任务，也熟悉 perturbation biology 与统计定义。

# 46. Scientific Agent / Auto Research

未来 AI for Science 不只是 foundation model，还会有 agent 决定：查什么文献、运行什么分析、选择什么实验、如何根据 feedback 修改假说。

对成像领域，可以构造：

`agent → inspect QC → choose analysis → detect uncertain event → request additional acquisition / assay → update hypothesis`

但 agent 的语言解释不能替代 verifier 和 experimental evidence。

# 47. 面试时最重要的统一表达

可以用：

“我比较关注的不是单独把显微图像做得更漂亮，而是把成像变成可靠的细胞状态测量。进一步把静态表型扩展成动态表型，再把这个 functional readout 接到 Virtual Cell 和蛋白/分子设计之后。这样上游模型负责提出候选和预测，真实细胞成像负责验证功能并提供反馈，最终形成 Design–Predict–Experiment–Measure–Learn–Redesign 的闭环。”

# 48. 面试中必须主动承认的边界

- Virtual Cell 目前不是完整 cell digital twin；
- arbitrary de novo protein → full cellular dynamics 尚未解决；
- morphology similarity ≠ same MoA；
- generated image ≠ measurement；
- PSNR/SSIM ≠ biological fidelity；
- correlation/prediction ≠ causality；
- in-vitro cellular response ≠ in-vivo efficacy；
- embedding 必须排除 batch/instrument shortcut；
- many cells ≠ many biological replicates；
- static representation 不自动包含 dynamics；
- 使用 future frames 的 restoration 不等于 real-time prediction。

这些不是弱点，而是定义可验证 research question 的基础。

# 49. 50 道模拟面试题索引

## A. AI + fluorescence imaging

1. 什么是 high-content imaging？与普通 fluorescence imaging 有什么区别？
2. AI 在 fluorescence imaging 中的三类核心作用是什么？
3. 为什么 fluorescence images 不能简单当 RGB images？
4. 什么是 embedding？它在 cell imaging 中有什么作用？
5. CellProfiler features 与 deep embeddings 有什么区别？
6. 什么是 shortcut learning？
7. 哪些 cell morphology features 可以数字化？
8. 为什么 segmentation 是关键步骤？
9. Dice 与 IoU 有什么区别？
10. 为什么 image restoration 不能只看 PSNR/SSIM？

## B. Dynamic phenotype

11. 什么是 dynamic phenotype？
12. 为什么 dynamic phenotype 可能比 static Cell Painting 更有价值？
13. Live-cell tracking 的核心计算问题是什么？
14. 什么是 MSD，为什么用于 molecular/cellular motion？
15. ERK pulse amplitude/duration/latency 分别是什么？
16. Fraction of responding cells 为什么重要？
17. Recovery time 反映什么？
18. Off-target morphology 是什么？
19. 为什么 DNA damage / chromatin 特别适合 dynamic imaging？
20. 什么是 Dynamic Cell Embedding？

## C. Virtual Cell

21. Virtual Cell 与普通 transcriptome prediction 有什么区别？
22. 为什么 transcriptome 经常成为 Virtual Cell target？
23. 对 new protein，理想 Virtual Cell 应预测什么？
24. 对 new drug，理想 Virtual Cell 应预测什么？
25. Virtual Cell 能直接预测 in-vivo efficacy 吗？
26. 哪些模型可以作为 Virtual Cell prototype？
27. 为什么 PIE 适合研究 new protein → cell response？
28. 为什么 PerturbNet 适合 Protein-to-Cell？
29. MultiVCDiff / MorphGen 的意义是什么？
30. Virtual Cell 与 live-cell imaging 是竞争关系吗？

## D. Molecular / protein design

31. 为什么 binding affinity alone 不够？
32. Fluorescence imaging 如何直接帮助 protein design？
33. 什么是 image-derived functional reward？
34. 什么是 Phenotype-in-the-loop Protein Design？
35. 为什么 dynamic phenotype 对 design 更有价值？
36. 哪些 proteins 最需要 dynamic microscopy？
37. New protein 可以直接放进 Virtual Cell 吗？
38. New protein vs new drug，哪一个更容易做 Virtual Cell prediction？
39. 为什么 PUREdrop-like 工作值得关注？
40. 把 imaging 用于 molecular design，需要哪些 computational skills？

## E. JUMP / Cell Painting

41. JUMP 是什么？
42. CPJUMP1 与 JUMP ORF 有什么区别？
43. 为什么 JUMP ORF 能与 Protenix 接起来？
44. 什么是 Cell Painting？
45. Morphology similarity 能证明 same mechanism 吗？

## F. Statistics / bioinformatics

46. Pearson 与 Spearman 的区别？
47. 为什么 many cells ≠ many biological replicates？
48. p-value、effect size、FDR 分别回答什么？
49. RNA-seq pipeline？
50. DNA-seq pipeline？

# 50. 已经逐题展开过的前 10 题核心答法

Q1 High-content imaging：不是拍很多图，而是标准化实验、多通道成像、自动分割、feature extraction 和 statistics，把 cell 转成 high-dimensional measurable phenotype。

Q2 AI 三类作用：measurement（segmentation/tracking/spot）、state interpretation（cycle/damage/perturbation）、restoration（denoising/deconvolution/SR/unmixing）。

Q3 fluorescence ≠ RGB：pixel intensity 受 exposure、probe、bleaching、PSF、noise 等影响；必须把 imaging physics 与 biology 分开。

Q4 embedding：image → high-dimensional vector，用于 similarity/clustering/retrieval/classification；必须检验 biology vs batch。

Q5 CellProfiler vs embedding：前者 explicit/interpretable，后者 learned/expressive；前者适合作 baseline 和解释，后者需证明增量价值。

Q6 shortcut：control=A microscope、treatment=B microscope，模型可能识别 instrument 而非 biology。

Q7 morphology：shape/intensity/texture/spatial features，并进一步聚合到 cell/well/perturbation level。

Q8 segmentation：boundary error 会传播到所有 downstream measurement；总体 overlap 好不代表困难亚群可靠。

Q9 Dice/IoU：都是 overlap metric，Dice 对 overlap 的表达形式为 2 intersection / total size，IoU 为 intersection / union；科学评价还需 downstream stability。

Q10 PSNR/SSIM：只能描述部分 pixel similarity；scientific restoration 要验证 spot、distance、event time、trajectory、biological conclusion。

# 51. 动态表型问题的现场回答逻辑

如果问“为什么动态比静态重要”：

先说 endpoint 会压缩过程信息；再举 53BP1：同样 endpoint focus number，可能一个持续形成、一个快速 repair；再连接 protein/drug design：candidate 的 latency/duration/recovery 可能决定真实功能与副作用。

如果问“Dynamic Cell Embedding”：

先定义 frame embedding z_t，再说明 temporal model 聚合成 trajectory embedding；最后说目标是 future-state prediction，而不是只把视频平均成一个 vector。

# 52. Virtual Cell 问题的现场回答逻辑

先避免说“Virtual Cell 已经能模拟整个细胞”。更准确：目前是多个 partial models。

新 protein 问题可回答：最理想当然是 sequence 到 fate，但现实上我会把任务拆成可验证中间层，先做 sequence/structure → transcriptome/morphology/dynamic reporter，再逐步扩大。

问“为什么需要 imaging”：因为 transcriptome 是 endpoint molecular readout，而 live imaging 提供 localization、dynamics、heterogeneity 和 trajectory，可作为独立验证层。

# 53. Protein Design 问题的现场回答逻辑

如果问“你是做 imaging 的，为什么来做 protein design？”：

回答重点不是说自己要重新做一个 protein generator，而是指出设计 pipeline 的瓶颈之一是 functional validation。Structure score / affinity 不能保证 cellular behavior。自己的优势是定义细胞层 readout 和动态 phenotype，并把它变成 design feedback。

# 54. AI 应用价值问题的现场回答逻辑

若面试官问“如何判断 AI 在这个领域有没有价值？”：

可以回答：我会先问科学 bottleneck，再问 AI 相对传统方法的 incremental value，然后做 generalization ladder，明确 prediction/explanation/causality，最后看它是否能进入实验闭环。对 fluorescence 来说，成熟能力是 measurement 和 profiling；更前沿的是 future-state prediction 和 adaptive intervention。

# 55. 为什么这个方向适合 Seed STEM

Seed 的优势在大模型、scientific model、protein/structure、agent 和 scalable computation。个人优势在 biological measurement、dynamic imaging、perturbation benchmark 和 scientific evaluation。

交集不是“我也做一个结构模型”，而是：

- 把 structure/design 输出连接到 cell-state prediction；
- 用 imaging 构建 functional oracle；
- 用 benchmark 定义 generalization boundary；
- 最终让 scientific agent 能选择下一 candidate / experiment。

# 56. 最终研究图

```text
Protein / molecule generator
          ↓
Sequence / structure representation
          ↓
Target / interaction / perturbation representation
          ↓
Virtual Cell / response model
          ↓
Transcriptome ─ Proteome ─ Morphology
          ↓
Live-cell dynamic phenotype
          ↓
Functional reward + uncertainty
          ↓
Candidate ranking / next experiment
          ↓
Redesign
```

核心不是声称所有箭头今天都已解决，而是把每条箭头拆成可以单独验证的 scientific task。

# 57. 研究落地优先级

第一阶段：用公开 static data 建立可靠 baseline，例如 JUMP ORF / Cell Painting + protein representation。

第二阶段：加入 dynamic data，建立 trajectory representation 和 future-state prediction。

第三阶段：建立 prospective validation，验证 unseen perturbation / unseen protein。

第四阶段：进入 active learning / adaptive experiment / design feedback。

这样比一开始声称“做完整 Virtual Cell”更可信，也更适合面试。

# 58. 一句话收束

**我的研究兴趣可以概括成：把活细胞成像从一个观察工具变成 AI 可学习、可预测、可验证的 cellular functional layer，用它连接 Virtual Cell 与真实细胞，并进一步给蛋白和分子设计提供动态功能反馈。**
