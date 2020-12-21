# mirrors-cfn-nag

Mirror of [cfn-nag](https://github.com/stelligent/cfn_nag) for [pre-commit](https://pre-commit.com).
This repo also provides a wrapper that allows running the hook only on files passed
from pre-commit instead of running on a directory or single file the way it works
in cfn-nag. By default `--fail-on-warnings` is enabled. If you are changing args
for this hook make sure to add `--input-path` at the end.

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/AleksaC/mirrors-cfn-nag
  rev: v0.6.13  # Use the sha / tag you want to point at
  hooks:
   - id: cfn-nag
     files: my-cfn-template.yml  # Set to regex matching filenames of your cloudformation templates
```
