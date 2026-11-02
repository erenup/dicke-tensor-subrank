#!/usr/bin/env python3
"""Build source indexes and check the paper-to-Lean and exact-check mapping.

The paper inventory (title, numbered sections and numbered results), the Lean
declarations, the exact-check functions and the generated tables in
by-section.md must agree with mapping.json. Any mismatch fails closed.
"""

import ast
import copy
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS = {
    "theorem": "Theorem", "proposition": "Proposition", "lemma": "Lemma",
    "corollary": "Corollary", "definition": "Definition", "remark": "Remark",
}
COVERAGES = {"paper_only", "partial_lean", "finite_checks_only"}
BY_SECTION = "paper-lean-mapping/by-section.md"


def need(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def reject_number(value):
    raise SystemExit("FAIL: unsupported JSON number")


def parse_json(data):
    return json.loads(data, object_pairs_hook=unique_object,
                      parse_float=reject_number, parse_constant=reject_number)


def keys(value, expected, label):
    need(isinstance(value, dict) and set(value) == set(expected), label + " fields")


def string(value, label):
    need(isinstance(value, str) and value.strip(), label + " text")


def strings(values, label):
    need(isinstance(values, list) and all(isinstance(x, str) for x in values), label)
    need(len(values) == len(set(values)), "duplicate " + label)
    for value in values:
        string(value, label)


def safe_path(name):
    need(isinstance(name, str) and name and "\\" not in name, "source path")
    p = Path(name)
    need(not p.is_absolute() and ".." not in p.parts and str(p) == name, "source path")
    return p


def read_inputs():
    names = {"lean/audit/TARGETS.json", "paper-lean-mapping/mapping.json", BY_SECTION}
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / "paper").rglob("*.tex"))
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / "lean/TR28").rglob("*.lean"))
    names.update({"verification/core/verification/check_entropy.py", "verification/core/verification/check_hashing.py"})
    result = {}
    for name in sorted(names):
        p = ROOT / safe_path(name)
        need(p.is_file() and not p.is_symlink(), "missing or linked source: " + name)
        need(p.stat().st_size <= 4000000, "oversized source: " + name)
        result[name] = p.read_text(encoding="utf-8")
    return result


def tex_uncomment(line):
    for i, char in enumerate(line):
        if char == "%":
            j = i - 1
            while j >= 0 and line[j] == "\\":
                j -= 1
            if (i - j - 1) % 2 == 0:
                return line[:i]
    return line


def paper_index(sources, entry):
    """Read the explicit section counter and shared theorem counter in TeX order."""
    seen = set()

    def expand(name):
        safe_path(name)
        need(name.startswith("paper/") and name.endswith(".tex"), "paper input path")
        need(name in sources, "missing paper input: " + name)
        need(name not in seen, "repeated paper input: " + name)
        seen.add(name)
        output = []
        for line in sources[name].splitlines():
            line = tex_uncomment(line)
            if re.search(r"\\(?:input|include)\b", line):
                match = re.fullmatch(r"\s*\\input\{([A-Za-z0-9_/-]+)\}\s*", line)
                need(match is not None, "unsupported paper inclusion")
                output.extend(expand("paper/" + match.group(1) + ".tex"))
            else:
                output.append((name, line))
        return output

    expanded = expand(entry)
    need(seen == {n for n in sources if n.startswith("paper/") and n.endswith(".tex")},
         "unreferenced paper source")
    text = "\n".join(line for _, line in expanded)
    declarations = re.findall(r"\\newtheorem(?:\*)?[^\n]*", text)
    expected = [r"\newtheorem{theorem}{Theorem}[section]"] + [
        r"\newtheorem{" + env + "}[theorem]{" + title + "}"
        for env, title in ENVIRONMENTS.items() if env != "theorem"]
    need(declarations == expected, "unsupported theorem counter declaration")
    need(not re.search(r"\\(?:setcounter|addtocounter|counterwithin|counterwithout|appendix)\b", text),
         "unsupported paper counter modification")
    titles = re.findall(r"\\title\{([^{}]*)\}", text)
    need(len(titles) == 1, "paper title declaration")
    pdf_titles = re.findall(r"pdftitle=\{([^{}]*)\}", text)
    need(len(pdf_titles) == 1, "paper PDF title declaration")
    token = re.compile(
        r"\\section(\*)?\{([^{}]+)\}|"
        r"\\(begin|end)\{([^{}]+)\}(?:\[([^\[\]]*)\])?|\\label\{([^{}]+)\}")
    sections, results, labels, stack = [], [], {}, []
    section = counter = 0
    active = None
    for source, line in expanded:
        for match in token.finditer(line):
            starred, title, command, env, name, label = match.groups()
            if title is not None:
                need(active is None, "section inside numbered result")
                if not starred:
                    section += 1
                    counter = 0
                    sections.append({"number": section, "title": title, "source": source})
            elif command == "begin":
                stack.append(env)
                if env in ENVIRONMENTS:
                    need(active is None and section > 0, "nested or unsectioned numbered result")
                    counter += 1
                    active = {"environment": env, "number": str(section) + "." + str(counter),
                              "section": section, "source": source, "labels": [], "depth": len(stack),
                              "name": name}
                need(env.rstrip("*") not in ENVIRONMENTS or env in ENVIRONMENTS,
                     "unsupported unnumbered result environment")
            elif command == "end":
                need(stack and stack[-1] == env, "unbalanced paper environment")
                if active is not None and len(stack) == active["depth"]:
                    need(len(active["labels"]) == 1, "numbered result requires one direct label")
                    results.append({k: active[k] for k in
                                    ("environment", "number", "section", "source", "name")} |
                                   {"label": active["labels"][0]})
                    active = None
                stack.pop()
            else:
                need(label not in labels, "duplicate paper label")
                labels[label] = {"section": section, "source": source}
                if active is not None and len(stack) == active["depth"]:
                    active["labels"].append(label)
    need(not stack and active is None, "unclosed paper environment")
    return {"title": titles[0], "pdf_title": pdf_titles[0]}, sections, results, labels


def lean_without_comments(text):
    """Mask strings and nested comments before looking for declarations."""
    out = []
    i = depth = 0
    quoted = False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                depth += 1
                out.extend("  ")
                i += 2
            elif text.startswith("-/", i):
                depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif quoted:
            if text[i] == "\\":
                need(i + 1 < len(text), "unterminated Lean string")
                out.extend("  ")
                i += 2
            else:
                quoted = text[i] != '"'
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif text.startswith("/-", i):
            depth = 1
            out.extend("  ")
            i += 2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out.extend(" " * (end - i))
            i = end
        elif text[i] == '"':
            quoted = True
            out.append(" ")
            i += 1
        else:
            out.append(text[i])
            i += 1
    need(not depth and not quoted, "unterminated Lean comment or string")
    return "".join(out)


def lean_index(sources):
    declarations = {}
    for source, text in sources.items():
        if not source.endswith(".lean"):
            continue
        namespaces = []
        for line in lean_without_comments(text).splitlines():
            match = re.match(r"\s*namespace\s+([A-Za-z_][A-Za-z0-9_.]*)\s*$", line)
            if match:
                namespaces.append(match.group(1))
                continue
            match = re.match(r"\s*end(?:\s+([A-Za-z_][A-Za-z0-9_.]*))?\s*$", line)
            if match:
                need(namespaces and (match.group(1) is None or match.group(1) == namespaces[-1]),
                     "unsupported Lean namespace end")
                namespaces.pop()
                continue
            match = re.match(r"\s*(?:noncomputable\s+)?(def|theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_']*)\b(.*)", line)
            if match:
                kind, name, header = match.groups()
                name = ".".join(namespaces + [name])
                need(name not in declarations, "duplicate Lean declaration")
                declarations[name] = {"source": source, "kind": kind, "header": header}
        need(not namespaces, "unclosed Lean namespace")
    return declarations


def validate(mapping, sources):
    keys(mapping, {"schema_version", "paper", "paper_title", "scope", "sections", "lean_targets",
                   "exact_checks", "numbered_results", "supporting_steps", "aggregate"}, "mapping")
    need(type(mapping["schema_version"]) is int and mapping["schema_version"] == 2, "schema version")
    need(mapping["paper"] == "paper/main.tex", "paper entry point")
    string(mapping["scope"], "mapping scope")
    string(mapping["paper_title"], "paper title")
    front, sections, inventory, labels = paper_index(sources, mapping["paper"])
    need(front["title"] == mapping["paper_title"], "paper title mismatch")
    need(front["pdf_title"] == mapping["paper_title"], "PDF title metadata mismatch")
    need(isinstance(mapping["sections"], list), "sections list")
    for item in mapping["sections"]:
        keys(item, {"number", "title", "source"}, "section")
        need(type(item["number"]) is int, "section number")
        string(item["title"], "section title")
        string(item["source"], "section source")
        need("|" not in item["title"], "section title text")
    need(mapping["sections"] == sections, "section inventory mismatch")
    declarations = lean_index(sources)
    registry = parse_json(sources["lean/audit/TARGETS.json"])
    targets = {}
    need(isinstance(mapping["lean_targets"], list), "Lean targets list")
    for item in mapping["lean_targets"]:
        keys(item, {"id", "declaration", "source", "proposition", "proposition_source", "scope"}, "Lean target")
        for key in item:
            string(item[key], "Lean target " + key)
        name = item["id"]
        need(name not in targets, "duplicate Lean target")
        targets[name] = item
        proof = declarations.get(item["declaration"])
        prop = declarations.get(item["proposition"])
        need(proof is not None and proof["source"] == item["source"] and proof["kind"] == "theorem",
             "missing mapped Lean theorem")
        need(prop is not None and prop["source"] == item["proposition_source"] and prop["kind"] == "def",
             "missing mapped Lean proposition")
        need(registry.get(item["proposition"]) == item["declaration"], "Lean target registry mismatch")
        need(re.fullmatch(r"\s*:\s*" + re.escape(item["proposition"].split(".")[-1]) +
                          r"\s*:=.*", proof["header"]) is not None, "mapped Lean theorem type")
    aggregate = mapping["aggregate"]
    keys(aggregate, {"declaration", "proposition", "source", "scope"}, "aggregate")
    need(aggregate["declaration"] == "TR28.core_theorems" and
         aggregate["proposition"] == "TR28.CoreTheorems", "aggregate target")
    aggregate_proof = declarations.get(aggregate["declaration"], {})
    aggregate_prop = declarations.get(aggregate["proposition"], {})
    need(aggregate_proof.get("source") == aggregate["source"] and
         aggregate_proof.get("kind") == "theorem",
         "missing aggregate Lean theorem")
    need(aggregate_prop.get("source") == "lean/TR28/Statement.lean" and
         aggregate_prop.get("kind") == "def", "missing aggregate Lean proposition")
    need(re.fullmatch(r"\s*:\s*CoreTheorems\s*:=.*", aggregate_proof["header"]) is not None,
         "aggregate Lean theorem type")
    need(registry == {x["proposition"]: x["declaration"] for x in targets.values()} |
         {aggregate["proposition"]: aggregate["declaration"]}, "unmapped Lean target registry entry")
    string(aggregate["scope"], "aggregate scope")
    checks = {}
    need(isinstance(mapping["exact_checks"], list), "exact checks list")
    for item in mapping["exact_checks"]:
        keys(item, {"id", "source", "function", "scope", "limitation"}, "exact check")
        for key in item:
            string(item[key], "exact check " + key)
        need(item["id"] not in checks, "duplicate exact check")
        checks[item["id"]] = item
        need(item["source"] in sources and item["source"].startswith("verification/core/verification/"),
             "missing exact-check source")
        tree = ast.parse(sources[item["source"]], filename=item["source"])
        functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
        need(functions.count(item["function"]) == 1, "missing mapped exact-check function")
    rows = mapping["numbered_results"]
    need(isinstance(rows, list), "numbered results list")
    row_index = []
    used_targets, used_checks, used_labels = set(), set(), set()

    def references(row):
        need(type(row["section"]) is int and row["section"] > 0, "paper section number")
        string(row["label"], "paper label")
        string(row["source"], "paper source")
        strings(row["lean_targets"], "Lean references")
        strings(row["exact_checks"], "exact-check references")
        need(set(row["lean_targets"]) <= set(targets), "unknown Lean reference")
        need(set(row["exact_checks"]) <= set(checks), "unknown exact-check reference")
        need(row["label"] in labels, "missing mapped paper label")
        need(labels[row["label"]] == {"section": row["section"], "source": row["source"]},
             "paper anchor location")
        need(row["label"] not in used_labels, "duplicate mapped paper label")
        used_labels.add(row["label"])
        used_targets.update(row["lean_targets"])
        used_checks.update(row["exact_checks"])
        string(row["covered"], "covered scope")
        string(row["paper_only"], "paper-only scope")

    for row in rows:
        keys(row, {"label", "environment", "number", "section", "source", "title", "coverage",
                   "lean_targets", "exact_checks", "covered", "paper_only"}, "numbered result")
        references(row)
        string(row["environment"], "result environment")
        string(row["number"], "result number")
        string(row["title"], "result title")
        need(row["coverage"] in COVERAGES, "unsupported coverage claim")
        need((row["coverage"] == "partial_lean") == bool(row["lean_targets"]), "Lean coverage classification")
        need(row["coverage"] != "finite_checks_only" or bool(row["exact_checks"]), "empty finite coverage")
        need(row["coverage"] != "paper_only" or not row["exact_checks"], "paper-only classification")
        need("|" not in row["title"], "result title text")
        row_index.append({k: row[k] for k in ("label", "environment", "number", "section", "source")})
    need(row_index == [{k: v for k, v in x.items() if k != "name"} for x in inventory],
         "numbered result inventory mismatch")
    for row, item in zip(rows, inventory):
        need(item["name"] is None or row["title"] == item["name"], "result title differs from paper")
    need(isinstance(mapping["supporting_steps"], list), "supporting steps list")
    for row in mapping["supporting_steps"]:
        keys(row, {"label", "section", "source", "title", "lean_targets", "exact_checks", "covered", "paper_only"},
             "supporting step")
        string(row["title"], "supporting title")
        need("|" not in row["title"], "supporting title text")
        references(row)
    need(used_targets == set(targets), "unreferenced Lean target")
    need(used_checks == set(checks), "unreferenced exact check")
    check_by_section(mapping, targets, checks, sources[BY_SECTION])
    return len(sections), len(inventory), len(targets), len(checks), len(mapping["supporting_steps"])


def render_tables(mapping, targets, checks):
    """Render the two tables of by-section.md from the validated map."""

    def lean(row):
        return ", ".join("`" + targets[x]["declaration"] + "`" for x in row["lean_targets"])

    def exact(row):
        return ", ".join("`" + checks[x]["source"].split("/")[-1] + ":" + checks[x]["function"] + "`"
                         for x in row["exact_checks"])

    lines = ["| Paper result | Label | Coverage |", "| --- | --- | --- |"]
    for row in mapping["numbered_results"]:
        if row["coverage"] == "paper_only":
            coverage = "Paper only"
        elif row["coverage"] == "partial_lean":
            coverage = "Partial Lean coverage: " + lean(row)
            if row["exact_checks"]:
                coverage += "; exact finite checks: " + exact(row)
        else:
            coverage = "Paper proof; finite exact checks: " + exact(row)
        lines.append("| " + ENVIRONMENTS[row["environment"]] + " " + row["number"] + ": " + row["title"] +
                     " | `" + row["label"] + "` | " + coverage + " |")
    results = "\n".join(lines)
    lines = ["| Supporting anchor | Section | Lean targets | Exact checks |", "| --- | ---: | --- | --- |"]
    for row in mapping["supporting_steps"]:
        lines.append("| `" + row["label"] + "`: " + row["title"] + " | " + str(row["section"]) + " | " +
                     (lean(row) or "None") + " | " + (exact(row) or "None") + " |")
    return results, "\n".join(lines)


def check_by_section(mapping, targets, checks, text):
    need(text.endswith("\n") and "\r" not in text, "by-section text format")
    padded = "\n" + text
    for table in render_tables(mapping, targets, checks):
        need(padded.count("\n" + table + "\n") == 1, "by-section result table mismatch")
    headings = [line for line in text.splitlines() if line.startswith("## ")]
    expected = ["## " + str(x["number"]) + ". " + x["title"] for x in mapping["sections"]]
    need(headings == expected, "by-section headings mismatch")


def negative_controls(mapping, sources):
    cases = []

    def changed(label, mutate, expected):
        bad_mapping, bad_sources = copy.deepcopy(mapping), dict(sources)
        mutate(bad_mapping, bad_sources)
        need(bad_mapping != mapping or bad_sources != sources, "inert negative control: " + label)
        cases.append((label, bad_mapping, bad_sources, expected))

    changed("missing paper label", lambda m, s: m["numbered_results"][0].update(label="thm:absent"),
            "missing mapped paper label")
    changed("omitted numbered result", lambda m, s: m["numbered_results"].pop(),
            "numbered result inventory mismatch")
    changed("duplicate numbered result", lambda m, s: m["numbered_results"].append(m["numbered_results"][0]),
            "duplicate mapped paper label")
    changed("wrong result number", lambda m, s: m["numbered_results"][0].update(number="1.2"),
            "numbered result inventory mismatch")
    changed("missing Lean theorem", lambda m, s: s.update({"lean/TR28/Density.lean":
            s["lean/TR28/Density.lean"].replace("theorem invariant_supermodular_density", "theorem absent_density", 1)}),
            "missing mapped Lean theorem")
    changed("comment-only Lean theorem", lambda m, s: s.update({"lean/TR28/Density.lean":
            "/- theorem invariant_supermodular_density : InvariantSupermodularDensity := by -/\n" +
            s["lean/TR28/Density.lean"].replace("theorem invariant_supermodular_density", "theorem absent_density", 1)}),
            "missing mapped Lean theorem")
    changed("wrong Lean theorem type", lambda m, s: s.update({"lean/TR28/Density.lean":
            s["lean/TR28/Density.lean"].replace(": InvariantSupermodularDensity :=", ": True :=", 1)}),
            "mapped Lean theorem type")
    changed("missing exact function", lambda m, s: m["exact_checks"][0].update(function="absent_check"),
            "missing mapped exact-check function")
    changed("unlabelled numbered result", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace(r"\end{document}", r"\begin{lemma}X\end{lemma}\end{document}")}),
            "numbered result requires one direct label")
    changed("unmapped numbered result", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace(r"\end{document}", r"\begin{lemma}\label{lem:unmapped}X\end{lemma}\end{document}")}),
            "numbered result inventory mismatch")
    changed("full formalization claim", lambda m, s: m["numbered_results"][0].update(coverage="fully_formalized"),
            "unsupported coverage claim")
    changed("unknown Lean reference", lambda m, s: m["numbered_results"][0]["lean_targets"].append("absent"),
            "unknown Lean reference")
    changed("changed theorem counter", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace(r"\newtheorem{theorem}{Theorem}[section]", r"\newtheorem{theorem}{Theorem}")}),
            "unsupported theorem counter declaration")
    old_title = "The asymptotic subrank of every Dicke tensor"
    new_title = mapping["paper_title"]
    changed("stale paper title", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace(r"\title{" + new_title + "}", r"\title{" + old_title + "}", 1)}),
            "paper title mismatch")
    changed("stale PDF title", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace("pdftitle={" + new_title + "}", "pdftitle={" + old_title + "}", 1)}),
            "PDF title metadata mismatch")
    changed("old section title", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace(r"\section{The main theorem}",
                                        r"\section{From Dicke tensors to an entropy-determined growth rate}", 1)}),
            "section inventory mismatch")
    changed("unmapped section", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace(r"\end{document}", r"\section{Discussion}\end{document}")}),
            "section inventory mismatch")
    changed("reinstated old input", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace(r"\input{sections/history}",
                                        r"\input{sections/history}" + "\n" + r"\input{sections/overview}", 1)}),
            "missing paper input: paper/sections/overview.tex")
    changed("omitted section input", lambda m, s: s.update({"paper/main.tex":
            s["paper/main.tex"].replace(r"\input{sections/upper}", "", 1)}),
            "unreferenced paper source")
    changed("renamed paper result", lambda m, s: m["numbered_results"][2].update(title="Submodularity"),
            "result title differs from paper")
    changed("stale result table", lambda m, s: s.update({BY_SECTION:
            s[BY_SECTION].replace("| Partial Lean coverage: ", "| Paper only: ", 1)}),
            "by-section result table mismatch")
    changed("stale section heading", lambda m, s: s.update({BY_SECTION:
            s[BY_SECTION].replace("## 1. The main theorem\n",
                                  "## 1. From Dicke tensors to an entropy-determined growth rate\n", 1)}),
            "by-section headings mismatch")
    for label, bad_mapping, bad_sources, expected in cases:
        try:
            validate(bad_mapping, bad_sources)
        except SystemExit as error:
            need(str(error) == "FAIL: " + expected, "wrong negative-control rejection: " + label)
        else:
            raise SystemExit("FAIL: accepted negative control: " + label)
    try:
        parse_json('{"schema_version":1,"schema_version":1}')
    except SystemExit as error:
        need(str(error) == "FAIL: duplicate JSON key", "wrong duplicate-key rejection")
    else:
        raise SystemExit("FAIL: duplicate JSON key accepted")
    return len(cases) + 1


def main():
    need(len(sys.argv) == 1, "this command takes no arguments")
    sources = read_inputs()
    mapping = parse_json(sources["paper-lean-mapping/mapping.json"])
    sections, results, targets, checks, supporting = validate(mapping, sources)
    controls = negative_controls(mapping, sources)
    need(read_inputs() == sources, "sources changed during check")
    print("PASS: paper title, " + str(sections) + " numbered section titles and " + str(results) +
          " numbered results in TeX order")
    print("PASS: " + str(targets) + " finite Lean targets and their aggregate declaration")
    print("PASS: " + str(checks) + " exact-check links and " + str(supporting) + " supporting paper anchors")
    print("PASS: by-section tables and section headings agree with the map")
    print("PASS: " + str(controls) + " mapping negative controls")
    print("RESULT: PASS mapping structure; mathematical coverage is stated per entry")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, SyntaxError, UnicodeError) as error:
        raise SystemExit("FAIL: mapping input: " + type(error).__name__)
