import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

type EmpiricalCounts = {
  snapshot_id: string;
  campaign_count: number;
  comparison_row_count: number;
  campaign_004: {
    series_count: number;
    comparison_row_count: number;
  };
};

type BenchmarkCounts = {
  snapshot_id: string;
  released_samples: number;
  released_variants: number;
  released_languages: number;
  released_source_classes: number;
  released_perturbation_axes: number;
};

type ValidationCounts = {
  snapshot_id: string;
  benchmark_axis_count: number;
  benchmark_baseline_count: number;
  benchmark_language_count: number;
  benchmark_source_class_count: number;
  benchmark_variant_count: number;
  empirical_campaign_count: number;
  empirical_comparison_row_count: number;
  shared_bridge_axis_count: number;
};

type VisibilityChecks = {
  generated_at: string;
  status: "ok";
  evidence_snapshot: {
    campaigns: number;
    comparison_rows: number;
    campaign_004_rows: number;
  };
  benchmark_subset: {
    released_baselines: number;
    released_variants: number;
    released_languages: number;
    released_source_classes: number;
  };
  validation_v1_1: {
    snapshot_id: string;
    benchmark_baselines: number;
    benchmark_variants: number;
    benchmark_languages: number;
    benchmark_source_classes: number;
    shared_bridge_axes: number;
    framing: string;
  };
  guardrail: string;
};

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, "../../..");
const SITE_ROOT = resolve(ROOT, "../TakoVHS.github.io");

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(path, "utf-8")) as T;
}

function ensureParent(path: string): void {
  mkdirSync(dirname(path), { recursive: true });
}

function buildChecks(
  empirical: EmpiricalCounts,
  benchmark: BenchmarkCounts,
  validation: ValidationCounts,
): VisibilityChecks {
  return {
    generated_at: new Date().toISOString(),
    status: "ok",
    evidence_snapshot: {
      campaigns: empirical.campaign_count,
      comparison_rows: empirical.comparison_row_count,
      campaign_004_rows: empirical.campaign_004.comparison_row_count,
    },
    benchmark_subset: {
      released_baselines: benchmark.released_samples,
      released_variants: benchmark.released_variants,
      released_languages: benchmark.released_languages,
      released_source_classes: benchmark.released_source_classes,
    },
    validation_v1_1: {
      snapshot_id: validation.snapshot_id,
      benchmark_baselines: validation.benchmark_baseline_count,
      benchmark_variants: validation.benchmark_variant_count,
      benchmark_languages: validation.benchmark_language_count,
      benchmark_source_classes: validation.benchmark_source_class_count,
      shared_bridge_axes: validation.shared_bridge_axis_count,
      framing: "descriptive",
    },
    guardrail:
      "The evidence visibility layer is descriptive and review-oriented. It does not upgrade the scientific meaning of the current public evidence package into a settled empirical endpoint, a forensic workflow, or a stronger attribution claim.",
  };
}

function renderDashboard(checks: VisibilityChecks): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Evidence Visibility Dashboard – CogniPrint</title>
  <meta name="description" content="A compact visibility dashboard for the current CogniPrint evidence snapshot, public benchmark subset, and descriptive validation layer.">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <div class="page">
    <nav>
      <a href="/">Home</a>
      <a href="/research.html">Research</a>
      <a href="/papers/">Papers</a>
      <a href="/software/">Software</a>
      <a href="/pricing/">Hosted Access</a>
      <a href="/evidence/">Evidence</a>
      <a href="/review/">Review</a>
      <a href="/disclaimer/">Disclaimer</a>
    </nav>

    <header class="page-header">
      <h1>Evidence Visibility Dashboard</h1>
      <p class="lede">A compact descriptive dashboard for the current CogniPrint public evidence snapshot, benchmark subset, and validation v1.1 layer.</p>
    </header>

    <main>
      <section>
        <h2>Empirical Snapshot</h2>
        <p>CogniPrint currently has a working empirical evidence package supporting a follow-up manuscript.</p>
        <div class="evidence-stats" aria-label="Empirical snapshot counts">
          <div class="evidence-stat"><strong>${checks.evidence_snapshot.campaigns}</strong><span>controlled perturbation campaigns</span></div>
          <div class="evidence-stat"><strong>${checks.evidence_snapshot.comparison_rows}</strong><span>comparison rows in the current package</span></div>
          <div class="evidence-stat"><strong>${checks.evidence_snapshot.campaign_004_rows}</strong><span>campaign-004 comparison rows</span></div>
        </div>
      </section>

      <section>
        <h2>Released Benchmark Subset</h2>
        <p>The first released public benchmark subset remains intentionally small and should be read as a benchmark-growth layer rather than as a broad validation endpoint.</p>
        <div class="evidence-stats" aria-label="Benchmark subset counts">
          <div class="evidence-stat"><strong>${checks.benchmark_subset.released_baselines}</strong><span>released benchmark baselines</span></div>
          <div class="evidence-stat"><strong>${checks.benchmark_subset.released_variants}</strong><span>released benchmark variants</span></div>
          <div class="evidence-stat"><strong>${checks.benchmark_subset.released_languages}</strong><span>released languages in the v1 subset</span></div>
        </div>
      </section>

      <section>
        <h2>Validation v1.1</h2>
        <p>The current statistical validation layer is descriptive. It helps review benchmark-versus-campaign behavior, but it does not by itself justify stronger inferential framing.</p>
        <div class="evidence-stats" aria-label="Validation coverage counts">
          <div class="evidence-stat"><strong>${checks.validation_v1_1.benchmark_baselines}</strong><span>benchmark baselines in validation v1.1</span></div>
          <div class="evidence-stat"><strong>${checks.validation_v1_1.benchmark_variants}</strong><span>benchmark variants in validation v1.1</span></div>
          <div class="evidence-stat"><strong>${checks.validation_v1_1.shared_bridge_axes}</strong><span>shared benchmark–campaign bridge axes</span></div>
        </div>
      </section>

      <section>
        <h2>Interpretation Guardrail</h2>
        <p>${checks.guardrail}</p>
        <div class="review-actions">
          <a href="https://github.com/TakoVHS/CogniPrint/tree/main/evidence/empirical-v1">Empirical snapshot</a>
          <a href="https://github.com/TakoVHS/CogniPrint/tree/main/evidence/public-benchmark-v1">Public benchmark subset</a>
          <a href="https://github.com/TakoVHS/CogniPrint/tree/main/evidence/statistical-validation-v1">Validation v1.1 layer</a>
          <a href="https://github.com/TakoVHS/CogniPrint/blob/main/docs/evidence-visibility-dashboard.md">Dashboard documentation</a>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
`;
}

function main(): void {
  const empirical = readJson<EmpiricalCounts>(join(ROOT, "evidence/empirical-v1/counts.json"));
  const benchmark = readJson<BenchmarkCounts>(join(ROOT, "evidence/public-benchmark-v1/counts.json"));
  const validation = readJson<ValidationCounts>(join(ROOT, "evidence/statistical-validation-v1/counts.json"));
  const checks = buildChecks(empirical, benchmark, validation);

  const checksPath = join(ROOT, "docs/evidence-visibility-checks.json");
  const dashboardPath = join(SITE_ROOT, "evidence/dashboard.html");

  ensureParent(checksPath);
  ensureParent(dashboardPath);

  writeFileSync(checksPath, JSON.stringify(checks, null, 2) + "\n", "utf-8");
  writeFileSync(dashboardPath, renderDashboard(checks), "utf-8");

  console.log(`Generated ${checksPath}`);
  console.log(`Generated ${dashboardPath}`);
}

main();
