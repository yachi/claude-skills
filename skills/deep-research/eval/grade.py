#!/usr/bin/env python3
"""Grade /dr skill outputs — 23 binary evals across 6 tiers. Usage: python3 grade.py <output.md> [--flawed-premise] [--verify-urls]"""

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

    rec = re.search(r'(?i)## Recommendation[\s\S]*?(?=\n##|\Z)', content)
    if rec:
        conds = re.findall(r'(?i)(?:if|when|unless|condition|change|switch|pivot|reconsider|revisit)', rec.group())
        r['E13_change_conditions'] = len(conds) >= 2
    else:
        r['E13_change_conditions'] = False

    words = len(content.split())
    r['E14_word_count_ok'] = 1500 <= words <= 5000

    # ═══ TIER 3: Rigor ═══

    findings = re.search(r'(?i)## Key Findings[\s\S]*?(?=\n##|\Z)', content)
    r['E15_findings_verified'] = '[unverified]' not in (findings.group().lower() if findings else '')

    sources = re.search(r'(?i)## Sources[\s\S]*?(?=\n##|\Z)', content)
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

    # E19: Executive summary is self-contained (has answer + confidence in first 3 sentences)
    exec_summary = re.search(r'(?i)## Executive Summary\s*\n([\s\S]*?)(?=\n##|\Z)', content)
    if exec_summary:
        summary_text = exec_summary.group(1).strip()
        has_answer = len(summary_text) > 50  # not trivially short
        has_conf = bool(re.search(r'\d+%', summary_text))
        r['E19_exec_summary_complete'] = has_answer and has_conf
    else:
        r['E19_exec_summary_complete'] = False

    # E20: Alternatives section exists and has 2+ options with data
    alts = re.search(r'(?i)## Alternatives[\s\S]*?(?=\n##|\Z)', content)
    if alts:
        alt_text = alts.group()
        alt_options = re.findall(r'(?:###\s|\d+\.\s\*\*|\*\*\d+\.)', alt_text)
        has_data = bool(re.search(r'\d+[%$KMB]|\$[\d,]+|EUR', alt_text))
        r['E20_alternatives_with_data'] = len(alt_options) >= 2 and has_data
    else:
        r['E20_alternatives_with_data'] = False

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
