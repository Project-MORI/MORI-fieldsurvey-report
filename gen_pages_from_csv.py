#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_pages_from_csv.py (external templates; RELATIVE LINKS)
- CSVからMkDocsページを一括生成（外部テンプレート使用）
- すべて相対リンクで出力（トップ→調査名、調査名→ID）
- 作成物:
  * docs/surveys/<title>/<survey_id>.md
  * docs/surveys/<title>/index.md
  * docs/index.md の "調査名の一覧" 自動更新（マーカー間のみ）
  * docs/assets/survey_links.json （相対パスを保存）

CSV 必須列: survey_id, title, survey_date, region, lat, lon
任意列   : members, route, jjfast, deter, firms, prodes, note, state など
テンプレ : templates/template_id.md, templates/template_name.md
"""
import argparse
import csv
import io
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SURVEYS = DOCS / "surveys"
ASSETS = DOCS / "assets"
TEMPLATES_DIR = ROOT / "templates"

LINKS_JSON = ASSETS / "survey_links.json"
INDEX_MD = DOCS / "index.md"
TOP_MARK_BEGIN = "<!-- BEGIN: AUTO_SURVEY_LIST -->"
TOP_MARK_END   = "<!-- END: AUTO_SURVEY_LIST -->"

# 必須テンプレ
TPL_ID_PATH   = TEMPLATES_DIR / "template_id.md"
TPL_NAME_PATH = TEMPLATES_DIR / "template_name.md"

# -------------------- 基本I/O --------------------

def read_csv(path: Path):
    with io.open(path, "r", encoding="utf-8-sig") as fp:
        reader = csv.DictReader(fp)
        rows = []
        for row in reader:
            norm = {}
            for k, v in row.items():
                key = (k or "").strip()
                val = (v.strip() if isinstance(v, str) else v)
                norm[key] = val
            rows.append(norm)
    return rows

def ensure_dir(p: Path, dry: bool):
    if p.exists():
        return
    if dry:
        print(f"[DRY] mkdir -p {p}")
    else:
        p.mkdir(parents=True, exist_ok=True)

def write_text(path: Path, text: str, force: bool, dry: bool):
    if path.exists() and not force:
        print(f"[SKIP] {path} (exists; --force で上書き)")
        return
    if dry:
        print(f"[DRY] write {path}")
    else:
        path.write_text(text, encoding="utf-8")
        print(f"[OK]   {path}")

# -------------------- テンプレ置換 --------------------

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([A-Za-z0-9_\-]+)\s*\}\}")

def render_template(tpl_text: str, mapping: dict) -> str:
    """{{key}} を mapping[key] に置換。未定義は空文字。"""
    def _sub(m):
        k = m.group(1)
        return str(mapping.get(k, "") or "")
    return _PLACEHOLDER_RE.sub(_sub, tpl_text)

def load_templates():
    if not TEMPLATES_DIR.exists():
        raise SystemExit(f"[ERR] テンプレートディレクトリが見つかりません: {TEMPLATES_DIR}")
    if not TPL_ID_PATH.exists():
        raise SystemExit(f"[ERR] 調査IDページ用テンプレが見つかりません: {TPL_ID_PATH}")
    if not TPL_NAME_PATH.exists():
        raise SystemExit(f"[ERR] 調査名ページ用テンプレが見つかりません: {TPL_NAME_PATH}")
    id_tpl = TPL_ID_PATH.read_text(encoding="utf-8")
    name_tpl = TPL_NAME_PATH.read_text(encoding="utf-8")
    return id_tpl, name_tpl

# -------------------- 相対リンク生成 --------------------

def rel_link_from_top_to_name(name: str) -> str:
    """トップ(index.md) から 調査名ページ(index.md) への相対リンク."""
    return f"surveys/{name}/"

def rel_link_from_name_to_id(id_: str) -> str:
    """調査名ページ(index.md) から 同フォルダ内の 調査IDページ への相対リンク."""
    return f"./{id_}"

# -------------------- 生成ロジック --------------------

def build_name_table(name: str, ids: list):
    """調査名ページの「調査ID一覧」テーブル（IDへの相対リンクを使用）。"""
    lines = [
        "| 調査ID | Mesh | 備考 |",
        "|--------|------|------|",
    ]
    for id_ in ids:
        link = rel_link_from_name_to_id(id_)
        lines.append(f"| [{id_}]({link}) |  |  |")
    return "\n".join(lines)

def update_top_index(survey_names: list, force: bool, dry: bool):
    """docs/index.md 内のマーカー間を調査名一覧（相対リンク）で更新。"""
    ensure_dir(DOCS, dry)
    if not INDEX_MD.exists():
        base = [
            "# トップページ",
            "",
            "説明文（ここに概要を書いてください）",
            "",
            "## 調査地図",
            "（GeoJSON 埋め込みはこの下に配置）",
            "",
            "## 調査名の一覧",
            TOP_MARK_BEGIN,
            "",
            TOP_MARK_END,
            ""
        ]
        content = "\n".join(base)
    else:
        content = INDEX_MD.read_text(encoding="utf-8")

    ul_lines = ["<ul>"]
    for name in sorted(survey_names, key=lambda s: s.lower()):
        href = rel_link_from_top_to_name(name)
        ul_lines.append(f'  <li><a href="{href}">{name}</a></li>')
    ul_lines.append("</ul>")
    block = "\n".join(ul_lines)

    if TOP_MARK_BEGIN in content and TOP_MARK_END in content:
        head, rest = content.split(TOP_MARK_BEGIN, 1)
        _, tail = rest.split(TOP_MARK_END, 1)
        new_content = head + TOP_MARK_BEGIN + "\n" + block + "\n" + TOP_MARK_END + tail
    else:
        new_content = content.rstrip() + "\n\n## 調査名の一覧\n" + TOP_MARK_BEGIN + "\n" + block + "\n" + TOP_MARK_END + "\n"

    write_text(INDEX_MD, new_content, force=True, dry=dry)

def main():
    ap = argparse.ArgumentParser(description="Generate MkDocs pages from CSV (external templates; relative links).")
    ap.add_argument("--csv", required=True, type=Path, help="CSV path (columns: survey_id,title,survey_date,region,lat,lon)")
    ap.add_argument("--force", action="store_true", help="既存ファイルを上書き")
    ap.add_argument("--dry-run", action="store_true", help="書き込みせず表示のみ")
    args = ap.parse_args()

    rows = read_csv(args.csv)
    if not rows:
        print("[ERR] CSV が空です")
        return

    ensure_dir(SURVEYS, args.dry_run)
    ensure_dir(ASSETS, args.dry_run)
    id_tpl_text, name_tpl_text = load_templates()

    by_name = defaultdict(list)     # title -> [survey_id,...]
    meta_by_name = {}               # title -> {date, members, route}

    # 相対リンクを保存（トップ基準の相対パス）
    id_to_url = {}     # 例: "001": "surveys/<title>/001"
    name_to_url = {}   # 例: "<title>": "surveys/<title>/"

    for r in rows:
        survey_id = (r.get("survey_id") or "").strip()
        title     = (r.get("title") or "").strip()
        survey_dt = (r.get("survey_date") or "").strip()
        region    = (r.get("region") or "").strip()
        lat       = (r.get("lat") or "").strip()
        lon       = (r.get("lon") or "").strip()

        if not title or not survey_id:
            print(f"[WARN] スキップ（title/survey_id 不足）: {r}")
            continue

        members = (r.get("members") or r.get("参加メンバー") or "").strip()
        route   = (r.get("route")   or r.get("ルート")       or r.get("ルートマップ") or "").strip()
        jjfast  = (r.get("jjfast")  or r.get("JJ_FAST検出日") or r.get("JJ-FAST検出日") or "").strip()
        deter   = (r.get("deter")   or r.get("Deter検出日")   or "").strip()
        firms   = (r.get("firms")   or r.get("NASA_FIRMS")    or r.get("FIRMS") or "").strip()
        prodes  = (r.get("prodes")  or r.get("Prodes年")      or r.get("PRODES") or "").strip()
        state   = (r.get("state")   or r.get("州")            or "").strip()
        note    = (r.get("note")    or r.get("備考")          or "").strip()

        # 調査名フォルダ
        name_dir = SURVEYS / title
        ensure_dir(name_dir, args.dry_run)

        # 調査IDページ（外部テンプレに流し込み）
        id_page_mapping = {
            "id": survey_id,
            "name": title,
            "date": survey_dt,
            "mesh": region,
            "lat": lat,
            "lon": lon,
            "州": state,
            "jjfast": jjfast,
            "deter": deter,
            "firms": firms,
            "prodes": prodes,
            "note": note,
        }
        id_md_text = render_template(id_tpl_text, id_page_mapping)
        write_text(name_dir / f"{survey_id}.md", id_md_text, force=args.force, dry=args.dry_run)

        # 集計（調査名ページ用）
        by_name[title].append(survey_id)
        if title not in meta_by_name:
            meta_by_name[title] = {"date": survey_dt, "members": members, "route": route}

        # 相対リンク（トップから見た相対パスで保存）
        name_to_url[str(title)] = rel_link_from_top_to_name(title)
        id_to_url[str(survey_id)] = f"{rel_link_from_top_to_name(title)}{survey_id}"

    # 調査名ページ（index.md）生成（IDへの相対リンクを埋め込む）
    for title, ids in by_name.items():
        ids_sorted = sorted(ids, key=lambda x: str(x))
        id_table = build_name_table(title, ids_sorted)
        mapping = {
            "name": title,
            "date": meta_by_name.get(title, {}).get("date", ""),
            "members": meta_by_name.get(title, {}).get("members", ""),
            "route": meta_by_name.get(title, {}).get("route", ""),
            "id_table": id_table,
        }
        name_md_text = render_template(name_tpl_text, mapping)
        write_text(SURVEYS / title / "index.md", name_md_text, force=args.force, dry=args.dry_run)

    # トップページの調査名一覧（相対リンク）を自動更新
    update_top_index(list(by_name.keys()), force=True, dry=args.dry_run)

    # GeoJSON 連携用リンクマップ（相対パス）
    ensure_dir(ASSETS, args.dry_run)
    links_payload = {
        "survey_name_to_url": name_to_url,  # "surveys/<title>/"
        "id_to_url": id_to_url              # "surveys/<title>/<id>"
    }
    write_text(LINKS_JSON, json.dumps(links_payload, ensure_ascii=False, indent=2), force=True, dry=args.dry_run)

    print("\n[INFO] 生成完了")
    print(f" - 調査名ページ: docs/surveys/<title>/index.md")
    print(f" - 調査IDページ: docs/surveys/<title>/<survey_id>.md")
    print(f" - トップ更新  : docs/index.md （{TOP_MARK_BEGIN}..{TOP_MARK_END}）")
    print(f" - リンクJSON : {LINKS_JSON}")

if __name__ == "__main__":
    main()
