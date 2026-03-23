# Contributing to claude-skills

Thanks for your interest in contributing! This project is a monorepo of production-grade skills for [Claude Code](https://claude.ai).

## Adding a New Skill

1. Create a directory under `skills/your-skill-name/`
2. Add a `SKILL.md` file — this is the skill prompt that Claude Code executes
3. Open a PR with:
   - A description of what the skill does
   - Example usage and expected output
   - Any eval/benchmark data if available

See [`skills/deep-research/`](skills/deep-research/) for a reference implementation with evals, benchmarks, and auto-research infrastructure.

## Improving Existing Skills

1. Fork the repo and create a feature branch
2. Make your changes to the skill's `SKILL.md`
3. If modifying `/deep-research`, run the eval suite:
   ```bash
   python skills/deep-research/eval/grade.py
   ```
4. Include before/after eval scores in your PR description

## Reporting Issues

- Use the [bug report template](https://github.com/yachi/claude-skills/issues/new?template=bug_report.yml) for bugs
- Use the [feature request template](https://github.com/yachi/claude-skills/issues/new?template=feature_request.yml) for ideas

## Code of Conduct

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
