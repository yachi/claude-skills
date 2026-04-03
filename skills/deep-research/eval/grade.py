#!/usr/bin/env python3
"""Grade /dr skill outputs — 35 binary evals across 9 tiers. Usage: python3 grade.py <output.md> [--flawed-premise] [--verify-urls]"""

import re, sys, subprocess, random

def grade(path, has_flawed_premise=False, verify_urls=False):
    with open(path) as f:
        content = f.read()

    r = {}

    # ═══ TIER 0: Structural presence (original 8) ═══

    urls = list(set(re.findall(r'https?://[^\s\)\]>\"\']+', content)))
    r['E1_urls_15+'] = len(urls) >= 15

    r['E2_confidence_%'] = bool(re.search(r'\d+%', content) and re.search(r'(?i)confiden', content))

    tables = re.findall(r'\|[^\n]+\|(?:\n\|[^\n]+\|)+', content)
    r['E3_comparison_table'] = any(t.count('\n') >= 3 for t in tables)

    r['E4_standard_clause'] = bool(re.search(
        r'(?:RFC|Section|Clause|Art|CC)\s*\d+[\.\d]*|ISO[\s/]\d+|'
        r'CFR \d+|ILO \d+|ERISA|Basel|Dodd.Frank|FIFRA|EAR|ITAR|'
        r'ICD \d+|FIPS \d+|Part \d+|OPC \d+|ISA.\d+', content))

    code_blocks = re.findall(r'```[\s\S]*?```', content)
    r['E5_code_block'] = len(code_blocks) >= 1

    if has_flawed_premise:
        r['E6_premise_challenge'] = bool(re.search(
            r'(?i)(premise|assumption|incorrect|false|misleading|'
            r'not.+(?:always|possible|viable)|flawed|myth|kill.switch|reject)', content))
    else:
        r['E6_premise_challenge'] = True

    r['E7_cost_figures'] = bool(re.search(
        r'\$[\d,]+|EUR\s*[\d,]+|€[\d,]+|GBP\s*[\d,]+|£[\d,]+|¥[\d,]+|\d+\s*(?:USD|EUR|GBP)', content))

    r['E8_counterargument'] = bool(re.search(
        r'(?i)(counterargument|counter-argument|adversarial|devil.s advocate|dissent|rebuttal)', content))

    # ═══ TIER 1: Verifiability proxy (regex-based) ═══

    domains = re.findall(r'https?://([^/\s]+)', ''.join(urls[:30]))
    legit = sum(1 for d in domains if re.search(r'\.(gov|edu|org|com|io|dev|net|int|mil)$', d))
    r['E9_urls_legit_tlds'] = legit >= 10

    specific = re.findall(
        r'(?:Section|Clause|Art(?:icle)?\.?|Part|Annex|Table|Req\.?|CC|SR)\s*\d+[\.\d]*', content)
    r['E10_3+_specific_clauses'] = len(specific) >= 3

    cited_data_lines = 0
    for line in content.split('\n'):
        has_num = bool(re.search(r'\d+[%$KMB]|\$[\d,]+|EUR\s*\d|\d+\.\d+', line))
        has_src = bool(re.search(r'\[.*?\]\(http|Source:|cited|per\s|according', line, re.IGNORECASE))
        if has_num and has_src:
            cited_data_lines += 1
    r['E11_sourced_numbers'] = cited_data_lines >= 3

    # ═══ TIER 2: Quality ═══

    real_code = 0
    for block in code_blocks:
        if re.match(r'```(?:python|bash|sh|javascript|typescript|go|rust|java|sql|yaml|json|toml|hcl|terraform|proto|xml)', block):
            if re.search(r'(?:import |from |def |function |const |let |var |SELECT |CREATE |resource |pip |npm |aws |kubectl |docker |curl |git )', block):
                real_code += 1
    r['E12_real_code'] = real_code >= 1 if code_blocks else True

    rec = re.search(r'(?i)## Recommendation[\s\S]*?(?=\n## [^#]|\Z)', content)
    if rec:
        conds = re.findall(r'(?i)(?:if|when|unless|condition|change|switch|pivot|reconsider|revisit)', rec.group())
        r['E13_change_conditions'] = len(conds) >= 2
    else:
        r['E13_change_conditions'] = False

    words = len(content.split())
    r['E14_word_count_ok'] = 1500 <= words <= 5000

    # ═══ TIER 3: Rigor ═══

    findings = re.search(r'(?i)## Key Findings[\s\S]*?(?=\n## [^#]|\Z)', content)
    r['E15_findings_verified'] = '[unverified]' not in (findings.group().lower() if findings else '')

    sources = re.search(r'(?i)## Sources[\s\S]*?(?=\n## [^#]|\Z)', content)
    if sources:
        r['E16_sources_organized'] = bool(re.search(r'(?:\*\*[^*]+\*\*:?|###\s)', sources.group()))
    else:
        r['E16_sources_organized'] = False

    # ═══ TIER 4: Ground Truth ═══

    # E17: Sample 5 URLs, check they return HTTP 200 (requires network, opt-in with --verify-urls)
    if verify_urls and urls:
        sample = random.sample(urls, min(5, len(urls)))
        live_count = 0
        dead_urls = []
        for url in sample:
            try:
                result = subprocess.run(
                    ['curl', '-sL', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '5', url],
                    capture_output=True, text=True, timeout=10
                )
                code = result.stdout.strip()
                if code.startswith(('2', '3')):  # 2xx or 3xx = alive
                    live_count += 1
                else:
                    dead_urls.append(f'{url} -> {code}')
            except:
                dead_urls.append(f'{url} -> timeout')
        r['E17_urls_resolve'] = live_count >= 4  # 4/5 must resolve
        if dead_urls:
            print(f'  E17 dead URLs: {dead_urls}')
    else:
        r['E17_urls_resolve'] = None  # skipped

    # E18: No duplicate content across sections (detect copy-paste)
    sections = re.split(r'\n## ', content)
    seen_paragraphs = set()
    duplicates = 0
    for section in sections:
        paragraphs = [p.strip() for p in section.split('\n\n') if len(p.strip()) > 100]
        for p in paragraphs:
            if p in seen_paragraphs:
                duplicates += 1
            seen_paragraphs.add(p)
    r['E18_no_duplicates'] = duplicates == 0

    # ═══ TIER 5: Industrial Standards (GRADE, CRAAP, ICD 203, NIST) ═══

    # E21: Source recency (CRAAP Currency) — 50%+ of URLs from domains suggesting recent content
    year_matches = re.findall(r'20(?:2[3-9]|[3-9]\d)', content)  # years 2023-2099
    r['E21_source_recency'] = len(year_matches) >= 5  # at least 5 references to recent years

    # E22: Evidence hierarchy disclosure (GRADE) — at least 1 finding explicitly states evidence level
    evidence_levels = re.findall(
        r'(?i)(meta.analysis|systematic review|controlled (?:trial|experiment|study)|'
        r'RCT|cohort study|case study|observational|longitudinal|peer.reviewed|'
        r'\[(?:high|moderate|low|very low) (?:confidence|evidence)\])',
        content
    )
    r['E22_evidence_grading'] = len(evidence_levels) >= 1

    # E23: No unsourced statistics in Key Findings (NIST + ICD 203)
    if findings:
        findings_text = findings.group()
        # Find lines with numbers but no citation
        unsourced_stats = 0
        for line in findings_text.split('\n'):
            has_stat = bool(re.search(r'\d+[%$KMB]|\$[\d,]+|EUR\s*\d|\d+\.\d+\s*(?:x|ms|s\b|GB|TB|MB)', line))
            has_cite = bool(re.search(r'\[.*?\]\(http|\(.*?20\d\d.*?\)|Source:|according|per\s', line, re.IGNORECASE))
            if has_stat and not has_cite and len(line.strip()) > 20:
                unsourced_stats += 1
        r['E23_findings_all_sourced'] = unsourced_stats == 0
    else:
        r['E23_findings_all_sourced'] = True  # no findings section = auto-pass

    # ═══ TIER 6: Convergence Loop (iterative refinement) ═══

    # E24: Evidence of iterative refinement — gap analysis or refinement rounds documented
    refinement_markers = re.findall(
        r'(?i)(refinement round|iteration \d|round \d|follow.up investigation|'
        r'gap analysis|additional research|upon further investigation|'
        r'revisiting|re-investigat|second pass|deeper investigation|'
        r'initial research .{0,30} additional|updating research plan|'
        r'emerged during|surfaced during|discovered during research)',
        content
    )
    r['E24_iterative_refinement'] = len(refinement_markers) >= 1

    # E25: Contradiction resolution — identifies conflicting sources and resolves them
    contradiction_markers = re.findall(
        r'(?i)(contradict|conflict(?:ing|s)|disagree|inconsistent|'
        r'source.{0,20}(?:claims?|says?|shows?|argues?).{0,40}(?:but|however|whereas|while)|'
        r'(?:however|but|whereas).{0,40}(?:another|other|different)\s+(?:source|study|report|benchmark))',
        content
    )
    r['E25_contradiction_resolution'] = len(contradiction_markers) >= 1

    # E26: Assumption audit completeness — no uncertain assumptions left uninvestigated
    assumption_section = re.search(r'(?i)##[#]?\s*Assumption[s]?\s*(?:Audit|Review)?[\s\S]*?(?=\n##[^#]|\Z)', content)
    if assumption_section:
        uncertain_count = len(re.findall(r'(?i)\buncertain\b', assumption_section.group()))
        investigated = len(re.findall(
            r'(?i)uncertain.{0,100}(?:investigated|researched|verified|resolved|could not verify|remains)',
            assumption_section.group()
        ))
        # Pass if no uncertain assumptions, or if uncertain ones have follow-up notes
        r['E26_assumptions_investigated'] = uncertain_count == 0 or investigated >= uncertain_count
    else:
        # Fallback: check whole doc for reclassification evidence (assumptions resolved before audit table)
        reclassified = re.findall(
            r'(?i)(?:moved from|reclassified.*from).{0,30}uncertain.{0,30}(?:to|→).{0,30}(?:verified|reasonable|confirmed)',
            content
        )
        has_audit = bool(re.search(r'(?i)assumption', content))
        r['E26_assumptions_investigated'] = len(reclassified) >= 1 or not has_audit

    # E19: Executive summary is self-contained (has answer + confidence in first 3 sentences)
    exec_summary = re.search(r'(?i)## Executive Summary\s*\n([\s\S]*?)(?=\n## [^#]|\Z)', content)
    if exec_summary:
        summary_text = exec_summary.group(1).strip()
        has_answer = len(summary_text) > 50  # not trivially short
        has_conf = bool(re.search(r'\d+%', summary_text))
        r['E19_exec_summary_complete'] = has_answer and has_conf
    else:
        r['E19_exec_summary_complete'] = False

    # E20: Alternatives section exists and has 2+ options with data
    alts = re.search(r'(?i)## Alternatives[\s\S]*?(?=\n## [^#]|\Z)', content)
    if alts:
        alt_text = alts.group()
        alt_options = re.findall(r'(?:###\s|\d+\.\s\*\*|\*\*\d+\.)', alt_text)
        has_data = bool(re.search(r'\d+[%$KMB]|\$[\d,]+|EUR', alt_text))
        r['E20_alternatives_with_data'] = len(alt_options) >= 2 and has_data
    else:
        r['E20_alternatives_with_data'] = False

    # ═══ TIER 7: Expert Delegation (multi-perspective research) ═══

    # E27: Multi-perspective synthesis — output shows 3+ distinct domain perspectives
    _DOMAINS = (r'regulatory|compliance|legal|technical|architecture|security|financial|cost|economic|'
                r'clinical|medical|infrastructure|networking|operational|business|UX|user experience|privacy|data protection')
    perspective_hits = re.findall(
        r'(?i)(?:###?\s*(?:' + _DOMAINS + r')\s*(?:analysis|review|assessment|findings|perspective)|'
        r'(?:from\s+(?:a|the)\s+)?(?:' + _DOMAINS + r')\s*(?:perspective|standpoint|viewpoint|angle|lens|analysis|expert|specialist))',
        content
    )
    r['E27_multi_perspective'] = len(set(perspective_hits)) >= 3

    # E28: Cross-domain constraint interaction — addresses how constraints interact, not just independently
    interaction_markers = re.findall(
        r'(?i)(interact(?:ion|s|ing)|intersect(?:ion|s|ing)|compound(?:s|ing|ed)|'
        r'combined (?:effect|impact|constraint|requirement)|'
        r'(?:constraint|requirement)s?.{0,30}(?:conflict|tension|tradeoff|trade-off)|'
        r'simultaneously|concurrently.{0,30}(?:comply|satisfy|meet)|'
        r'cross-(?:domain|cutting|jurisdict)|multi-(?:jurisdict|regulat))',
        content
    )
    r['E28_constraint_interaction'] = len(interaction_markers) >= 2

    # E29: Multi-framework depth — 3+ distinct regulatory/standards frameworks cited
    framework_refs = {m.upper().replace(' ', '') for m in re.findall(
        r'(?i)(GDPR|PSD2|APPI|LGPD|BDSG|NDPR|HIPAA|PCI.DSS|SOX|MiCA|DORA|FCA|FinCEN|'
        r'Kenya.{0,10}(?:Data|DPA)|Nigeria.{0,10}(?:Data|NDPR)|Basel|Dodd.Frank|MiFID|CCPA|PIPL|'
        r'ViDA|HMRC|MTD|Peppol|EMIR|SFDR|NIS2|CRA|CSRD|AI.Act|DSA|DMA|'
        r'NIST|OWASP|ISO\s*\d+|IEC\s*\d+|EN\s*\d+|RFC\s*\d+|'
        r'ERISA|FIFRA|EAR|ITAR|TSCA|CPSC|OSHA|EPA|FDA|FTC|SEC|'
        r'Cartagena|CBD|UNCLOS|ILO|UNDRIP|WHO|WTO|WIPO)',
        content
    )}
    r['E29_multi_framework_depth'] = len(framework_refs) >= 3

    # ═══ TIER 8: Actionability & Grounding (environment-aware implementation) ═══

    # E30: Artifact specificity — Implementation Guidance names specific actionable artifacts
    # (file paths, form numbers, tool names, regulatory bodies, sequenced steps, templates)
    # Generic across domains: a pharma report names "FDA Form 1571", a devops report names
    # "~/.tool-versions", a legal report names "Annex III risk assessment dossier"
    impl_sections = re.split(r'\n(?=## )', content)
    impl_text = next((s for s in impl_sections if 'Implementation' in s.split('\n')[0]), content)
    artifacts = re.findall(
        r'(?i)('
        r'/(?:etc|home|usr|var|opt|Users|tmp|app|srv)[\w/._-]+|'      # absolute file paths
        r'~\/[\w/._-]+|'                                              # home-relative paths
        r'(?:package|config|docker|requirements|Cargo|go)\.\w+|'      # config files
        r'(?:Form|Annex|Schedule|Appendix|Exhibit)\s+[A-Z0-9]+[\.\d]*|'  # regulatory artifacts
        r'(?:Step|Phase|Year|Week|Month|Stage)\s+\d+|'                # sequenced steps
        r'(?:Template|Checklist|Playbook|Runbook)\b|'                 # operational docs
        r'(?:pip|npm|brew|cargo|apt|mise|nvm)\s+install|'             # install commands
        r'(?:v|version)\s*\d+[\.\d]+\b'                               # version numbers
        r')',
        impl_text
    )
    r['E30_artifact_specificity'] = len(artifacts) >= 3

    # E31: Recommendation validation — output shows evidence of validating its recommendation
    # (testing code, computing an example, checking a registry, citing precedent/case study/production use)
    validation_markers = re.findall(
        r'(?i)((?:tested|confirmed|verified|validated|computed|calculated|measured|benchmarked|checked|demonstrated).{0,60}'
        r'(?:successfully|works|passes|started|running|output|result|returns|shows|yields|produces|gives)|'
        r'(?:precedent|case study|real[\s-]world|in practice|deployed at|used by|in production|production[\s-]ready)\s|'
        r'(?:example|calculation|computation):\s|'
        r'(?:\d+\+?\s+)?(?:customer|client|user|company|enterprise)s?\s+(?:use|using|report|adopted|rely))',
        content
    )
    r['E31_recommendation_validated'] = len(validation_markers) >= 1

    # E32: Sensitivity analysis — recommendation stress-tested against assumptions
    sensitivity_markers = re.findall(
        r'(?i)((?:if|when|should)\s+.{0,30}(?:assumption|premise).{0,30}(?:wrong|incorrect|change|break|fail|invalid)|'
        r'sensiti(?:vity|ve)\s+analysis|'
        r'recommendation\s+(?:changes?|breaks?|holds?)\s+(?:if|when)|'
        r'(?:robust|resilient|brittle)\s+(?:to|against|under))',
        content
    )
    r['E32_sensitivity_analysis'] = len(sensitivity_markers) >= 1

    # E33: Source credibility — at least 1 explicit primary-source label
    credibility_markers = re.findall(
        r'(?i)(primary source|first-party|official doc(?:umentation|s)?|'
        r'peer[\s-]reviewed|registry\s+(?:data|entry|record)|'
        r'vendor[\s-](?:provided|supplied|originated|documentation)|'
        r'secondary source|third[\s-]party)',
        content
    )
    r['E33_source_credibility_labeled'] = len(credibility_markers) >= 1

    # E34: Imprecision reporting — sample sizes, confidence intervals, or margins of error
    precision_markers = re.findall(
        r'(?i)(n\s*=\s*[\d,]+|sample\s+(?:size|of)\s+[\d,]+|'
        r'confidence\s+interval|margin\s+of\s+error|±\s*[\d.]+|'
        r'standard\s+deviation|std\.?\s*dev|p\s*[<>=]\s*0?\.\d+|'
        r'\d+\s*%\s*CI\b)',
        content
    )
    r['E34_imprecision_reported'] = len(precision_markers) >= 1

    # E35: Scope boundaries — explicit out-of-scope statement
    scope_markers = re.findall(
        r'(?i)(out[\s-]of[\s-]scope|(?:does|do)\s+not\s+(?:cover|address|evaluate|consider)|'
        r'beyond\s+(?:the\s+)?scope|excluded?\s+from\s+(?:this\s+)?analysis|'
        r'not\s+(?:included|covered)\s+(?:in|here)|scope\s+(?:of|for)\s+this)',
        content
    )
    r['E35_scope_boundaries'] = len(scope_markers) >= 1

    # ═══ Report ═══
    # Filter out None (skipped) evals
    active = {k: v for k, v in r.items() if v is not None}
    score = sum(active.values())
    total = len(active)

    print(f'\n{"─"*50}')
    for tier_name, prefix_list in [
        ('TIER 0 (structural)', ('E1_','E2_','E3_','E4_','E5_','E6_','E7_','E8_')),
        ('TIER 1 (verifiable)', ('E9_','E10_','E11_')),
        ('TIER 2 (quality)',    ('E12_','E13_','E14_')),
        ('TIER 3 (rigor)',      ('E15_','E16_')),
        ('TIER 4 (ground truth)', ('E17_','E18_','E19_','E20_')),
        ('TIER 5 (industrial)', ('E21_','E22_','E23_')),
        ('TIER 6 (convergence)', ('E24_','E25_','E26_')),
        ('TIER 7 (multi-framework)', ('E27_','E28_','E29_')),
        ('TIER 8 (actionability)', ('E30_','E31_','E32_','E33_','E34_','E35_')),
    ]:
        tier_evals = {k:v for k,v in r.items() if any(k.startswith(p) for p in prefix_list) and v is not None}
        if not tier_evals:
            continue
        tier_score = sum(tier_evals.values())
        tier_total = len(tier_evals)
        print(f'\n  {tier_name}: {tier_score}/{tier_total}')
        for k, v in tier_evals.items():
            print(f'    {"PASS" if v else "FAIL"} {k}')

    skipped = {k: v for k, v in r.items() if v is None}
    if skipped:
        print(f'\n  SKIPPED (run with --verify-urls): {", ".join(skipped.keys())}')

    print(f'\n{"─"*50}')
    print(f'  TOTAL: {score}/{total}')
    print(f'  URLs: {len(urls)} | Tables: {len(tables)} | Code: {len(code_blocks)} | Words: {words}')
    print(f'{"─"*50}\n')
    return score, total, r

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 grade.py <output.md> [--flawed-premise] [--verify-urls]")
        sys.exit(1)
    flawed = '--flawed-premise' in sys.argv
    verify = '--verify-urls' in sys.argv
    path = [a for a in sys.argv[1:] if not a.startswith('--')][0]
    grade(path, has_flawed_premise=flawed, verify_urls=verify)
