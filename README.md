# claude-skills

Production-grade Claude Code skills, auto-research validated.

## Skills

| Skill | Description | Validated | Lines |
|-------|-------------|-----------|-------|
| [`/deep-research`](skills/deep-research/) (or `/dr`) | Deep Research — exhaustive, evidence-based investigation of any topic | 95 runs, 85+ domains, 25/25 evals | 191 |

## Install

```bash
# As a Claude Code plugin (all skills)
/plugin install deep-research@yachi/claude-skills

# Or install manually
git clone https://github.com/yachi/claude-skills.git
cp -r claude-skills/skills/deep-research ~/.claude/commands/deep-research
# For short alias:
ln -s ~/.claude/commands/deep-research ~/.claude/commands/dr
```

## `/deep-research` (alias: `/dr`)

Industrial-grade research skill. Every claim survives cross-examination by domain experts.

**10 phases:** Clarify → Decompose → Multi-Source Investigation → Industry Standards Audit → Quantitative Analysis → Adversarial Review → **Convergence Loop** → Practitioner Check → Verify → Synthesis

**Standards:** ICD 203 (9/9), GRADE, NIST reproducibility, CRAAP

**Auto-research validated:**
- 95 runs across 85+ domains (tech, finance, medical, legal, industrial, adversarial)
- 26 regex evals (6 tiers) + LLM-as-judge (fact-checks 3 claims per output)
- Convergence loop: self-drives iterative refinement until zero research gaps remain (max 3 rounds)
- Self-improving loop (Karpathy-inspired): `evolve-v2.md`

**Includes:**
- 104 research outputs across every domain imaginable
- 9 LLM judge assessments with fact-check details
- Original benchmark data (with-skill vs baseline, 5 domains + 3 convergence evals)
- Visual benchmark dashboard
- Auto-research infrastructure (grade.py, judge.md, evolve loops)

See [`skills/deep-research/`](skills/deep-research/) for full docs, examples, and the auto-research toolkit.

## Structure

```
claude-skills/
├── .claude-plugin/marketplace.json
├── skills/
│   └── deep-research/
│       ├── SKILL.md                    ← the skill (191 lines)
│       ├── eval/
│       │   ├── grade.py                ← 26-eval regex grading (6 tiers)
│       │   └── judge.md                ← LLM fact-checker (/25)
│       ├── autoresearch/
│       │   ├── evolve-v2.md            ← self-improvement loop
│       │   ├── evolve-v1.md            ← legacy loop
│       │   ├── program.md             ← test prompts + 11 criteria
│       │   ├── log.md                  ← full 95-run log
│       │   ├── outputs/               ← 95 runs + 9 judges
│       │   └── examples/              ← curated best/worst
│       └── benchmark/
│           ├── iteration-1/            ← with-skill vs baseline (5 domains)
│           ├── iteration-2/            ← convergence loop evals (3 domains)
│           └── dashboard/              ← visual dashboard
├── LICENSE (MIT)
└── README.md
```

## Adding new skills

```
skills/
├── deep-research/  ← existing
│   └── SKILL.md
└── your-skill/  ← add here
    └── SKILL.md
```

Then add to `.claude-plugin/marketplace.json`.

## License

MIT
