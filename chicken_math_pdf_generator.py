#!/usr/bin/env python3
"""
Chicken Math Calculator - Official Government Audit Report Generator
Creates a fancy 2-page PDF report with chicken clipart and red stamps
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Ellipse
from reportlab.graphics import renderPDF
from datetime import datetime
import io

def create_stamp_graphic():
    """Create a red 'OFFICIAL' stamp graphic"""
    d = Drawing(100, 100)
    # Outer circle
    d.add(Ellipse(50, 50, 45, 45, strokeColor=colors.red, strokeWidth=3, fillColor=None))
    # Inner circle
    d.add(Ellipse(50, 50, 35, 35, strokeColor=colors.red, strokeWidth=2, fillColor=None))
    return d

def add_page_number(canvas, doc):
    """Add page numbers and header/footer to each page"""
    canvas.saveState()
    
    # Header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(colors.HexColor('#e74c3c'))
    canvas.drawString(inch, letter[1] - 0.5*inch, "DEPARTMENT OF CHICKEN MATHEMATICS")
    canvas.drawString(letter[0] - 3*inch, letter[1] - 0.5*inch, f"Report Date: {datetime.now().strftime('%B %d, %Y')}")
    
    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.grey)
    page_num = canvas.getPageNumber()
    text = f"Page {page_num} | CONFIDENTIAL - For Chicken Owner Use Only"
    canvas.drawCentredString(letter[0]/2.0, 0.5*inch, text)
    
    canvas.restoreState()

def generate_chicken_math_pdf(data, output_filename="chicken_math_report.pdf"):
    """
    Generate the official Chicken Math PDF report
    
    data = {
        'name': 'John Doe',
        'current_flock': 6,
        'real_flock': 11,
        'yearly_eggs': 3146,
        'egg_revenue': 1573.00,
        'feed_cost': 756.00,
        'net_profit': 817.00,
        'funny_quote': 'Your funny quote here...',
        'recommended_purchase': 'Premium Feed Upgrade Package',
        'meme_image_url': None  # Optional URL to chicken meme
    }
    """
    
    # Create the PDF
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=100,
        bottomMargin=72
    )
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#e74c3c'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    stamp_style = ParagraphStyle(
        'Stamp',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.red,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # PAGE 1: OFFICIAL AUDIT REPORT
    
    # Title with chicken emoji representation
    title = Paragraph("🐔 OFFICIAL CHICKEN MATH AUDIT REPORT 🐔", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Official stamp
    stamp = Paragraph("★ OFFICIAL CERTIFIED ★", stamp_style)
    elements.append(stamp)
    elements.append(Spacer(1, 0.3*inch))
    
    # Chicken owner info
    owner_info = Paragraph(f"<b>Prepared For:</b> {data.get('name', 'Chicken Owner')}", subtitle_style)
    elements.append(owner_info)
    elements.append(Spacer(1, 0.1*inch))
    
    date_info = Paragraph(f"<b>Audit Date:</b> {datetime.now().strftime('%B %d, %Y')}", body_style)
    elements.append(date_info)
    elements.append(Spacer(1, 0.3*inch))
    
    # Warning notice
    warning = Paragraph(
        "<b>⚠️ OFFICIAL NOTICE ⚠️</b><br/>"
        "This report contains classified information regarding the true size of your chicken flock. "
        "The discrepancies found during this audit are NOT your fault. Chicken Math is a scientifically "
        "proven phenomenon affecting 99.7% of backyard chicken owners.",
        body_style
    )
    elements.append(warning)
    elements.append(Spacer(1, 0.3*inch))
    
    # FINDINGS TABLE
    elements.append(Paragraph("<b>SECTION 1: FLOCK SIZE FINDINGS</b>", subtitle_style))
    
    flock_data = [
        ['Category', 'Count', 'Status'],
        ['Chickens You Admit To Owning', str(data.get('current_flock', 0)), '✓'],
        ['Actual Chicken Count (Per Audit)', str(data.get('real_flock', 0)), '⚠️'],
        ['Discrepancy', str(data.get('real_flock', 0) - data.get('current_flock', 0)), 'CRITICAL']
    ]
    
    flock_table = Table(flock_data, colWidths=[3*inch, 1.5*inch, 1*inch])
    flock_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f39c12')),
    ]))
    
    elements.append(flock_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ECONOMIC ANALYSIS
    elements.append(Paragraph("<b>SECTION 2: ECONOMIC IMPACT ANALYSIS</b>", subtitle_style))
    
    economic_data = [
        ['Metric', 'Annual Amount'],
        ['Projected Egg Production', f"{data.get('yearly_eggs', 0):,} eggs"],
        ['Egg Revenue Value', f"${data.get('egg_revenue', 0):,.2f}"],
        ['Feed & Bedding Costs', f"${data.get('feed_cost', 0):,.2f}"],
        ['Net Financial Impact', f"${data.get('net_profit', 0):,.2f}"]
    ]
    
    economic_table = Table(economic_data, colWidths=[3.5*inch, 2*inch])
    economic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#2ecc71') if data.get('net_profit', 0) >= 0 else colors.HexColor('#e74c3c')),
    ]))
    
    elements.append(economic_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Official Assessment
    elements.append(Paragraph("<b>OFFICIAL ASSESSMENT:</b>", subtitle_style))
    assessment = Paragraph(data.get('funny_quote', 'No assessment provided.'), body_style)
    elements.append(assessment)
    
    # PAGE BREAK
    elements.append(PageBreak())
    
    # PAGE 2: RECOMMENDATIONS AND CERTIFICATION
    
    page2_title = Paragraph("OFFICIAL RECOMMENDATIONS & CERTIFICATION", title_style)
    elements.append(page2_title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Recommendations
    elements.append(Paragraph("<b>SECTION 3: DEPARTMENT RECOMMENDATIONS</b>", subtitle_style))
    
    rec_text = f"""
    Based on our comprehensive audit of your chicken operation, the Department of Chicken Mathematics 
    hereby recommends the following action:<br/><br/>
    <b>Recommended Purchase:</b> {data.get('recommended_purchase', 'Premium Chicken Care Package')}<br/><br/>
    This recommendation is based on your current flock size, production levels, and the undeniable 
    laws of Chicken Math. Compliance is voluntary but highly encouraged for optimal chicken happiness.
    """
    elements.append(Paragraph(rec_text, body_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Fun Facts
    elements.append(Paragraph("<b>SECTION 4: OFFICIAL CHICKEN MATH FACTS</b>", subtitle_style))
    
    facts = [
        "• The Chicken Math Formula has been scientifically proven in over 1 million backyard coops",
        "• 97% of chicken owners underestimate their true flock size by at least 40%",
        "• The primary cause of Chicken Math is 'just one more won't hurt' syndrome",
        "• Most chicken owners experience Chicken Math within 6 months of their first purchase",
        "• There is no known cure for Chicken Math, only acceptance"
    ]
    
    for fact in facts:
        elements.append(Paragraph(fact, body_style))
    
    elements.append(Spacer(1, 0.4*inch))
    
    # Certification
    elements.append(Paragraph("<b>OFFICIAL CERTIFICATION</b>", subtitle_style))
    
    cert_text = """
    This report has been prepared in accordance with the Official Chicken Math Standards (OCMS) 
    and the International Backyard Poultry Guidelines (IBPG). All calculations have been verified 
    by certified Chicken Mathematicians.<br/><br/>
    This document serves as official proof that you are not crazy—you really do have more chickens 
    than you thought you had.
    """
    elements.append(Paragraph(cert_text, body_style))
    elements.append(Spacer(1, 0.4*inch))
    
    # Signature section
    sig_data = [
        ['', ''],
        ['_' * 40, '_' * 40],
        ['Chief Chicken Mathematician', 'Department Director'],
        ['Dr. Henrietta Clucksworth', 'Colonel Sanders III']
    ]
    
    sig_table = Table(sig_data, colWidths=[2.75*inch, 2.75*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 2), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 2), (-1, 2), 10),
        ('FONTSIZE', (0, 3), (-1, 3), 9),
    ]))
    
    elements.append(sig_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer stamp
    footer_stamp = Paragraph("★ OFFICIAL GOVERNMENT DOCUMENT ★<br/><br/>NOT VALID WITHOUT CHICKEN STAMP", stamp_style)
    elements.append(footer_stamp)
    
    # Build PDF
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    
    print(f"PDF generated successfully: {output_filename}")
    return output_filename


if __name__ == "__main__":
    # Example usage with sample data
    sample_data = {
        'name': 'Jane Chicken Lover',
        'current_flock': 6,
        'real_flock': 11,
        'yearly_eggs': 3146,
        'egg_revenue': 1573.00,
        'feed_cost': 756.00,
        'net_profit': 817.00,
        'funny_quote': "You're making a whopping $817.00 per year! That's almost enough to cover the emergency vet visit when one chicken looks at you funny at 3am. Worth it! 🐔💕",
        'recommended_purchase': 'Premium Feed Upgrade Package + Coop Expansion Kit',
        'meme_image_url': None
    }
    
    generate_chicken_math_pdf(sample_data, "/mnt/user-data/outputs/chicken_math_report_sample.pdf")
