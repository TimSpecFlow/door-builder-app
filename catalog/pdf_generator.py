"""
PDF Quote Generator for Door Specifications

Generates professional PDF quotes with company branding,
door specifications, and pricing breakdown.
"""

from io import BytesIO
from datetime import datetime
import uuid

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


class QuoteGenerator:
    """Generate professional PDF quotes for door specifications."""
    
    # Company info - customize these
    COMPANY_NAME = "SpecFlow"
    COMPANY_TAGLINE = "Precision Door Hardware Built to Spec"
    COMPANY_ADDRESS = "Phoenix / Scottsdale, AZ"
    COMPANY_PHONE = "480-243-7837"
    COMPANY_EMAIL = "info@specflow.tech"
    COMPANY_WEBSITE = "www.specflow.tech"
    
    # Colors matching brand
    PRIMARY_COLOR = colors.HexColor('#8b5cf6')  # Purple
    SECONDARY_COLOR = colors.HexColor('#3b82f6')  # Blue
    DARK_COLOR = colors.HexColor('#1e293b')
    LIGHT_COLOR = colors.HexColor('#f8fafc')
    MUTED_COLOR = colors.HexColor('#64748b')
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            'CompanyName',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.PRIMARY_COLOR,
            spaceAfter=4,
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            'Tagline',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.MUTED_COLOR,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            'QuoteTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=self.DARK_COLOR,
            spaceAfter=6,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=self.PRIMARY_COLOR,
            spaceBefore=16,
            spaceAfter=8
        ))
        
        self.styles.add(ParagraphStyle(
            'QuoteNumber',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.MUTED_COLOR,
            alignment=TA_RIGHT
        ))
        
        self.styles.add(ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=self.MUTED_COLOR,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            'Total',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=self.DARK_COLOR,
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        ))
    
    def generate_quote(self, specs: dict, estimate: dict, recommendations: list = None) -> BytesIO:
        """
        Generate a PDF quote from door specifications.
        
        Args:
            specs: Door specification dictionary
            estimate: Estimate with breakdown
            recommendations: Optional list of product recommendations
        
        Returns:
            BytesIO buffer containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.5*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Quote number and date
        quote_number = f"QT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        quote_date = datetime.now().strftime('%B %d, %Y')
        
        # Header section
        story.extend(self._build_header(quote_number, quote_date))
        
        # Door specifications
        story.extend(self._build_specifications(specs))
        
        # Pricing breakdown
        story.extend(self._build_pricing(estimate))
        
        # Product recommendations (if any)
        if recommendations:
            story.extend(self._build_recommendations(recommendations))
        
        # Terms and conditions
        story.extend(self._build_terms())
        
        # Footer
        story.extend(self._build_footer())
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _build_header(self, quote_number: str, quote_date: str) -> list:
        """Build the header section with company info."""
        elements = []
        
        # Company name and tagline
        elements.append(Paragraph(self.COMPANY_NAME, self.styles['CompanyName']))
        elements.append(Paragraph(self.COMPANY_TAGLINE, self.styles['Tagline']))
        
        # Quote info table (right-aligned)
        quote_info = [
            ['Quote Number:', quote_number],
            ['Date:', quote_date],
            ['Valid Until:', (datetime.now().replace(day=1).replace(month=datetime.now().month + 1) 
                             if datetime.now().month < 12 
                             else datetime.now().replace(year=datetime.now().year + 1, month=1, day=1)
                            ).strftime('%B %d, %Y')],
        ]
        
        quote_table = Table(quote_info, colWidths=[1.2*inch, 2*inch])
        quote_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.MUTED_COLOR),
            ('TEXTCOLOR', (1, 0), (1, -1), self.DARK_COLOR),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Create a header table with company info on left and quote info on right
        header_table = Table(
            [[Paragraph(f"{self.COMPANY_ADDRESS}<br/>{self.COMPANY_PHONE}<br/>{self.COMPANY_EMAIL}", 
                       self.styles['Normal']), 
              quote_table]],
            colWidths=[3.5*inch, 3.5*inch]
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 0.2*inch))
        elements.append(HRFlowable(width="100%", thickness=1, color=self.PRIMARY_COLOR))
        elements.append(Spacer(1, 0.15*inch))
        
        # Title
        elements.append(Paragraph("Door Hardware Quote", self.styles['QuoteTitle']))
        
        return elements
    
    def _build_specifications(self, specs: dict) -> list:
        """Build the door specifications section."""
        elements = []
        
        elements.append(Paragraph("Door Specifications", self.styles['SectionHeader']))
        
        # Organize specs into logical groups
        spec_groups = [
            ("Dimensions", [
                ("Width", f"{specs.get('width', 36)}\""),
                ("Height", f"{specs.get('height', 80)}\""),
                ("Thickness", specs.get('thickness', '1-3/4"')),
            ]),
            ("Configuration", [
                ("Door Type", self._format_value(specs.get('doorType', 'interior'))),
                ("Material", self._format_value(specs.get('material', 'wood'))),
                ("Panel Style", self._format_value(specs.get('panelStyle', 'flat'))),
                ("Swing Direction", self._format_value(specs.get('swingDirection', 'left-inswing'))),
            ]),
            ("Frame & Jamb", [
                ("Jamb Width", f"{specs.get('jambWidth', 4.5)}\""),
                ("Jamb Material", self._format_value(specs.get('jambMaterial', 'wood'))),
                ("Rough Opening", f"{specs.get('roughOpeningWidth', 38)}\" × {specs.get('roughOpeningHeight', 82.5)}\""),
            ]),
        ]
        
        # Add glass section if applicable
        if specs.get('hasGlass'):
            spec_groups.append(("Glass Options", [
                ("Glass Type", self._format_value(specs.get('glassType', 'clear'))),
                ("Lite Pattern", self._format_value(specs.get('litePattern', 'full'))),
            ]))
        
        # Add fire rating if applicable
        if specs.get('fireRating') and specs.get('fireRating') != 'none':
            spec_groups.append(("Safety", [
                ("Fire Rating", self._format_value(specs.get('fireRating'))),
            ]))
        
        # Hardware
        hardware_list = specs.get('hardware', [])
        if hardware_list:
            hardware_items = [(self._format_value(h), "✓") for h in hardware_list]
            spec_groups.append(("Hardware Included", hardware_items))
        
        # Build spec tables
        for group_name, items in spec_groups:
            data = [[group_name, '']] + items
            
            table = Table(data, colWidths=[2.5*inch, 4.5*inch])
            table.setStyle(TableStyle([
                # Header row
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, 0), 10),
                ('TEXTCOLOR', (0, 0), (0, 0), self.SECONDARY_COLOR),
                ('SPAN', (0, 0), (1, 0)),
                ('BOTTOMPADDING', (0, 0), (0, 0), 8),
                
                # Data rows
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TEXTCOLOR', (0, 1), (0, -1), self.MUTED_COLOR),
                ('TEXTCOLOR', (1, 1), (1, -1), self.DARK_COLOR),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                ('TOPPADDING', (0, 1), (-1, -1), 4),
                
                # Grid
                ('LINEBELOW', (0, 0), (-1, 0), 0.5, self.MUTED_COLOR),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _build_pricing(self, estimate: dict) -> list:
        """Build the pricing breakdown section."""
        elements = []
        
        elements.append(Paragraph("Pricing Breakdown", self.styles['SectionHeader']))
        
        breakdown = estimate.get('breakdown', {})
        
        pricing_data = [
            ['Item', 'Amount'],
            ['Door Slab', f"${breakdown.get('door_slab', 0):,.2f}"],
            ['Frame & Jamb', f"${breakdown.get('frame_jamb', 0):,.2f}"],
        ]
        
        if breakdown.get('glass', 0) > 0:
            pricing_data.append(['Glass Options', f"${breakdown.get('glass', 0):,.2f}"])
        
        pricing_data.append(['Hardware', f"${breakdown.get('hardware', 0):,.2f}"])
        
        if breakdown.get('fire_rating', 0) > 0:
            pricing_data.append(['Fire Rating Upgrade', f"${breakdown.get('fire_rating', 0):,.2f}"])
        
        if breakdown.get('finish', 0) > 0:
            pricing_data.append(['Finish', f"${breakdown.get('finish', 0):,.2f}"])
        
        pricing_data.append(['', ''])
        pricing_data.append(['Materials Subtotal', f"${breakdown.get('materials_subtotal', 0):,.2f}"])
        pricing_data.append(['Installation Labor', f"${breakdown.get('labor', 0):,.2f}"])
        pricing_data.append(['', ''])
        
        total = estimate.get('estimate', 0)
        pricing_data.append(['TOTAL', f"${total:,.2f}"])
        
        table = Table(pricing_data, colWidths=[5*inch, 2*inch])
        table.setStyle(TableStyle([
            # Header
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.DARK_COLOR),
            ('LINEBELOW', (0, 0), (-1, 0), 1, self.DARK_COLOR),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Data rows
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('TEXTCOLOR', (0, 1), (0, -2), self.MUTED_COLOR),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            
            # Subtotal row
            ('FONTNAME', (0, -4), (-1, -4), 'Helvetica-Bold'),
            ('LINEABOVE', (0, -4), (-1, -4), 0.5, self.MUTED_COLOR),
            
            # Total row
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('TEXTCOLOR', (0, -1), (-1, -1), self.PRIMARY_COLOR),
            ('LINEABOVE', (0, -1), (-1, -1), 1.5, self.PRIMARY_COLOR),
            ('TOPPADDING', (0, -1), (-1, -1), 10),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_recommendations(self, recommendations: list) -> list:
        """Build product recommendations section."""
        elements = []
        
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Recommended Products", self.styles['SectionHeader']))
        
        # Limit to top 5 recommendations
        for rec in recommendations[:5]:
            rec_text = f"<b>{rec.get('name', '')}</b> - {rec.get('category', '')}"
            if rec.get('model_numbers'):
                rec_text += f"<br/><i>Models: {', '.join(rec['model_numbers'][:3])}</i>"
            if rec.get('price_range'):
                rec_text += f" | {rec['price_range']}"
            
            elements.append(Paragraph(rec_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.08*inch))
        
        return elements
    
    def _build_terms(self) -> list:
        """Build terms and conditions section."""
        elements = []
        
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Terms & Conditions", self.styles['SectionHeader']))
        
        terms = [
            "• Quote valid for 30 days from issue date",
            "• 50% deposit required to begin order",
            "• Lead time: 2-4 weeks for standard items",
            "• Installation scheduling upon material arrival",
            "• Warranty: Manufacturer warranty on all products",
            "• Prices subject to change based on final measurements",
        ]
        
        for term in terms:
            elements.append(Paragraph(term, self.styles['Normal']))
            elements.append(Spacer(1, 0.04*inch))
        
        return elements
    
    def _build_footer(self) -> list:
        """Build the footer section."""
        elements = []
        
        elements.append(Spacer(1, 0.4*inch))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=self.MUTED_COLOR))
        elements.append(Spacer(1, 0.1*inch))
        
        footer_text = (
            f"Thank you for choosing {self.COMPANY_NAME}!<br/>"
            f"{self.COMPANY_PHONE} | {self.COMPANY_EMAIL} | {self.COMPANY_WEBSITE}"
        )
        elements.append(Paragraph(footer_text, self.styles['Footer']))
        
        return elements
    
    def _format_value(self, value: str) -> str:
        """Format a value for display (capitalize, replace dashes with spaces)."""
        if not value:
            return "N/A"
        return value.replace('-', ' ').replace('_', ' ').title()
