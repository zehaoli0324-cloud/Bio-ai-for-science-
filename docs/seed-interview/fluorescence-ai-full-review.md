# 荧光成像中的人工智能与高通量计算生物学：完整研究综述归档

> 本文件将本轮对话中形成的长综述核心内容纳入 Seed 面试资料。检索基线为 2026-10-04，后续机构项目核对整理至 2026-10-07。项目适用性为研究选型，不代表已在本仓库复现。

## 1. 核心判断

荧光成像把分子定位、细胞结构和部分生理活动变成可观测信号，同时受 photon budget、diffraction、photobleaching、phototoxicity、label specificity 和 sampling frequency 限制。

AI 当前最明确的价值依次是：

1. 扩大可重复 measurement 的规模；
2. 在有限采集条件下提高特定 readout 的提取效率；
3. 在明确实验体系和验证范围内预测 biological state；
4. 更长期地参与实验选择与闭环干预。

最大的科学风险是把 algorithm output 直接当 biological fact。更平滑的图像未必强度更准确；更连续的 trajectory 可能掩盖 transient event；morphology similarity 不能证明 shared mechanism；generated cell image 不能代替未做的实验。

## 2. 高通量 profiling 生态

CellProfiler：显式 morphology / texture / intensity feature，是可解释 baseline。

CytoTable：将 high-content output 整理成表格。

pycytominer：aggregation、normalization、feature selection。

DeepProfiler：learned image feature。

Cell Painting/JUMP：统一 morphology readout 比较大量 chemical/genetic perturbation，适合 endpoint profiling 和 candidate screening，但固定细胞数据不能直接提供同一细胞的 event order。

Optical pooled screening：perturbation identity + imaging phenotype，通过 barcode/readout 建立映射。Brieflow 提供 integrated workflow；分析难点包括 registration、barcode recognition、cell boundary、identity assignment 和 QC。

数据工程必须保留 raw image、metadata、plate/well/field/cell/time/channel、analysis version、model weight、parameter 和 QC。

## 3. Segmentation / tracking / spot

Segmentation：Cellpose、StarDist、microSAM。

重点不是平均 overlap，而是 merge、split、miss、subpopulation bias 对 downstream science 的影响。

Cell tracking：Ultrack、Trackastra。

Point/particle tracking：TrackMate、trackpy。

RNA spot：Big-FISH。

Dense emitter localization：DECODE。

DNA locus tracking 需考虑 localization error、drift、blinking、defocus、association error。Enhancer-promoter contact 应传播 position uncertainty 到 distance/contact duration，而不是只设一个硬阈值。

## 4. Dynamic phenotype

SPOT 等工作把 Shape、Appearance、Motion 组织成 dynamic phenotype。动态信息可区分相同 endpoint 的不同过程。

53BP1：同样 focus number 可能来自持续形成、快速消失或长时间停留。

Mitochondria：同样 endpoint morphology 可能具有不同 change rate/recovery。

动态模型评价必须把 temporal resolution、recording duration 和 photodamage tradeoff 纳入。

## 5. Image restoration

观测可抽象为真实 fluorescence distribution 经过 optical convolution，再叠加 photon/detector noise 和 background。

逆问题通常没有唯一解，deep model 利用 prior 选择 plausible solution。因此要问：哪些信息来自 observation，哪些来自 learned prior？

CARE：paired restoration。

Noise2Void：blind-spot self-supervised denoising。

CAREamics：现代 restoration framework。

DeepInterpolation、DeepCAD-RT、DeepSeMi、SUPPORT：利用 temporal/spatiotemporal redundancy。

ZS-DeconvNet：zero-shot denoising/deconvolution 思路。

DL-SR/BioSR：deep super-resolution benchmarking。

MicroSplit：semantic unmixing。

时序 restoration 特别要检查 event onset、peak、rise、duration、disappearance；不能只看 correlation。

## 6. Super-resolution 边界

SIM 的额外 resolution 来自 structured illumination 的物理采集信息。普通 fluorescence image → neural SR 更多依赖 prior。

因此 neural network 生成 filament/spot separation 不能单独证明结构真实存在。应保留 raw、traditional reconstruction、model output，并用 orthogonal reference / downstream measurement 验证。

## 7. Representation / foundation model

OpenPhenom：Cell Painting pretrained representation，适合 perturbation morphology。

SubCell：protein localization / cellular image representation。

Cell-DINO / Channel Adaptive DINO：fluorescence self-supervised representation + channel adaptation。

好的 representation 应在控制 batch 后保留 biology。模型如果能预测 experiment date，也可能在 perturbation classification 上获得虚假高分。

## 8. Generative morphology / Virtual Cell

MorphoDiff：transcriptome-guided morphology generation。

MorphGen：perturbation-conditioned multi-channel cellular image generation。

生成模型适合 condition distribution modeling、data augmentation、candidate ranking，但 realistic image ≠ experimentally observed truth。

Virtual Cell 必须明确 perturbation、time、environment 和 output modality。只在训练条件附近生成 static image 的模型不能被当成完整 dynamics/causal simulator。

## 9. AI 能力边界

### Physical boundary

没有观测到的信息无法保证恢复为真。快速未采样事件、不可分离重叠来源、严重损伤 sample 只能用 prior 估计。

### Statistical boundary

换 microscope、cell type、label、drug、batch 会造成 distribution shift。训练集 performance 不代表新实验可靠。

### Biological boundary

Morphology 与 molecular state / mechanism 多对一；molecular state 与 fate 也多对一。因果解释需要 intervention 和 validation。

## 10. 评价体系

Segmentation：object-level merge/split/miss + downstream feature error。

Tracking：identity switch、track break、lineage error。

Intensity：bias、dynamic range。

Event：recall、false positive、timing error。

Motion：displacement distribution、diffusion parameter。

最终应问 downstream conclusion 是否稳定，例如 candidate ranking、effect size、subpopulation conclusion 是否在 independent batch 重现。

## 11. Pseudoreplication 与数据划分

一个 well 中几千个 cells 不等于几千次 independent experiments。应根据问题使用 well、batch、culture、donor 等独立层级。

Train/validation/test 应按 date、plate、field、trajectory、perturbation 组织，避免相邻 frame 或同一 biological unit 泄漏。

## 12. 最匹配个人背景的三个研究方向

### A. Low-light dynamic-event fidelity

问题：降低 light dose 后，restoration 是否仍保留 DNA locus proximity event、53BP1 dynamics、organelle sensor response？

评价 event time、duration、intensity bias、trajectory error，而非只看 image quality。

### B. Dynamic phenotype under perturbation

比较 static feature、handcrafted dynamic feature、learned trajectory representation，检验 early trajectory 是否增加 endpoint 之外的信息，并预测 future response。

### C. Uncertainty-aware adaptive acquisition

当 model 判断 event imminent 或 uncertainty 上升时，提高 sampling；其他阶段降低 exposure/frame rate。目标函数是 information gain vs photodamage，而不是 average image quality。

## 13. 前沿机构项目

Meta：Cell-DINO / Channel Adaptive DINO。

Microsoft：GigaTIME / GigaTIME-Flash，H&E → virtual multiplex IF/spatial protein prediction。

NVIDIA：VISTA-2D，cell instance segmentation/morphology。

Google Research + ISTA：LICONN，expansion microscopy + fluorescence + AI reconstruction of neural connectivity。

Recursion：Phenom / OpenPhenom / MAE microscopy，perturbation imaging representation。

CZI/Biohub：MorphGen、Virtual Cells Platform、SubCell ecosystem、Virtual Biology Initiative。

没有把 Protenix 当作 Seed fluorescence project；Protenix 属于 molecular structure prediction。对话检索也没有确认 Anthropic/OpenAI 存在与上述项目等价的 dedicated fluorescence program。

## 14. 开源入口清单

- CellProfiler/CellProfiler
- cytomining/CytoTable
- cytomining/pycytominer
- cytomining/DeepProfiler
- cheeseman-lab/brieflow
- cheeseman-lab/brieflow-analysis
- fractal-analytics-platform/fractal-tasks-core
- MouseLand/cellpose
- stardist/stardist
- computational-cell-analytics/micro-sam
- royerlab/ultrack
- weigertlab/trackastra
- trackmate-sc/TrackMate
- soft-matter/trackpy
- fish-quant/big-fish
- TuragaLab/DECODE
- fyz11/SPOT
- CSBDeep/CSBDeep
- juglab/n2v
- CAREamics/careamics
- AllenInstitute/deepinterpolation
- cabooster/DeepCAD-RT
- GuoxunZhang-THU/DeepSeMi
- NICALab/SUPPORT
- TristaZeng/ZS-DeconvNet
- qc17-THU/DL-SR
- juglab/MicroSplit
- HenriquesLab/ZeroCostDL4Mic
- CellProfiling/subcell-embed
- CellProfiling/subcell-analysis
- CellProfiling/SubCellPortable
- recursionpharma/maes_microscopy
- bowang-lab/MorphoDiff
- czi-ai/MorphGen
- facebookresearch/dinov2（Cell-DINO docs）
- google/ffn
- MONAI VISTA-2D model bundle

## 15. 面试结论

对生命科学背景研究者，真正稀缺的不是再背一个视觉 backbone，而是能够把 imaging physics、cell biology、machine learning 和 experimental design 连接起来，知道：什么可以可靠测量、什么只是 model hypothesis、什么需要下一次实验验证。

因此最有辨识度的方向是从 pixel metric 推进到 biological-event fidelity，再进一步进入 perturbation response、Virtual Cell validation 和 closed-loop experimental decision。
