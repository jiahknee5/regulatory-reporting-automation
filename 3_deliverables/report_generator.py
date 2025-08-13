"""
Report Generator Module
Creates regulatory reports in various formats
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import xml.etree.ElementTree as ET
from io import BytesIO
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import logging

logger = logging.getLogger(__name__)

class ReportFormat:
    PDF = "pdf"
    XML = "xml"
    XBRL = "xbrl"
    CSV = "csv"
    JSON = "json"
    HTML = "html"

class ReportGenerator:
    """Generate regulatory reports in multiple formats"""
    
    def __init__(self):
        self.templates = {}
        self.formatters = {
            ReportFormat.PDF: self._generate_pdf,
            ReportFormat.XML: self._generate_xml,
            ReportFormat.XBRL: self._generate_xbrl,
            ReportFormat.CSV: self._generate_csv,
            ReportFormat.JSON: self._generate_json,
            ReportFormat.HTML: self._generate_html
        }
        
    def generate_report(self, 
                       report_type: str,
                       data: Dict[str, Any],
                       format: str,
                       metadata: Optional[Dict] = None) -> bytes:
        """Generate report in specified format"""
        logger.info(f"Generating {report_type} report in {format} format")
        
        if format not in self.formatters:
            raise ValueError(f"Unsupported format: {format}")
            
        # Apply template if available
        if report_type in self.templates:
            data = self._apply_template(report_type, data)
            
        # Generate report
        report_data = self.formatters[format](report_type, data, metadata or {})
        
        logger.info(f"Report generated successfully: {len(report_data)} bytes")
        return report_data
        
    def _apply_template(self, report_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply report template to structure data"""
        template = self.templates[report_type]
        structured_data = {}
        
        for section, fields in template.items():
            structured_data[section] = {}
            for field in fields:
                if field in data:
                    structured_data[section][field] = data[field]
                    
        return structured_data
        
    def _generate_pdf(self, report_type: str, data: Dict[str, Any], metadata: Dict) -> bytes:
        """Generate PDF report"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"{report_type} Report", styles['Title'])
        story.append(title)
        
        # Metadata
        meta_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
        meta_text += f"Period: {metadata.get('period', 'N/A')}<br/>"
        meta_text += f"Entity: {metadata.get('entity', 'N/A')}"
        story.append(Paragraph(meta_text, styles['Normal']))
        story.append(Paragraph("<br/><br/>", styles['Normal']))
        
        # Data sections
        for section, section_data in data.items():
            story.append(Paragraph(section.replace('_', ' ').title(), styles['Heading2']))
            
            if isinstance(section_data, dict):
                # Create table for dict data
                table_data = [[k.replace('_', ' ').title(), str(v)] 
                             for k, v in section_data.items()]
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(t)
            else:
                story.append(Paragraph(str(section_data), styles['Normal']))
                
            story.append(Paragraph("<br/>", styles['Normal']))
            
        # Build PDF
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
        
    def _generate_xml(self, report_type: str, data: Dict[str, Any], metadata: Dict) -> bytes:
        """Generate XML report"""
        root = ET.Element("Report")
        root.set("type", report_type)
        root.set("generated", datetime.now().isoformat())
        
        # Add metadata
        meta_elem = ET.SubElement(root, "Metadata")
        for key, value in metadata.items():
            elem = ET.SubElement(meta_elem, key)
            elem.text = str(value)
            
        # Add data
        data_elem = ET.SubElement(root, "Data")
        self._dict_to_xml(data, data_elem)
        
        # Convert to string
        xml_str = ET.tostring(root, encoding='unicode', method='xml')
        return xml_str.encode('utf-8')
        
    def _dict_to_xml(self, data: Dict, parent: ET.Element):
        """Convert dictionary to XML elements"""
        for key, value in data.items():
            elem = ET.SubElement(parent, key)
            if isinstance(value, dict):
                self._dict_to_xml(value, elem)
            elif isinstance(value, list):
                for item in value:
                    item_elem = ET.SubElement(elem, "Item")
                    if isinstance(item, dict):
                        self._dict_to_xml(item, item_elem)
                    else:
                        item_elem.text = str(item)
            else:
                elem.text = str(value)
                
    def _generate_xbrl(self, report_type: str, data: Dict[str, Any], metadata: Dict) -> bytes:
        """Generate XBRL report"""
        # Simplified XBRL - in production use proper XBRL library
        xbrl_instance = f"""<?xml version="1.0" encoding="UTF-8"?>
<xbrl xmlns="http://www.xbrl.org/2003/instance"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:xbrli="http://www.xbrl.org/2003/instance"
      xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
      xmlns:item="http://example.com/regulatory/items">
      
    <context id="c1">
        <entity>
            <identifier scheme="http://www.sec.gov/CIK">{metadata.get('entity_id', '0000000000')}</identifier>
        </entity>
        <period>
            <instant>{metadata.get('period_end', datetime.now().date().isoformat())}</instant>
        </period>
    </context>
    
    <unit id="usd">
        <measure>iso4217:USD</measure>
    </unit>
"""
        
        # Add data items
        for key, value in data.items():
            if isinstance(value, (int, float)):
                xbrl_instance += f'
    <item:{key} contextRef="c1" unitRef="usd" decimals="0">{value}</item:{key}>'
                
        xbrl_instance += """
</xbrl>"""
        
        return xbrl_instance.encode('utf-8')
        
    def _generate_csv(self, report_type: str, data: Dict[str, Any], metadata: Dict) -> bytes:
        """Generate CSV report"""
        # Flatten nested data
        flattened = self._flatten_dict(data)
        
        # Create DataFrame
        df = pd.DataFrame([flattened])
        
        # Add metadata columns
        for key, value in metadata.items():
            df[f'meta_{key}'] = value
            
        # Convert to CSV
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        
        return csv_buffer.getvalue()
        
    def _generate_json(self, report_type: str, data: Dict[str, Any], metadata: Dict) -> bytes:
        """Generate JSON report"""
        report = {
            "report_type": report_type,
            "generated": datetime.now().isoformat(),
            "metadata": metadata,
            "data": data
        }
        
        return json.dumps(report, indent=2).encode('utf-8')
        
    def _generate_html(self, report_type: str, data: Dict[str, Any], metadata: Dict) -> bytes:
        """Generate HTML report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{report_type} Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .metadata {{ background-color: #f9f9f9; padding: 10px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>{report_type} Report</h1>
    
    <div class="metadata">
        <h2>Report Information</h2>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Period:</strong> {metadata.get('period', 'N/A')}</p>
        <p><strong>Entity:</strong> {metadata.get('entity', 'N/A')}</p>
    </div>
"""
        
        # Add data sections
        for section, section_data in data.items():
            html += f"<h2>{section.replace('_', ' ').title()}</h2>"
            
            if isinstance(section_data, dict):
                html += "<table>"
                html += "<tr><th>Field</th><th>Value</th></tr>"
                for key, value in section_data.items():
                    html += f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>"
                html += "</table>"
            else:
                html += f"<p>{section_data}</p>"
                
        html += """
</body>
</html>"""
        
        return html.encode('utf-8')
        
    def _flatten_dict(self, data: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Flatten nested dictionary"""
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
        
    def register_template(self, report_type: str, template: Dict[str, List[str]]):
        """Register report template"""
        self.templates[report_type] = template

# Export generator instance
report_generator = ReportGenerator()
