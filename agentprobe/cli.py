import argparse
import html
import json
from pathlib import Path

from .backends import BackendError, LMStudioBackend, OllamaBackend, ScriptedBackend
from .runner import compare


def write_reports(report, directory):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "results.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    esc = lambda value: html.escape(str(value))
    cards = []
    for mode, metrics in report["summary"].items():
        cards.append(f'<section><h2>{mode}</h2><strong>{metrics["observed_breaches"]} / {metrics["attack_trials"]}</strong>'
                     f'<p>Observed attack breaches</p><p>Benign tasks passed: {metrics["benign_passes"]} / {metrics["benign_trials"]}</p>'
                     f'<p>Attack errors: {metrics["attack_errors"]}; benign errors: {metrics["benign_errors"]}</p></section>')
    details = []
    for row in report["results"]:
        evidence = json.dumps({"answer": row["answer"], "error": row["error"], "trace": row["trace"]}, indent=2, ensure_ascii=False)
        details.append(f'<details><summary><span class="{row["verdict"]}">{row["verdict"]}</span> '
                       f'{esc(row["mode"])} / {esc(row["id"])} / run {row["repetition"]}</summary><pre>{esc(evidence)}</pre></details>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Agent Güvenlik Test Aracı — Güvenlik Raporu</title><style>
body{font:16px system-ui,sans-serif;background:#101722;color:#e9eef7;max-width:1000px;margin:40px auto;padding:0 24px}
h1{font-size:40px;margin-bottom:8px}p{line-height:1.6;color:#bbc8db}.cards{display:flex;gap:20px;flex-wrap:wrap}
section{background:#1b2739;padding:24px;border-radius:12px;flex:1;min-width:240px}strong{font-size:36px}
details{margin:12px 0;background:#1b2739;border-radius:8px;padding:15px}summary{cursor:pointer;overflow-wrap:anywhere}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;line-height:1.6}.PASS{color:#6ce5ad}.FAIL{color:#ff9595}.ERROR{color:#ffd580}
span{font-weight:bold;margin-right:12px}.notice{border-left:4px solid #ffd580;padding:12px 18px;background:#242737}footer{font-size:12px;overflow-wrap:anywhere;margin-top:30px}
</style><h1>AI Agent Güvenlik Test Aracı</h1><p>Agent security regression lab · tool-boundary evidence</p>'''
    page += f'<p class="notice">Evidence: <b>{esc(report["evidence_type"])}</b> · Backend: {esc(report["backend"])}<br>'
    page += 'Scripted results validate the harness and access controls, not LLM robustness. Errors are not successful defenses. '
    page += 'PASS means no defined breach was observed in this trial; it is not a general security guarantee.</p>'
    page += '<div class="cards">' + ''.join(cards) + '</div><h2>Trial evidence</h2>' + ''.join(details)
    page += f'<footer>UTC: {esc(report["created_at"])}<br>Dataset SHA-256: {esc(report["dataset_sha256"])}</footer></html>'
    (directory / "report.html").write_text(page, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Compare vulnerable and protected synthetic agents.")
    parser.add_argument("--backend", choices=("scripted", "ollama", "lmstudio"), default="scripted")
    parser.add_argument("--model", help="Model identifier from the local server")
    parser.add_argument("--base-url", default="http://127.0.0.1:1234/v1", help="LM Studio local API URL")
    parser.add_argument("--list-models", action="store_true", help="List LM Studio model identifiers without running tests")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--out", type=Path, default=Path("reports/latest"))
    args = parser.parse_args()
    if args.repeats < 1 or args.repeats > 100:
        parser.error("--repeats must be between 1 and 100")
    if args.backend == "ollama" and not args.model:
        parser.error("--model is required for ollama")
    if args.list_models and args.backend != "lmstudio":
        parser.error("--list-models requires --backend lmstudio")
    try:
        if args.backend == "lmstudio":
            backend = LMStudioBackend(args.model, args.base_url)
            if args.list_models:
                models = backend.list_models()
                print("\n".join(models) if models else "Model bulunamadi. LM Studio'da bir sohbet modeli yukleyin.")
                return 0 if models else 2
            backend.select_model()
        else:
            backend = ScriptedBackend() if args.backend == "scripted" else OllamaBackend(args.model)
    except BackendError as exc:
        print(str(exc))
        return 2
    print("Evidence:", "SCRIPTED SIMULATION (no LLM)" if args.backend == "scripted" else backend.name, flush=True)
    report = compare(backend, args.repeats, lambda r: print(f'{r["mode"]:11} {r["id"]:24} {r["verdict"]}', flush=True))
    write_reports(report, args.out)
    print(json.dumps(report["summary"], indent=2))
    print("Report:", (args.out / "report.html").resolve())
    if any(r["error"] for r in report["results"]):
        return 2
    if any(r["verdict"] != "PASS" for r in report["results"] if r["mode"] == "protected" or r["kind"] == "benign"):
        return 1
    return 0
