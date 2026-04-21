# Cognitive Fingerprints: A Mathematical Framework for Statistical Profiling of Text

## Abstract (working draft)

We introduce a mathematical framework for representing text samples by compact finite-dimensional profiles, termed **cognitive fingerprints**. The framework is based on a feature map from token sequences into a Euclidean space of empirical statistics. This representation supports quantitative comparison of text samples through profile distances and similarity measures, as well as perturbation-based questions about stability under bounded edits. The goal of the framework is not to provide definitive judgments about a text, but to establish a reproducible mathematical basis for profile construction, profile comparison, and empirical study of structure in collections of text samples. We formulate the basic setting, define the profile representation, and record conservative stability statements under explicit modelling assumptions.

## 1. Introduction

Quantitative study of text often requires a representation that is compact enough for analysis, yet expressive enough to preserve regularities of interest. A common mathematical strategy is to map structured objects into finite-dimensional feature spaces and then reason about geometry, distances, and perturbations in that space. In the case of text, such a representation provides a principled way to study regularity, variation, and similarity across samples without reducing the problem to a single scalar summary.

The CogniPrint programme adopts this viewpoint. Its central object is the **cognitive fingerprint** of a text sample: a finite-dimensional vector of empirical statistics extracted from the text. The purpose of this object is not to act as a final judgment mechanism. Rather, it serves as a mathematical profile that enables reproducible comparison of text samples and collections of text samples.

This framing leads naturally to several mathematical questions. First, what class of feature maps yields a useful profile representation? Second, how should one compare profiles in a way that respects both magnitude and geometric orientation in feature space? Third, under what assumptions does the profile remain stable when a text sample is perturbed by a bounded number of edits? Fourth, how do aggregated profiles behave for collections of samples?

The present draft takes a deliberately conservative position. It does not claim universal invariance properties for arbitrary feature maps, nor does it claim that any profile representation can support definitive conclusions about authorship or source. Instead, it introduces a formal setting, states explicit assumptions, and derives basic bounds that clarify what can be proved once a suitable feature map has been fixed.

### 1.1. Contributions of the draft

This draft makes the following limited but precise contributions:

1. It defines a general feature-map framework for constructing finite-dimensional text profiles.
2. It formalises the notion of a cognitive fingerprint and its normalised counterpart.
3. It introduces profile comparison through Euclidean distance and cosine similarity.
4. It states conservative stability results under explicit coordinate-wise Lipschitz assumptions.
5. It defines aggregated profiles for corpora and records the corresponding mean-profile perturbation bound.

### 1.2. Scope and limitations

The analysis in this draft is intentionally narrow in scope. The results are conditional on explicit assumptions about the chosen feature coordinates. They are not intended to be read as universal theorems about all conceivable text statistics. Likewise, this draft does not yet include a full empirical section. Its primary purpose is to establish a clean mathematical foundation and a disciplined vocabulary for future formal and empirical work.

## 2. Formal setting

Let $\mathcal{V}$ be a finite vocabulary, and let

$$
\mathcal{T} = \bigcup_{n \geq 1} \mathcal{V}^n
$$

be the set of all finite token sequences over $\mathcal{V}$. An element $T \in \mathcal{T}$ is called a **text sample**. Its token length is denoted by $|T|$.

### 2.1. Feature map

Let

$$
\phi : \mathcal{T} \to \mathbb{R}^d
$$

be a feature map. The coordinates of $\phi$ are measurable empirical statistics extracted from a text sample. Depending on the application, such coordinates may include bounded counts, length-normalised summaries, variation measures, or dispersion measures.

The theory developed here does not require a specific feature family, but it does require that the chosen coordinates admit explicit control under perturbation in the regime of interest.

### 2.2. Cognitive fingerprint

The vector

$$
\phi(T) = (\phi_1(T), \ldots, \phi_d(T))
$$

is called the **cognitive fingerprint** of the text sample $T$.

When profile comparison should be invariant under global rescaling, one may also work with the normalised profile

$$
\widehat{\phi}(T) = \frac{\phi(T)}{\|\phi(T)\|_2},
$$

whenever $\phi(T) \neq 0$.

### 2.3. Profile comparison

For two text samples $T_1, T_2 \in \mathcal{T}$, define the Euclidean profile distance

$$
D_2(T_1, T_2) = \|\phi(T_1) - \phi(T_2)\|_2.
$$

If both profiles are non-zero, define the cosine profile similarity

$$
S_{\cos}(T_1, T_2) = \frac{\langle \phi(T_1), \phi(T_2) \rangle}{\|\phi(T_1)\|_2 \, \|\phi(T_2)\|_2}.
$$

The first quantity measures absolute separation in feature space, while the second measures angular alignment.

### 2.4. Perturbation model

Let $d_{\mathrm{edit}}(T_1, T_2)$ denote an edit distance on token sequences. The central perturbation question is how much the profile can change when the text sample is modified by a bounded number of edits.

We therefore impose the following assumption.

**Assumption 2.1 (Coordinate stability).** For each coordinate $\phi_i$ there exists a constant $L_i \geq 0$ such that

$$
|\phi_i(T_1) - \phi_i(T_2)| \leq L_i \, d_{\mathrm{edit}}(T_1, T_2)
$$

for all text pairs in the analysis regime.

This is a modelling assumption about the selected feature family. It is not asserted as a universal fact for arbitrary text statistics.

### 2.5. Basic stability statement

Under Assumption 2.1 one obtains the bound

$$
\|\phi(T_1) - \phi(T_2)\|_2 \leq \Big(\sum_{i=1}^{d} L_i^2\Big)^{1/2} d_{\mathrm{edit}}(T_1, T_2).
$$

This follows by squaring the coordinate bounds, summing over all coordinates, and taking square roots.

### 2.6. Aggregated profiles

For a finite collection of text samples

$$
\mathcal{C} = \{T^{(1)}, \ldots, T^{(N)}\},
$$

one may define the empirical mean profile

$$
\overline{\phi}(\mathcal{C}) = \frac{1}{N} \sum_{j=1}^{N} \phi\big(T^{(j)}\big).
$$

This aggregated object is useful when the object of study is a corpus rather than a single sample.

## 3. Immediate next section

The next section of the preprint should state the normalised comparison bound, extend the argument to aggregated profiles, and make explicit which parts of the framework are theorem-level statements and which parts remain open empirical questions.
