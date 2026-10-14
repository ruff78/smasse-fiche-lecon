#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMASSE Fiche Lecon - export PDF (moteur de rendu pedagogique)
==============================================================

Convertit un document ecrit dans un dialecte Markdown "pedagogique" en un PDF
pret a imprimer pour les enseignants du secondaire nigerien (progressions
decloisonnees, sequences didactiques, fiches de lecon, grilles d'evaluation).

Dialecte pris en charge
-----------------------
  # / ## / ### / ####     titres de section
  >                       encart (note institutionnelle, consigne)
  > [!CLE]                encart intitule
  -                       liste a puces (2 espaces en tete = sous-niveau)
  1.  2.  1)  1°          liste numerotee
  | a | b |               tableau (ligne d'alienment |---|---| obligatoire)
  <br> dans une cellule   retour a la ligne force
  <!--pagebreak-->        saut de page
  ::: landscape           composition en A4 paysage a partir d'ici
  ::: portrait            retour a la composition A4 portrait

Metadonnees de page de titre : lignes commencant par "@meta " dans le .md

Usage :
    python3 render.py document.md sortie.pdf \
        --title "..." --subtitle "..." --header "..." --footer "..."
"""

from __future__ import annotations

import argparse
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# --------------------------------------------------------------------------- #
#  Charte graphique
# --------------------------------------------------------------------------- #

VERT = colors.HexColor("#0B6E4F")
VERT_CLAIR = colors.HexColor("#E7F2ED")
ORANGE = colors.HexColor("#E87722")
ROUGE = colors.HexColor("#C1272D")
BLEU = colors.HexColor("#1F4E79")
GRIS_FOND = colors.HexColor("#F3F5F6")
GRIS_BORD = colors.HexColor("#C3CBD0")
GRIS_TXT = colors.HexColor("#39424A")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF, SERIF_B = "DejaVuSerif", "DejaVuSerif-Bold"
SANS, SANS_B = "DejaVuSans", "DejaVuSans-Bold"

MARGIN = 15 * mm
HEADER_H = 15 * mm
FOOTER_H = 12 * mm


def register_fonts() -> bool:
    """Enregistre DejaVu (couvre tous les caracteres du francais)."""
    if not os.path.isdir(FONT_DIR):
        return False
    for name, f in ((SERIF, "DejaVuSerif.ttf"), (SERIF_B, "DejaVuSerif-Bold.ttf"),
                    (SANS, "DejaVuSans.ttf"), (SANS_B, "DejaVuSans-Bold.ttf")):
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, f)))
    pdfmetrics.registerFontFamily(SERIF, normal=SERIF, bold=SERIF_B,
                                 italic=SERIF, boldItalic=SERIF_B)
    pdfmetrics.registerFontFamily(SANS, normal=SANS, bold=SANS_B,
                                  italic=SANS, boldItalic=SANS_B)
    addMapping(SERIF, 0, 0, SERIF)
    addMapping(SERIF, 1, 0, SERIF_B)
    addMapping(SANS, 0, 0, SANS)
    addMapping(SANS, 1, 0, SANS_B)
    return True


HAS_TTF = register_fonts()
if not HAS_TTF:                                    # repli Type1
    SERIF = SERIF_B = SANS = SANS_B = "Helvetica"


# --------------------------------------------------------------------------- #
#  Styles
# --------------------------------------------------------------------------- #

def _s(**kw):
    return ParagraphStyle(kw.pop("name", "st"), **kw)


STYLES = {
    "body": _s(name="body", fontName=SERIF, fontSize=9.2, leading=12.4,
               alignment=TA_JUSTIFY, spaceAfter=4),
    "h1": _s(name="h1", fontName=SANS_B, fontSize=13, leading=16,
             textColor=colors.white, alignment=TA_LEFT),
    "h2": _s(name="h2", fontName=SANS_B, fontSize=10.8, leading=13.6,
             textColor=VERT, spaceBefore=9, spaceAfter=1),
    "h3": _s(name="h3", fontName=SANS_B, fontSize=9.5, leading=12.2,
             textColor=BLEU, spaceBefore=7, spaceAfter=2),
    "h4": _s(name="h4", fontName=SANS_B, fontSize=9.1, leading=11.8,
             textColor=GRIS_TXT, spaceBefore=5, spaceAfter=1.5),
    "li": _s(name="li", fontName=SERIF, fontSize=9.2, leading=12.2,
             alignment=TA_LEFT, leftIndent=10, firstLineIndent=-10, spaceAfter=1.8),
    "li2": _s(name="li2", fontName=SERIF, fontSize=9.0, leading=11.9,
              alignment=TA_LEFT, leftIndent=22, firstLineIndent=-10, spaceAfter=1.4),
    "note": _s(name="note", fontName=SANS, fontSize=8.6, leading=11.6,
               alignment=TA_LEFT, textColor=GRIS_TXT, spaceAfter=1.6),
    "note_lbl": _s(name="note_lbl", fontName=SANS_B, fontSize=8.4, leading=10.6,
                   textColor=VERT, spaceAfter=2),
    "tc": _s(name="tc", fontName=SERIF, fontSize=8.1, leading=10.1,
             alignment=TA_LEFT, spaceAfter=0),
    "th": _s(name="th", fontName=SANS_B, fontSize=8.1, leading=10.1,
             alignment=TA_LEFT, textColor=colors.white, spaceAfter=0),
    "small": _s(name="small", fontName=SERIF, fontSize=8.2, leading=11,
                textColor=GRIS_TXT, alignment=TA_LEFT),
    "cover_k": _s(name="cover_k", fontName=SANS, fontSize=9.6, leading=14,
                  alignment=TA_CENTER, textColor=VERT),
    "cover_t": _s(name="cover_t", fontName=SANS_B, fontSize=22, leading=27,
                  alignment=TA_CENTER, textColor=colors.HexColor("#123528")),
    "cover_s": _s(name="cover_s", fontName=SANS, fontSize=11.6, leading=16,
                  alignment=TA_CENTER, textColor=GRIS_TXT),
    "cover_m": _s(name="cover_m", fontName=SANS, fontSize=9.3, leading=13.6,
                  alignment=TA_CENTER, textColor=colors.black),
}

RE_B = re.compile(r"\*\*(.+?)\*\*", re.S)
RE_I = re.compile(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", re.S)
RE_C = re.compile(r"`([^`\n]+?)`")


def inline(text: str) -> str:
    t = text.strip().replace("&", "&amp;").replace("<br>", "<br/>")
    t = re.sub(r"<(?!/?(?:b|i|u|sub|sup|br/?)>)[^>]*>", "", t)
    t = RE_B.sub(lambda m: "<b>%s</b>" % m.group(1), t)
    t = RE_I.sub(lambda m: "<i>%s</i>" % m.group(1), t)
    t = RE_C.sub(lambda m: "<i>%s</i>" % m.group(1), t)
    return t


def P(text: str, style: str = "body", **over) -> Paragraph:
    st = STYLES[style]
    if over:
        st = _s(parent=st, **over)
    return Paragraph(inline(text), st)


class HRule(Flowable):
    """Filet horizontal."""

    def __init__(self, color=ORANGE, thickness=0.9, space_before=1, space_after=3):
        Flowable.__init__(self)
        self.color, self.thickness = color, thickness
        self.sb, self.sa = space_before, space_after

    def wrap(self, availWidth, availHeight):
        self.aw = availWidth
        return (availWidth, self.sb + self.thickness + self.sa)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.sa, self.aw, self.sa)


class Badge(Flowable):
    """Bandeau de titre colore pleine largeur."""

    def __init__(self, text, style="h1", bg=VERT, accent=ORANGE, pad=5.5):
        Flowable.__init__(self)
        self.toc_text = re.sub(r"<[^>]+>|\*\*", "", text)
        self.toc_level = 0 if style == "h1" else 1
        self.para = P(text, style)
        self.bg, self.accent, self.pad = bg, accent, pad

    def wrap(self, availWidth, availHeight):
        self.aw = availWidth
        w, h = self.para.wrap(availWidth - 2 * (self.pad + 1), availHeight)
        self.ph = h
        return (availWidth, h + 2 * self.pad + 2.6)

    def draw(self):
        c = self.canv
        h = self.ph + 2 * self.pad
        c.setFillColor(self.bg)
        c.rect(0, 2.6, self.aw, h - 2.6, stroke=0, fill=1)
        c.setFillColor(self.accent)
        c.rect(0, 0, self.aw, 2.6, stroke=0, fill=1)
        c.saveState()
        c.translate(self.pad + 1, self.pad)
        self.para.drawOn(c, 0, 0)
        c.restoreState()


# --------------------------------------------------------------------------- #
#  Tableaux
# --------------------------------------------------------------------------- #

def _lines_of(raw: str):
    return [x for x in re.split(r"<br\s*/?>", raw) if x.strip()]


def _plain(txt: str) -> str:
    return re.sub(r"<[^>]+>", "", txt.replace("**", "").replace("`", "")).strip()


MIN_COL_W = 41.0
MAX_COL_W = 250.0


def nat_width(text: str, style: str) -> float:
    """Largeur naturelle d'une cellule : plancher = mot le plus long (graisse incluse)."""
    f, s = STYLES[style].fontName, STYLES[style].fontSize
    fb = STYLES[style].fontName
    words = [w for w in re.split(r"\s+", _plain(text)) if w]
    if not words:
        return MIN_COL_W
    longest = max(stringWidth(w, fb, s) for w in words) * 1.18
    body = stringWidth(" ".join(words), f, s) * 0.50
    return max(min(body, MAX_COL_W), longest + 6, MIN_COL_W)


def count_lines(raw: str, width: float, style: str) -> int:
    """Estime le nombre de lignes rendues dans une cellule de largeur donnee."""
    f, s = STYLES[style].fontName, STYLES[style].fontSize
    total = 0
    for part in _lines_of(raw):
        words = _plain(part).split()
        if not words:
            continue
        line, n = "", 1
        for w in words:
            cand = w if not line else line + " " + w
            if stringWidth(cand, f, s) <= width - 6:
                line = cand
            else:
                n += 1
                line = w
        total += n
    return max(total, 1)


LINE_H = 10.1          # hauteur d'une ligne de cellule
ROW_PAD = 5.2


def build_table(block: list, avail: float, max_lines: int):
    rows = []
    for line in block:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    rows = [r for r in rows
            if not all(re.fullmatch(r":?-{2,}:?", (c or "-").strip()) for c in r)]
    if not rows:
        return []
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    header, body = rows[0], rows[1:]

    # --- largeur des colonnes ------------------------------------------- #
    nat = [max(nat_width(rows[r][c], "th" if r == 0 else "tc") for r in range(len(rows)))
           for c in range(ncols)]
    if ncols >= 6:                                   # colonne « n° » etroite
        nat[0] = min(nat[0], 36)
    total = sum(nat)
    if total < avail:
        slack = avail - total
        wts = [n / total for n in nat]
        widths = [nat[i] + slack * wts[i] for i in range(ncols)]
    else:
        widths = [avail * n / total for n in nat]
    widths = [max(w, MIN_COL_W) for w in widths]
    widths = [w * avail / sum(widths) for w in widths]

    # --- segmentation des lignes trop hautes ----------------------------- #
    flat = []
    for r in body:
        est = max(count_lines(c, widths[i], "tc") for i, c in enumerate(r))
        parts = [_lines_of(c) for c in r]
        nlines = max((len(p) for p in parts), default=1)
        if est <= max_lines:
            flat.append((r, est))
            continue
        per = max(1, int(max_lines * nlines / est))
        for idx in range(0, nlines, per):
            seg = ["<br>".join(p[idx:idx + per]) for p in parts]
            h = max([count_lines(seg[i], widths[i], "tc") for i in range(ncols)] + [1])
            flat.append((seg, h))

    # --- paquetage en blocs tenant sur une page -------------------------- #
    out, chunk, used = [], [], 0.0
    page_h = max_lines * LINE_H

    def flush():
        nonlocal chunk, used
        if not chunk:
            return
        data = [[P(c or " ", "th") for c in header]] + \
               [[P(c or " ", "tc") for c in row] for row, _n, _h in chunk]
        t = Table(data, colWidths=widths, repeatRows=1)
        cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), VERT),
            ("BOX", (0, 0), (-1, -1), 0.8, VERT),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, GRIS_BORD),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
            ("TOPPADDING", (0, 0), (-1, -1), 2.6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
        ]
        for i, _row in enumerate(chunk, start=1):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), GRIS_FOND))
        t.setStyle(TableStyle(cmds))
        out.append(t)
        out.append(Spacer(1, 4))
        chunk, used = [], 0.0

    for row, nlines in flat:
        h = nlines * LINE_H + ROW_PAD
        if used and used + h > page_h:
            flush()
        chunk.append((row, 0, nlines))
        used += h
    flush()
    return out


# --------------------------------------------------------------------------- #
#  Document
# --------------------------------------------------------------------------- #

class PedagogicDoc(BaseDocTemplate):
    def __init__(self, filename, header="", footer="", **kw):
        self.header, self.footer = header, footer
        self.toc_entries = []          # [(niveau, titre, page), ...]
        BaseDocTemplate.__init__(self, filename, pagesize=A4, title=kw.pop("title", ""),
                                 author=kw.pop("author", ""),
                                 subject=kw.pop("subject", ""),
                                 creator="SMASSE Fiche Lecon (export PDF)",
                                 leftMargin=MARGIN, rightMargin=MARGIN,
                                 topMargin=MARGIN, bottomMargin=MARGIN, **kw)
        pw, ph = A4
        lw, lh = landscape(A4)

        def fr(idn, w, h):
            return Frame(MARGIN, FOOTER_H, w - 2 * MARGIN, h - FOOTER_H - HEADER_H,
                         id=idn, leftPadding=0, rightPadding=0, topPadding=3, bottomPadding=0)

        self.addPageTemplates([
            PageTemplate(id="cover", frames=[
                Frame(MARGIN, 18 * mm, pw - 2 * MARGIN, ph - 18 * mm - 24 * mm,
                      id="coverf", leftPadding=0, rightPadding=0)],
                pagesize=A4, onPage=self._furniture),
            PageTemplate(id="portrait", frames=[fr("p", pw, ph)],
                         pagesize=A4, onPage=self._furniture),
            PageTemplate(id="landscape", frames=[fr("l", lw, lh)],
                         pagesize=landscape(A4), onPage=self._furniture),
        ])

    def afterFlowable(self, flowable):
        if isinstance(flowable, Badge):
            lvl, txt = flowable.toc_level, flowable.toc_text
        else:
            entry = getattr(flowable, "_toc", None)
            if not (entry and isinstance(entry, tuple)):
                return
            lvl, txt = entry
        key = "sec-%d-%d" % (lvl, self.page)
        try:
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(txt[:70].encode("utf-8").decode("latin-1", "ignore")
                                      if False else txt[:70], key, level=lvl, closed=1)
        except Exception:
            pass
        entry = (lvl, txt[:86], self.page)
        if not self.toc_entries or self.toc_entries[-1] != entry:
            self.toc_entries.append(entry)

    def _furniture(self, canv, doc):
        w, h = doc.pagesize
        n = canv.getPageNumber()
        if n == 1:
            canv.setFillColor(VERT)
            canv.rect(0, h - 13 * mm, w, 13 * mm, stroke=0, fill=1)
            canv.setFillColor(ORANGE)
            canv.rect(0, h - 15.6 * mm, w, 2.6 * mm, stroke=0, fill=1)
            canv.setFillColor(ROUGE)
            canv.rect(0, 0, w, 5.5 * mm, stroke=0, fill=1)
            return
        canv.setStrokeColor(VERT)
        canv.setLineWidth(0.8)
        canv.line(MARGIN, h - 12.5 * mm, w - MARGIN, h - 12.5 * mm)
        canv.setFont(SANS, 7.1)
        canv.setFillColor(GRIS_TXT)
        canv.drawString(MARGIN, h - 11 * mm, self.header)
        canv.drawRightString(w - MARGIN, h - 11 * mm, "SMASSE Fiche Le\u00e7on \u2022 Niger")
        canv.setStrokeColor(GRIS_BORD)
        canv.setLineWidth(0.4)
        canv.line(MARGIN, 10.5 * mm, w - MARGIN, 10.5 * mm)
        canv.setFont(SANS, 7.1)
        canv.drawString(MARGIN, 7.2 * mm, self.footer)
        canv.setFont(SANS_B, 7.6)
        canv.setFillColor(VERT)
        canv.drawRightString(w - MARGIN, 7.2 * mm, "p. %d" % n)

# --------------------------------------------------------------------------- #
#  Lecture du Markdown
# --------------------------------------------------------------------------- #

TOC_DATA = []      # [(niveau, titre, page)] - injecte par main() entre deux passes


def make_toc():
    """Sommaire statique : titre + page, rempli a la passe precedente."""
    if not TOC_DATA:
        return Spacer(1, 6)
    avail = A4[0] - 2 * MARGIN
    st0 = ParagraphStyle("toc0", fontName=SANS_B, fontSize=9.4, leading=12,
                         textColor=VERT)
    st1 = ParagraphStyle("toc1", fontName=SERIF, fontSize=8.7, leading=11.4,
                         leftIndent=14, textColor=colors.black)
    stp = ParagraphStyle("tocp", fontName=SANS_B, fontSize=8.7, leading=11.4,
                         alignment=2, textColor=GRIS_TXT)   # 2 = droite
    rows = []
    for lvl, txt, page in TOC_DATA:
        if "SOMMAIRE" in txt.upper():
            continue
        rows.append([Paragraph(inline(txt), st0 if lvl == 0 else st1),
                     Paragraph(str(page), stp)])
    t = Table(rows, colWidths=[avail - 16 * mm, 16 * mm])
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ("TOPPADDING", (0, 0), (-1, -1), 2.2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
            ("LINEBELOW", (0, 0), (-1, -2), 0.25, GRIS_BORD)]
    for i, (lvl, _t, _p) in enumerate([e for e in TOC_DATA if "SOMMAIRE" not in e[1].upper()]):
        if lvl == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), VERT_CLAIR))
            cmds.append(("TOPPADDING", (0, i), (-1, i), 4.5))
    t.setStyle(TableStyle(cmds))
    return t


def page_max(orient: str) -> int:
    h = (A4[1] if orient == "portrait" else landscape(A4)[1]) - HEADER_H - FOOTER_H - 6
    return int((h - 4) // (LINE_H + ROW_PAD * 0.55))


def parse(md: str, title: str, subtitle: str, meta: list):
    lines = md.split("\n")
    flow, i, orient = [], 0, "portrait"
    n = len(lines)

    while i < n:
        line = lines[i]
        s = line.strip()

        def switch(new):
            """Bascule d'orientation sans creer de page blanche."""
            nonlocal orient
            if new == orient:
                return
            orient = new
            flow.append(NextPageTemplate(new))
            if not flow[:-1] or not isinstance(flow[-2], (PageBreak, CondPageBreak)):
                flow.append(PageBreak())

        if re.match(r"^:::\s*$", s):                  # fin de bloc ::: -> portrait
            switch("portrait")
            i += 1
            continue
        m = re.match(r"^:::\s*(landscape|portrait)\s*$", s, re.I)
        if m:
            switch(m.group(1).lower())
            i += 1
            continue
        if s == "<!--toc-->":
            flow.append(make_toc())
            i += 1
            continue
        if s in ("<!--pagebreak-->", "\\pagebreak", "---PAGE---"):
            # saut conditionnel : pas de page presque vide si la place suffit
            if flow and not isinstance(flow[-1], (PageBreak, CondPageBreak,
                                                  NextPageTemplate)):
                flow.append(CondPageBreak(95))
            i += 1
            continue

        if s.startswith("|"):
            block = []
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            avail = (A4[0] if orient == "portrait" else landscape(A4)[0]) - 2 * MARGIN
            flow += build_table(block, avail, page_max(orient))
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            lvl, txt = len(m.group(1)), m.group(2).strip()
            if lvl == 1:
                bd = Badge(txt)
                bd._toc = (0, re.sub(r"<[^>]+>|\*\*", "", txt))
                flow += [Spacer(1, 4), bd, Spacer(1, 5)]
            elif lvl == 2:
                ph = P(txt, "h2")
                ph._toc = (1, re.sub(r"<[^>]+>|\*\*", "", txt))
                flow += [ph, HRule(ORANGE, 0.9, 0.5, 3)]
            elif lvl == 3:
                flow += [P(txt, "h3"), HRule(GRIS_BORD, 0.5, 0, 2.5)]
            else:
                flow.append(P(txt, "h4"))
            i += 1
            continue

        if s.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            label = None
            if block and re.match(r"^\[![^\]]+\]$", block[0]):
                label = block.pop(0)[2:-1].strip()
            avail = (A4[0] if orient == "portrait" else landscape(A4)[0]) - 2 * MARGIN
            data = ([[P(label.upper(), "note_lbl")]] if label else []) + \
                   [[P(b, "note")] for b in block if b]
            if not data:
                i += 1
                continue
            box = Table(data, colWidths=[avail - 8])
            box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), VERT_CLAIR),
                ("LINEBEFORE", (0, 0), (0, -1), 2.8, VERT),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, 0 if label else -1), 4.5),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 4.5),
                ("TOPPADDING", (0, 1 if label else 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -2), 1),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            flow += [Spacer(1, 3), KeepTogether([box]), Spacer(1, 4)]
            continue

        m = re.match(r"^(\s*)[-*\u2022]\s+(.*)$", line)
        if m:
            st = "li2" if len(m.group(1)) >= 2 else "li"
            flow.append(Paragraph("\u2022&nbsp;&nbsp;" + inline(m.group(2)), STYLES[st]))
            i += 1
            continue
        m = re.match(r"^(\s*)(\d+\s*[°.)])\s+(.*)$", line)
        if m:
            st = "li2" if len(m.group(1)) >= 2 else "li"
            num = m.group(2).replace(" ", "")
            flow.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, inline(m.group(3))),
                                  STYLES[st]))
            i += 1
            continue

        if not s:
            i += 1
            continue

        buf = [s]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^\s*(#{1,4}\s|[-*\u2022]\s|\d+\s*[°.)]\s|\||>|:::|<!--|@meta)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        flow.append(P(" ".join(buf), "body"))

    return flow


def cover_flow(title, subtitle, meta, kicker=""):
    f = [P("R\u00e9publique du Niger \u2022 Minist\u00e8re charg\u00e9 de "
           "l\u2019Enseignement secondaire<br/>Direction des Lyc\u00e9es et des "
           "Coll\u00e8ges d\u2019Enseignement g\u00e9n\u00e9ral \u2022 "
           "Inspection de Fran\u00e7ais",
           "cover_k", alignment=TA_CENTER),
         Spacer(1, 3 * mm),
         HRule(VERT, 1.2, 0, 2), Spacer(1, 22 * mm)]
    if kicker:
        f += [P(kicker.upper(), "cover_k", fontName=SANS_B, fontSize=10,
                textColor=ORANGE), Spacer(1, 6 * mm)]
    f += [P(title, "cover_t"), Spacer(1, 4.5 * mm)]
    bar = Table([[""]], colWidths=[64 * mm], rowHeights=[1.8], hAlign="CENTER")
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ORANGE)]))
    f += [bar, Spacer(1, 5.5 * mm)]
    if subtitle:
        f += [P(subtitle, "cover_s"), Spacer(1, 12 * mm)]
    rows = []
    for m in meta:
        if ":" in m:
            k, v = m.split(":", 1)
            rows.append([P(k.strip(), "cover_m", fontName=SANS_B, alignment=TA_LEFT),
                         P(v.strip(), "cover_m", alignment=TA_LEFT)])
        elif m:
            rows.append([P(m, "cover_m"), P("", "cover_m")])
    if rows:
        box = Table(rows, colWidths=[58 * mm, 92 * mm])
        box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, VERT),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, GRIS_BORD),
            ("BACKGROUND", (0, 0), (0, -1), VERT_CLAIR),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 4.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ]))
        box.hAlign = "CENTER"
        f.append(box)
    return f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("out")
    ap.add_argument("--title", default="Progression")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--header", default="")
    ap.add_argument("--footer", default="")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--no-cover", action="store_true")
    args = ap.parse_args()

    with open(args.source, encoding="utf-8") as fh:
        md = fh.read()
    meta = [l[5:].strip() for l in md.splitlines() if l.startswith("@meta")]
    md = "\n".join(l for l in md.splitlines() if not l.startswith("@meta"))

    global TOC_DATA

    def build_once(dest):
        doc = PedagogicDoc(
            dest,
            header=args.header or args.title,
            footer=args.footer or "Fran\u00e7ais \u2014 3\u00e8me ann\u00e9e du 1er cycle \u2022 "
                                  "Ann\u00e9e scolaire 2026-2027",
            title=args.title, author="SMASSE Fiche Le\u00e7on",
            subject="Progression annuelle d\u00e9cloisonn\u00e9e de fran\u00e7ais, "
                    "classe de 3e (Niger)",
        )
        flow = []
        if not args.no_cover:
            flow += cover_flow(args.title, args.subtitle, meta, args.kicker)
            flow += [NextPageTemplate("portrait"), PageBreak()]
        flow += parse(md, args.title, args.subtitle, meta)
        doc.build(flow)
        return doc.toc_entries

    # Le sommaire (<!--toc-->) exige des numeros de page : on reconstruit
    # jusqu'a ce que les pages relevees ne bougent plus (3 passes en pratique).
    entries = []
    for _ in range(5):
        TOC_DATA = entries
        found = build_once(args.out)
        if found == entries:
            break
        entries = found
    else:
        TOC_DATA = entries
        build_once(args.out)
    size = os.path.getsize(args.out) / 1024
    print("OK  %s  (%.0f Ko, sommaire : %d entrees)" % (args.out, size, len(entries)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
