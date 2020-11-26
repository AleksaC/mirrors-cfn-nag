# mirrors-cfn-nag

Mirror of [cfn-nag](https://github.com/stelligent/cfn_nag) for [pre-commit](https://pre-commit.com).

## Usage
Add this to your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/AleksaC/mirrors-cfn-nag
  rev: v0.6.13  # Use the sha / tag you want to point at
  hooks:
   - id: cfn-nag
```
