#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_pages_from_csv.py (external templates; RELATIVE LINKS)

- CSV から MkDocs ページを一括生成（外部テンプレート使用）
- すべて相対リンクで出力（トップ → 調査名、調査名 → ID）
- 作成物:
  * docs/surveys/<title>/<survey_id>.md
  * docs/surveys/<title>/index.md
  * docs/index.md の "調査名の一覧" 自動更新（マーカー間のみ）
  * docs/assets/survey_links.json （相対パスを保存）

CSV 主な列:
  - fid
  - survey_id
  - title
  - survey_date
  - region
  - type       : （今回は使わない）
  - lat
  - lon
  - Embargo
  - Deter
  - Tipo       : DES/LOG など → type として利用
  - Prodes
  - JJ-FAST_v3_2
  - JJ-FAST_v4_1

テンプレ :
  - templates/template_id.md      （調査IDページ）
  - templates/template_name.md    （調査名ページ）
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

IMAGES_DIR = DOCS / "images"
MAP_DIR = IMAGES_DIR / "map"
GRAPH_DIR = IMAGES_DIR / "graph"

LINKS_JSON = ASSETS / "survey_links.json"
INDEX_MD = DOCS / "index.md"
TOP_MARK_BEGIN = "<!-- BEGIN: AUTO_SURVEY_LIST -->"
TOP_MARK_END   = "<!-- END: AUTO_SURVEY_LIST -->"

# 必須テンプレ
TPL_ID_PATH   = TEMPLATES_DIR / "template_id.md"
TPL_NAME_PATH = TEMPLATES_DIR / "template_name.md"

# -------------------- 基本 I/O --------------------

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

def build_name_table(name: str, records: list):
    """
    調査名ページの「調査ID一覧」テーブルを生成。

    仕様:
      - | ID | Mesh | の 2 列のみ
      - Mesh は CSV の region を自動流し込み
    records: [{"id": "...", "mesh": "..."}, ...]
    """
    lines = [
        "| ID | Mesh |",
        "|--------|------|",
    ]
    for rec in records:
        id_ = rec["id"]
        mesh = rec.get("mesh", "")
        link = rel_link_from_name_to_id(id_)
        lines.append(f"| [{id_}]({link}) | {mesh} |")
    return "\n".join(lines)

def update_top_index(survey_names: list, force: bool, dry: bool):
    """
    docs/index.md 内のマーカー間を調査名一覧（相対リンク）で更新。
    """
    ensure_dir(DOCS, dry)
    if not INDEX_MD.exists():
        base = [
            "# MORI Field Survey Reports",
            "",
            "本サイトは、Project MORI の現地調査結果を整理・公開するためのページです。",
            "",
            "## 概要",
            "",
            "- 調査の目的と背景の概要をここに記載してください。",
            "- 利用上の注意点や、問い合わせ先などもあれば追記してください。",
            "",
            "## 調査マップ（GeoJSON）",
            "",
            "GitHub Pages 上に表示する GeoJSON マップ（ポイント）の埋め込みコードやリンクをこのセクションに記載します。",
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
        new_content = (
            content.rstrip()
            + "\n\n## 調査名の一覧\n"
            + TOP_MARK_BEGIN + "\n"
            + block + "\n"
            + TOP_MARK_END + "\n"
        )

    write_text(INDEX_MD, new_content, force=True, dry=dry)

def extract_state_from_survey_id(survey_id: str) -> str:
    """
    例: PV-RO-2209-23 -> RO を抽出
    先頭が英字 + '-' + 2文字州コード + '-' のパターンを想定。
    """
    if not survey_id:
        return ""
    m = re.match(r"^[A-Z]+-([A-Z]{2})-", survey_id)
    if m:
        return m.group(1)
    return ""

def build_map_and_graph_blocks(survey_id: str) -> tuple[str, str]:
    """
    各調査IDページ用の Map / Graph セクションを組み立てる。

    - Map: docs/images/map/<id>.png
    - Graph: docs/images/graph/<id>_*.png （複数可）

    調査IDページの位置: docs/surveys/<title>/<id>.md
      → docs/images/... への相対パスは "../../images/..."
    """
    # ---- Map ----
    map_file = MAP_DIR / f"{survey_id}.png"
    if map_file.exists():
        map_rel = f"../../images/map/{map_file.name}"
        map_block = f"![Static survey map for {survey_id}]({map_rel})"
    else:
        map_block = "（静的地図画像はまだ登録されていません）"

    # ---- Graph(s) ----
    graph_block = "（グラフ画像はまだ登録されていません）"
    if GRAPH_DIR.exists():
        graph_files = sorted(GRAPH_DIR.glob(f"{survey_id}_*.png"))
        if graph_files:
            lines = []
            for gf in graph_files:
                rel = f"../../images/graph/{gf.name}"
                alt = gf.stem
                lines.append(f"![Graph {alt}]({rel})")
            graph_block = "\n".join(lines)

    return map_block, graph_block

def main():
    ap = argparse.ArgumentParser(
        description="Generate MkDocs pages from CSV (external templates; relative links)."
    )
    ap.add_argument(
        "--csv", required=True, type=Path,
        help="CSV path (columns: survey_id,title,survey_date,region,lat,lon, ...)"
    )
    ap.add_argument("--force", action="store_true", help="既存ファイルを上書き")
    ap.add_argument("--dry-run", action="store_true", help="書き込みせず表示のみ")
    args = ap.parse_args()

    rows = read_csv(args.csv)
    if not rows:
        print("[ERR] CSV が空です")
        return

    ensure_dir(SURVEYS, args.dry_run)
    ensure_dir(ASSETS, args.dry_run)
    # 画像ディレクトリは「存在していれば使う」方針なので、ここで作成はしない
    id_tpl_text, name_tpl_text = load_templates()

    # by_name: title -> [{"id": ..., "mesh": ...}, ...]
    by_name = defaultdict(list)
    meta_by_name = {}               # title -> {date, members, route}

    # 相対リンクを保存（トップ基準の相対パス）
    id_to_url = {}     # 例: "PV-RO-2209-23": "surveys/<title>/PV-RO-2209-23"
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

        # --- 追加情報（今後のため members/route だけ残しておく） ---
        members = (r.get("members") or r.get("参加メンバー") or "").strip()
        route   = (r.get("route")   or r.get("ルート")       or r.get("ルートマップ") or "").strip()

        # --- 州: CSV列がなければ survey_id から抽出 ---
        state = (r.get("state") or r.get("州") or "").strip()
        if not state:
            state = extract_state_from_survey_id(survey_id)

        embargo = (r.get("Embargo") or r.get("emb") or "").strip()
        deter   = (
            r.get("Deter")
            or r.get("deter")
            or r.get("Deter検出日")
            or ""
        ).strip()
        prodes = (
            r.get("Prodes")
            or r.get("prodes")
            or r.get("Prodes年")
            or r.get("PRODES")
            or ""
        ).strip()

        # JJ-FAST v3.2 / v4.1 （今回の CSV に合わせて）
        jjfast_v3 = (
            r.get("JJ-FAST_v3_2")
            or r.get("JJ_FAST_v3")
            or r.get("JJ-FAST v3.2")
            or ""
        ).strip()
        jjfast_v4 = (
            r.get("JJ-FAST_v4_1")
            or r.get("JJ_FAST_v4")
            or r.get("JJ-FAST v4.1")
            or ""
        ).strip()

        # FIRMS は今回の CSV には列がないので、将来用に空のままでもOK
        firms = (
            r.get("NASA_FIRMS")
            or r.get("FIRMS")
            or r.get("firms")
            or ""
        ).strip()

        # 備考/Obs 用（今は列がないので、将来 note 列が増えたらここにマップ）
        note = (
            r.get("note")
            or r.get("obs")
            or r.get("備考")
            or ""
        ).strip()

        # Tipo → type として使う（CSV の type 列は使わない）
        tipo = (
            r.get("Tipo")
            or r.get("tipo")
            or r.get("TIPO")
            or ""
        ).strip()

        # Map / Graph ブロック生成
        map_block, graph_block = build_map_and_graph_blocks(survey_id)

        # 調査名フォルダ
        name_dir = SURVEYS / title
        ensure_dir(name_dir, args.dry_run)

        # 調査IDページ（外部テンプレに流し込み）
        id_page_mapping = {
            "id": survey_id,
            "name": title,
            "date": survey_dt,
            "mesh": region,
            "state": state,
            "lat": lat,
            "lon": lon,

            "JJ_FAST_v3": jjfast_v3,
            "JJ_FAST_v4": jjfast_v4,
            "Deter":      deter,
            "type":       tipo,
            "NASA_FIRMS": firms,
            "Prodes":     prodes,
            "emb":        embargo,
            # "obs":        note,

            "map_block":   map_block,
            "graph_block": graph_block,

            # 旧テンプレ互換用（もし他で使用していれば）
            "州": state,
            "jjfast": jjfast_v3,
            "deter": deter,
            "firms": firms,
            "prodes": prodes,
            "note": note,
        }

        id_md_text = render_template(id_tpl_text, id_page_mapping)
        write_text(name_dir / f"{survey_id}.md", id_md_text, force=args.force, dry=args.dry_run)

        # 集計（調査名ページ用: ID + Mesh(region) を保存）
        by_name[title].append({"id": survey_id, "mesh": region})
        if title not in meta_by_name:
            meta_by_name[title] = {"date": survey_dt, "members": members, "route": route}

        # 相対リンク（トップから見た相対パスで保存）
        name_to_url[str(title)] = rel_link_from_top_to_name(title)
        id_to_url[str(survey_id)] = f"{rel_link_from_top_to_name(title)}{survey_id}"

    # 調査名ページ（index.md）生成
    for title, records in by_name.items():
        # IDでソート
        records_sorted = sorted(records, key=lambda r: str(r["id"]))
        id_table = build_name_table(title, records_sorted)
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
    write_text(
        LINKS_JSON,
        json.dumps(links_payload, ensure_ascii=False, indent=2),
        force=True,
        dry=args.dry_run,
    )

    print("\n[INFO] 生成完了")
    print(" - 調査名ページ: docs/surveys/<title>/index.md")
    print(" - 調査IDページ: docs/surveys/<title>/<survey_id>.md")
    print(f" - トップ更新  : docs/index.md （{TOP_MARK_BEGIN}..{TOP_MARK_END}）")
    print(f" - リンクJSON : {LINKS_JSON}")

if __name__ == "__main__":
    main()
