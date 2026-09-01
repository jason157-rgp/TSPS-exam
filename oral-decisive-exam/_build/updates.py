#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新時間與更新紀錄

側欄倒數下面標「最後更新」，卷首放一張逐次的更新紀錄表。
時間取建置當下的台北時間——GitHub Pages 每次推送都會重新建置，
所以這個時間就是網站上線的時間。
"""
import datetime
import subprocess
from pathlib import Path

TPE = datetime.timezone(datetime.timedelta(hours=8))

# 由新到舊。日期用台北時間的月/日。
LOG = [
    ("09/02", "台大確定是戴浩志理事長（只有人選、沒有出題方向）；同院的洪學義因此可跳過"),
    ("09/02", "側欄加入「隱藏今年不會出的」開關——藏起 11 位同院已被取代的考官與 6 個只有他們會問的主題"),
    ("08/31", "新增〈可以跳過的考官〉：依 114 年「一院一位」的規律，標出可跳過的名單與會連帶消失的主題"),
    ("08/31", "補完七個缺口：唇顎裂、正顎、OSA、軟組織肉瘤、高壓氧、KTS、植入物手術的預防性抗生素"),
    ("08/30", "新增〈考官簡介與照片〉：110 年之後仍出題的 27 位，連到各自醫院官網的簡介頁"),
    ("08/30", "新增〈今年確定出場的考官 × 老師本人給的提示〉，並在各考官節頂端加上提示帶"),
    ("08/30", "新增〈考前情報更新〉：同學回報的考官情報 × 手冊考官檔案逐關對照"),
    ("08/29", "新增 12 集語音課程，可用 Safari 朗讀螢幕收聽；側欄加入入口"),
    ("08/27", "已讀狀態納入跨裝置同步；側欄加上未讀計數與「只看未讀」"),
    ("08/27", "每節下方的筆記可跨裝置同步（Cloudflare Worker）"),
    ("08/27", "每節下方加入筆記，自動儲存、可匯出匯入"),
    ("08/26", "全書內容換成校訂版 markdown（211 節，框架不動）"),
    ("08/25", "新增純文字版 plain/，讓不執行 JavaScript 的工具也讀得到內容"),
    ("08/25", "修復段落結構，還原 77 張表格與 2871 個清單項；補回遺失的「第二部」標題"),
    ("08/24", "接上瀏覽器 history：可回上一頁，每一節有自己的網址"),
    ("08/24", "更正考試日星期（2026/09/05 是星期六）；讀書進度表改為即時倒數"),
    ("08/24", "重建索引與導覽，第一部 91 列反查索引全部可點"),
    ("08/24", "手冊自 Claude artifact 移入 GitHub"),
]


def stamp() -> str:
    """建置時間（台北）。CI 上以 commit 時間為準，本機則用現在時間。"""
    try:
        iso = subprocess.run(["git", "log", "-1", "--format=%cI"],
                             cwd=Path(__file__).resolve().parent,
                             capture_output=True, text=True, timeout=5).stdout.strip()
        if iso:
            return datetime.datetime.fromisoformat(iso).astimezone(TPE).strftime("%Y/%m/%d %H:%M")
    except Exception:
        pass
    return datetime.datetime.now(TPE).strftime("%Y/%m/%d %H:%M")


def rail_html(ts: str) -> str:
    """側欄倒數下面那一行。"""
    return (f'\n    <div class="stamp">最後更新　{ts[5:]}　'
            f'<button type="button" class="jump" data-go="s1">更新紀錄</button></div>')


def log_html(ts: str) -> str:
    """卷首的更新紀錄表。"""
    rows = "\n".join(f"<tr><td>{d}</td><td>{t}</td></tr>" for d, t in LOG)
    return (
        '<h3 id="updates">更新紀錄</h3>\n'
        f'<p>最後更新：<strong>{ts}</strong>（台北時間）。'
        '本手冊每次改動都會重新建置並上線，這個時間就是目前這一版的上線時間。</p>\n'
        '<table>\n<thead><tr><th>日期</th><th>更新內容</th></tr></thead>\n'
        f'<tbody>\n{rows}\n</tbody>\n</table>\n'
    )
