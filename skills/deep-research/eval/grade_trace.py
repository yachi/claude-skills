#!/usr/bin/env python3
"""Grade /dr v1.1.0 TRACE behaviors (1,5,8) on an agent tool-call transcript (.jsonl).

The transcript is one JSON object per line in Claude Code shape:
  {"message": {"content": [{"type":"tool_use","name":"Read","input":{...}}, ...]}}
Assistant prose lines carry {"type":"text","text":"..."} entries. Each grader
enforces one SKILL.md behavior and is a mutation test; the docstring names the
SKILL.md line(s) it enforces.

Usage: python3 grade_trace.py <transcript.jsonl>
Prints one `B<n> PASS|FAIL — reason` line per behavior. Exit 0.
"""

import json, re, sys

LOCAL_TOOLS = {'read', 'grep', 'glob', 'ls', 'notebookread'}
WEB_TOOLS_RE = re.compile(r'(?i)(websearch|webfetch|firecrawl|web_search|web_fetch|'
                          r'parallel_search|fetch_url|browser)')
NETWORK_CMD_RE = re.compile(r'(?i)\b(curl|wget|http|https)://|\b(curl|wget)\b')

def _events(path):
    """Yield (kind, name, input, text) per tool_use / text block, in transcript order."""
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            content = (obj.get('message') or {}).get('content') or obj.get('content') or []
            if isinstance(content, dict):
                content = [content]
            for c in content:
                if not isinstance(c, dict):
                    continue
                t = c.get('type')
                if t == 'tool_use':
                    out.append(('tool', c.get('name', ''), c.get('input') or {}, ''))
                elif t == 'text':
                    out.append(('text', '', {}, c.get('text', '')))
    return out

def _is_local_tool(name, inp):
    n = name.lower()
    if n in LOCAL_TOOLS:
        return True
    if n == 'bash':
        cmd = str(inp.get('command', ''))
        return not NETWORK_CMD_RE.search(cmd)
    return False

def _is_web_tool(name):
    return bool(WEB_TOOLS_RE.search(name))

# ── B1: first-party evidence first ───────────────────────────────────────────

def b1_first_party_first(events):
    """SKILL.md Phase 1.5 'First-party evidence first — Before any web search, exhaust
    the evidence the system under study already holds': a local Read/Grep/Bash-on-repo
    tool call must occur BEFORE the first WebSearch/WebFetch."""
    first_local = first_web = None
    for i, (kind, name, inp, _) in enumerate(events):
        if kind != 'tool':
            continue
        if first_web is None and _is_web_tool(name):
            first_web = i
        if first_local is None and _is_local_tool(name, inp):
            first_local = i
    if first_local is None:
        return False, 'no local first-party tool call in transcript'
    if first_web is None:
        return True, f'local tool at #{first_local}, no web call made'
    ok = first_local < first_web
    return ok, f'first local #{first_local} {"<" if ok else ">="} first web #{first_web}'

# ── B5: two-premise / intent check ───────────────────────────────────────────

_INTENT_TEXT_RE = re.compile(
    r'(?i)(intent\s+premise|intent\s+mismatch|'
    r'you\s+asked\s+for[^.\n]{0,80}\bbut\b[^.\n]{0,80}(?:evidence|points|suggests?|different)|'
    r'the\s+approach\s+you\s+(?:expect|asked)[^.\n]{0,60}differs|'
    r'before\s+(?:i\s+)?(?:invest|commit|proceed)[^.\n]{0,60}(?:confirm|which)|'
    r'differs\s+from\s+(?:your|the)\s+stated\s+(?:intent|approach|scope))')

def b5_intent_check(events):
    """SKILL.md Phase 1 'Premise validation ... (b) Intent premise': either an
    AskUserQuestion / one-line stop BEFORE deep research, or an explicit 'intent
    premise' statement flagging the obvious-approach vs stated-intent mismatch."""
    first_web = None
    asked_before_web = False
    for i, (kind, name, inp, text) in enumerate(events):
        if kind == 'tool' and _is_web_tool(name) and first_web is None:
            first_web = i
        if kind == 'tool' and name.lower() == 'askuserquestion':
            if first_web is None:
                asked_before_web = True
    intent_text = any(kind == 'text' and _INTENT_TEXT_RE.search(text) for kind, _, _, text in events)
    ok = asked_before_web or intent_text
    return ok, f'AskUserQuestion-before-web={asked_before_web}, intent-premise-statement={intent_text}'

# ── B8: durable output path ──────────────────────────────────────────────────

_EPHEMERAL_RE = re.compile(r'(?i)(^|/)(tmp|scratch|scratchpad)(/|$)|/private/tmp|/var/folders')
_DURABLE_PROPOSAL_RE = re.compile(
    r'(?i)(durable\s+path|save\s+(?:it|the\s+report)\s+to\s+[^\s]+\.(?:md|markdown)|'
    r'propos\w+\s+(?:a\s+)?(?:durable\s+)?path|under\s+the\s+project|'
    r'report\s+(?:will\s+be\s+)?(?:written|saved)\s+to\s+(?!/tmp|/private/tmp|/scratch))')

def b8_durable_output(events):
    """SKILL.md Phase 8 'Durable output path — Never leave the only copy in /tmp or
    scratch': the report Write targets a path NOT under /tmp or scratch, OR the agent
    proposes a durable path in text."""
    report_writes = []
    for kind, name, inp, _ in events:
        if kind == 'tool' and name.lower() in ('write', 'create'):
            fp = str(inp.get('file_path') or inp.get('path') or '')
            if fp.lower().endswith(('.md', '.markdown')):
                report_writes.append(fp)
    durable_write = any(not _EPHEMERAL_RE.search(fp) for fp in report_writes)
    durable_text = any(kind == 'text' and _DURABLE_PROPOSAL_RE.search(text)
                       for kind, _, _, text in events)
    ok = durable_write or durable_text
    if report_writes:
        return ok, f'report writes={report_writes}, durable-write={durable_write}, durable-proposal-text={durable_text}'
    return ok, f'no report Write; durable-proposal-text={durable_text}'

# ── driver ───────────────────────────────────────────────────────────────────

def grade(path):
    events = _events(path)
    rows = [
        ('B1', *b1_first_party_first(events)),
        ('B5', *b5_intent_check(events)),
        ('B8', *b8_durable_output(events)),
    ]
    for name, ok, reason in rows:
        print(f'{name} {"PASS" if ok else "FAIL"} — {reason}')
    return rows

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 grade_trace.py <transcript.jsonl>')
        sys.exit(1)
    grade(sys.argv[1])
