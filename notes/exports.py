"""Create private, downloadable representations of a journal note."""
from io import BytesIO
from textwrap import wrap

from django.utils.html import escape
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def _font(size, italic=False):
    """Use a journal-like installed font when it is available, with a safe fallback."""
    candidates = (
        ("C:/Windows/Fonts/georgiai.ttf" if italic else "C:/Windows/Fonts/georgia.ttf"),
        ("DejaVuSerif-Italic.ttf" if italic else "DejaVuSerif.ttf"),
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _safe_filename(title):
    slug = "".join(char if char.isalnum() else "-" for char in title.lower()).strip("-")
    return slug[:60] or "journal-note"


def note_filename(note, extension):
    return f"{_safe_filename(note.title)}.{extension}"


def build_note_pdf(note):
    """Return a refined A4 PDF with a calm reading width."""
    output = BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=28 * mm,
        rightMargin=28 * mm,
        topMargin=28 * mm,
        bottomMargin=24 * mm,
        title=note.title,
        author="Scribe",
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "JournalTitle",
        parent=styles["Title"],
        fontName="Times-Italic",
        fontSize=28,
        leading=34,
        textColor=HexColor("#2C2525"),
        spaceAfter=9 * mm,
    )
    date_style = ParagraphStyle(
        "JournalDate",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=HexColor("#756B66"),
        spaceAfter=12 * mm,
    )
    body_style = ParagraphStyle(
        "JournalBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=19,
        textColor=HexColor("#2C2525"),
    )

    date = note.updated_at.strftime("%B %d, %Y")
    body = escape(note.content).replace("\n", "<br/>")
    story = [
        Paragraph(note.title, title_style),
        Paragraph(f"Scribe journal  ·  {date}", date_style),
        Paragraph(body, body_style),
        Spacer(1, 12 * mm),
        Paragraph("Private journal note", ParagraphStyle("Footer", parent=date_style, alignment=TA_CENTER)),
    ]
    document.build(story)
    return output.getvalue()


def build_note_image(note):
    """Return a share-ready PNG card, styled like a page from the journal."""
    width, padding = 1400, 120
    title_font = _font(72, italic=True)
    body_font = _font(35)
    meta_font = _font(25, italic=True)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    def wrap_pixels(text, font, max_width):
        lines = []
        for paragraph in text.splitlines() or [""]:
            words = paragraph.split() or [""]
            current = words[0]
            for word in words[1:]:
                candidate = f"{current} {word}"
                if measure.textlength(candidate, font=font) <= max_width:
                    current = candidate
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
        return lines

    title_lines = wrap_pixels(note.title, title_font, width - 2 * padding)
    content_lines = wrap_pixels(note.content, body_font, width - 2 * padding)
    height = max(980, 300 + len(title_lines) * 94 + len(content_lines) * 57 + 190)
    image = Image.new("RGB", (width, height), "#F8F5F2")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((44, 44, width - 44, height - 44), radius=34, fill="#FFFDFB", outline="#E8E0D8", width=3)
    draw.rounded_rectangle((padding, 112, padding + 56, 120), radius=4, fill="#B89B5E")

    y = 164
    for line in title_lines:
        draw.text((padding, y), line, font=title_font, fill="#2C2525")
        y += 94
    draw.text((padding, y + 7), note.updated_at.strftime("%B %d, %Y"), font=meta_font, fill="#756B66")
    y += 90
    draw.line((padding, y, width - padding, y), fill="#E8E0D8", width=3)
    y += 54
    for line in content_lines:
        draw.text((padding, y), line, font=body_font, fill="#2C2525")
        y += 57

    draw.text((padding, height - 116), "Scribe  ·  Private journal", font=meta_font, fill="#6E5A8A")
    output = BytesIO()
    image.save(output, format="PNG", optimize=True)
    return output.getvalue()
