import os
import uuid
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.core.logging import logger

REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../reports"))
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_pdf_report(incident_data: Dict[str, Any]) -> str:
    """
    Generates a professional SOC Cybersecurity Incident Report PDF using ReportLab.
    Includes incident metadata, risk scoring breakdown, evidence quotes,
    detected tactics, mitigation guidance, and compliance disclaimers.
    """
    incident_number = incident_data.get("incident_number", "INC-UNKNOWN")
    report_id = f"REP-{uuid.uuid4().hex[:8].upper()}"
    filename = f"KAVACH_SOC_Report_{incident_number}.pdf"
    file_path = os.path.join(REPORTS_DIR, filename)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Styling
    brand_title_style = ParagraphStyle(
        'BrandTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        fontName="Helvetica-Bold",
        spaceAfter=2
    )
    meta_style = ParagraphStyle(
        'MetaSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0284c7"),
        fontName="Helvetica-Bold",
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1e293b")
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=12,
        fontName="Courier",
        textColor=colors.HexColor("#334155")
    )
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#64748b")
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("🛡️ KAVACH AI — Security Incident Response Report", brand_title_style))
    story.append(Paragraph(
        f"<b>Report ID:</b> {report_id} &nbsp;|&nbsp; "
        f"<b>Incident Ref:</b> {incident_number} &nbsp;|&nbsp; "
        f"<b>Generated:</b> {incident_data.get('created_at', 'N/A')}",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0284c7"), spaceAfter=10))

    # 2. Executive Overview Table
    severity = incident_data.get("severity", "Medium")
    risk_score = incident_data.get("risk_score", 0.0)

    # Determine severity background color
    sev_bg = colors.HexColor("#fee2e2") if severity in ["Critical", "High"] else colors.HexColor("#fef3c7")
    sev_text = "#991b1b" if severity in ["Critical", "High"] else "#92400e"

    overview_rows = [
        [Paragraph("Incident Title:", body_bold), Paragraph(str(incident_data.get("title", "Voice Scam Alert")), body_style)],
        [Paragraph("Assigned Analyst:", body_bold), Paragraph(str(incident_data.get("assigned_analyst", "SOC Analyst 1")), body_style)],
        [Paragraph("Investigation Status:", body_bold), Paragraph(f"<b>{incident_data.get('status', 'New')}</b>", body_style)],
        [Paragraph("Assessed Severity:", body_bold), Paragraph(f"<font color='{sev_text}'><b>{severity}</b></font>", body_style)],
        [Paragraph("Calculated Risk Score:", body_bold), Paragraph(f"<b>{risk_score} / 100</b> (Explainable Rule Engine)", body_style)],
        [Paragraph("Detected Language:", body_bold), Paragraph(str(incident_data.get("detected_language", "en")).upper(), body_style)],
    ]
    t_overview = Table(overview_rows, colWidths=[140, 400])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 10))

    # 3. Audio & Evidence Transcript
    story.append(Paragraph("Audio & Conversation Transcript", h2_style))
    transcript_text = incident_data.get("transcript_text", "").strip() or "No transcript available."
    transcript_preview = transcript_text if len(transcript_text) < 500 else transcript_text[:500] + "..."
    t_transcript = Table([[Paragraph(f"<i>\"{transcript_preview}\"</i>", code_style)]], colWidths=[540])
    t_transcript.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_transcript)
    story.append(Spacer(1, 10))

    # 4. Detected Threats Table
    story.append(Paragraph("Detected Social Engineering Tactics & Evidence", h2_style))
    threats = incident_data.get("threats", [])
    if threats:
        threat_table_data = [
            [
                Paragraph("<b>Threat Category</b>", body_bold),
                Paragraph("<b>Matched Evidence</b>", body_bold),
                Paragraph("<b>Points</b>", body_bold),
                Paragraph("<b>Tactic Explanation</b>", body_bold)
            ]
        ]
        for th in threats:
            threat_table_data.append([
                Paragraph(str(th.get("category", "")), body_style),
                Paragraph(f"<code>{th.get('matched_text', '')}</code>", code_style),
                Paragraph(f"+{th.get('contribution', 0)}", body_bold),
                Paragraph(str(th.get("explanation", "")), body_style)
            ])
        t_threats = Table(threat_table_data, colWidths=[120, 100, 45, 275])
        t_threats.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#94a3b8")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t_threats)
    else:
        story.append(Paragraph("No suspicious social engineering tactics detected. Call classified as benign.", body_style))
    story.append(Spacer(1, 10))

    # 5. Immediate Mitigation Guidance
    story.append(Paragraph("Actionable Defensive Recommendations", h2_style))
    recommendations = incident_data.get("recommendations", [
        "Never disclose OTP, UPI PIN, or banking passwords.",
        "End suspicious calls and independently verify via official numbers.",
        "Report cybercrime incidents immediately to National Helpline 1930."
    ])
    rec_items = []
    for r in recommendations[:4]:
        rec_items.append([Paragraph("•", body_bold), Paragraph(str(r), body_style)])
    t_recs = Table(rec_items, colWidths=[15, 525])
    t_recs.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_recs)
    story.append(Spacer(1, 12))

    # 6. Analyst Notes & Incident Timeline
    if incident_data.get("analyst_notes"):
        story.append(Paragraph("Analyst Investigation Notes", h2_style))
        story.append(Paragraph(str(incident_data.get("analyst_notes")), body_style))
        story.append(Spacer(1, 8))

    # 7. Compliance Disclaimer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceBefore=10, spaceAfter=6))
    disclaimer_text = (
        "<b>IMPORTANT NOTICE:</b> KAVACH AI is an AI-assisted decision-support system, not a guaranteed fraud detector. "
        "Threat scores and tactic classifications are algorithmic recommendations based on acoustic speech transcription "
        "and social-engineering heuristics. This report is intended for security operations centre analysts and authorized "
        "investigators. In case of emergency or financial theft, report immediately to Indian Cybercrime Reporting Portal "
        "(https://cybercrime.gov.in) or call the Cyber Helpline at 1930."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))

    # Build document
    doc.build(story)
    logger.info(f"Generated SOC incident report PDF at {file_path}")
    return file_path
