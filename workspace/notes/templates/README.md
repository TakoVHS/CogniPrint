# Campaign Templates

These YAML files are starter templates for repeatable CogniPrint empirical campaigns.

## Available templates

- `single-baseline-perturbation.yml`
- `multi-series-perturbation-campaign.yml`
- `multilingual-comparison-campaign.yml`

## Usage

1. Copy one template into `workspace/notes/`.
2. Rename it for the active campaign.
3. Replace the example file paths with your real local inputs.
4. Run:

```bash
cogniprint campaign run --config workspace/notes/<your-campaign>.yml
cogniprint campaign summarize --campaign-dir workspace/campaigns/<campaign-id>
```

## Interpretation rule

Campaign outputs should be read as observed profile changes, perturbation effects, and stability tendencies. They are not definitive source judgments.
