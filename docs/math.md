# Mathematical Note for CogniPrint

## Purpose

This note records a conservative mathematical foundation for the CogniPrint research programme. It is written to support reproducible terminology, preprint preparation, and future formal refinement.

The document avoids product claims and uses only research-safe language.

## 1. Basic setting

Let $\mathcal{V}$ be a finite vocabulary and let

$$
\mathcal{T} = \bigcup_{n \geq 1} \mathcal{V}^n
$$

be the set of all finite token sequences over $\mathcal{V}$.

An element $T \in \mathcal{T}$ is called a **text sample**.

For a text sample $T$, let $|T|$ denote its token length.

## 2. Feature map and cognitive fingerprint

Let

$$
\phi : \mathcal{T} \to \mathbb{R}^d
$$

be a feature map whose coordinates are measurable statistics extracted from a text sample. Typical coordinates may include length-normalised counts, variation measures, dispersion measures, or other bounded empirical summaries.

### Definition 2.1 (Cognitive fingerprint)
The vector

$$
\phi(T) = (\phi_1(T), \ldots, \phi_d(T))
$$

is called the **cognitive fingerprint** of the text sample $T$.

### Definition 2.2 (Normalised profile)
If $\phi(T) \neq 0$, define the normalised profile

$$
\widehat{\phi}(T) = \frac{\phi(T)}{\|\phi(T)\|_2}.
$$

The normalised profile is used when comparison must be invariant under global rescaling.

## 3. Profile similarity

### Definition 3.1 (Euclidean profile distance)
For two text samples $T_1, T_2 \in \mathcal{T}$,

$$
D_2(T_1, T_2) = \|\phi(T_1) - \phi(T_2)\|_2.
$$

### Definition 3.2 (Cosine profile similarity)
If both fingerprints are non-zero, define

$$
S_{\cos}(T_1, T_2) = \frac{\langle \phi(T_1), \phi(T_2) \rangle}{\|\phi(T_1)\|_2 \|\phi(T_2)\|_2}.
$$

This quantity measures angular alignment in feature space.

## 4. Perturbation model

Let $d_{\mathrm{edit}}(T_1, T_2)$ denote an edit distance between two token sequences.

The role of perturbation analysis is to ask how much the fingerprint can change under a bounded number of token edits.

### Assumption 4.1 (Coordinate stability)
For each coordinate $\phi_i$ there exists a constant $L_i \geq 0$ such that

$$
|\phi_i(T_1) - \phi_i(T_2)| \leq L_i \, d_{\mathrm{edit}}(T_1, T_2)
$$

for all relevant text pairs $(T_1, T_2)$ in the analysis regime.

This is a modelling assumption, not a universal theorem about every possible feature.

### Proposition 4.2 (Fingerprint stability)
Under Assumption 4.1,

$$
\|\phi(T_1) - \phi(T_2)\|_2 \leq \Big( \sum_{i=1}^d L_i^2 \Big)^{1/2} d_{\mathrm{edit}}(T_1, T_2).
$$

#### Proof
By coordinate stability,

$$
(\phi_i(T_1) - \phi_i(T_2))^2 \leq L_i^2 d_{\mathrm{edit}}(T_1, T_2)^2.
$$

Summing over $i = 1, \dots, d$ gives

$$
\|\phi(T_1) - \phi(T_2)\|_2^2 \leq \sum_{i=1}^d L_i^2 \, d_{\mathrm{edit}}(T_1, T_2)^2.
$$

Taking square roots yields the result.

## 5. Normalised comparison bounds

When fingerprints are normalised, one wants control of the angular comparison under perturbation.

### Assumption 5.1 (Non-degeneracy)
There exists $m > 0$ such that

$$
\|\phi(T)\|_2 \geq m
$$

for all text samples considered in the experiment.

### Proposition 5.2 (Normalised profile stability)
Assume Proposition 4.2 and Assumption 5.1. Then there exists a constant $C > 0$ such that

$$
\|\widehat{\phi}(T_1) - \widehat{\phi}(T_2)\|_2 \leq C \, d_{\mathrm{edit}}(T_1, T_2)
$$

for all text samples in the analysis regime.

#### Proof sketch
The map $x \mapsto x / \|x\|_2$ is Lipschitz on the set $\{x \in \mathbb{R}^d : \|x\|_2 \geq m\}$. Combining this with Proposition 4.2 yields the claim.

## 6. Aggregated profiles over corpora

For a finite collection of text samples

$$
\mathcal{C} = \{T^{(1)}, \dots, T^{(N)}\},
$$

one may define the empirical mean profile

$$
\overline{\phi}(\mathcal{C}) = \frac{1}{N} \sum_{j=1}^{N} \phi\big(T^{(j)}\big).
$$

This object is useful for studying group-level regularities in feature space.

### Proposition 6.1 (Mean-profile perturbation bound)
If $\phi$ satisfies Proposition 4.2 coordinate-wise, then for two aligned corpora $\mathcal{C}_1, \mathcal{C}_2$ of equal size,

$$
\|\overline{\phi}(\mathcal{C}_1) - \overline{\phi}(\mathcal{C}_2)\|_2
\leq
\frac{1}{N} \sum_{j=1}^{N} K \, d_{\mathrm{edit}}\big(T_1^{(j)}, T_2^{(j)}\big),
$$

where $K = (\sum_i L_i^2)^{1/2}$.

This follows directly from Proposition 4.2 and the triangle inequality.

## 7. Research interpretation

The mathematical role of CogniPrint is not to produce final judgments. Its role is to define:

- a feature map from texts into a finite-dimensional space;
- similarity and distance notions in that space;
- stability questions under perturbation;
- empirical procedures for studying structure in collections of text samples.

## 8. Open directions

The following directions remain open and should be framed as research questions rather than settled claims:

1. Conditions under which a chosen feature map is stable under realistic perturbations.
2. Identification of feature families with useful invariance properties.
3. Concentration behaviour of empirical mean profiles for large corpora.
4. Geometry of profile clusters under different normalisation schemes.
5. Robust comparison of corpora with unequal length and heterogeneous style distributions.

## 9. Canonical sentence

**CogniPrint is a mathematical research framework for cognitive fingerprint analysis, profile comparison, and reproducible study of statistical regularities in text.**
