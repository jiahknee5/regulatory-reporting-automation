# CLAUDE.md - Regulatory Reporting Automation

This file provides guidance to Claude Code when working with the Regulatory Reporting Automation project.

## Quick Start

```bash
# Navigate to project directory
cd /Volumes/project_chimera/projects/regulatory-reporting-automation

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start development server
python src/main.py

# Access API documentation
open http://localhost:8000/docs
```

## Project Overview

The Regulatory Reporting Automation system uses AI to interpret complex regulatory requirements, validate data, and generate compliant reports across multiple jurisdictions. The system reduces manual effort by 80% and virtually eliminates reporting errors.

### Key Technologies
- Python 3.9+
- FastAPI for REST APIs
- TensorFlow/Transformers for ML/NLP
- PostgreSQL for data storage
- Redis for caching
- Docker for containerization

### Architecture Pattern
- Microservices architecture
- Event-driven processing
- AI/ML pipeline integration
- Real-time monitoring

## Development Commands

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_rule_engine.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run integration tests only
pytest tests/integration/ -v
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/ --ignore-missing-imports
```

### Docker Operations
```bash
# Build image
docker build -t regulatory-reporting:latest .

# Run container
docker run -p 8000:8000 regulatory-reporting:latest

# Docker compose
docker-compose up -d
```

## Key Components

### Rule Engine
The rule engine (`3_deliverables/rule_engine.py`) interprets regulatory requirements:
- Loads rules from configuration
- Applies validation, calculation, and transformation rules
- Tracks rule versions and effective dates

### ML Models
Machine learning models (`3_deliverables/ml_models.py`) provide:
- Anomaly detection for data quality
- NLP parsing of regulatory text
- Compliance risk prediction

### Report Generator
The report generator (`3_deliverables/report_generator.py`) creates:
- Multiple output formats (PDF, XML, XBRL, CSV)
- Template-based generation
- Dynamic field mapping

### Compliance Dashboard
Real-time monitoring (`3_deliverables/compliance_dashboard.py`):
- Tracks submission deadlines
- Monitors compliance status
- Generates alerts

## Integration Points

### Data Sources
- ERP systems (SAP, Oracle)
- Financial databases
- Manual uploads
- API integrations

### Regulatory Portals
- SEC EDGAR system
- FCA GABRIEL
- ESMA reporting systems

### Internal Systems
- Authentication via SSO
- Notification services
- Audit logging

## Common Development Tasks

### Adding a New Regulator
1. Add regulator config to `0_admin/regulatory_jurisdictions.json`
2. Create rule set in `config/regulators.yaml`
3. Add submission endpoint in `src/api/submission.py`
4. Create report template
5. Add tests

### Adding a New Report Type
1. Define report structure in templates
2. Create validation rules
3. Add field mappings
4. Implement format converters
5. Update documentation

### Debugging Issues
- Check logs in `logs/regulatory_reporting.log`
- Use debug mode: `LOG_LEVEL=DEBUG python src/main.py`
- Monitor metrics at `/metrics` endpoint
- Check rule application at `/api/v1/validation/trace`

## Performance Optimization

- Use Redis caching for frequently accessed data
- Batch process large reports
- Implement async processing for submissions
- Monitor query performance

## Security Considerations

- All data encrypted in transit (TLS 1.3)
- Sensitive data encrypted at rest
- Role-based access control
- Audit logging for all actions
- Regular security scans

## Troubleshooting

### Common Issues
1. **Rule Loading Failures**
   - Check rule syntax in configuration
   - Verify effective dates
   - Look for conflicting rules

2. **Submission Errors**
   - Verify API credentials
   - Check network connectivity
   - Review submission logs

3. **Performance Issues**
   - Monitor Redis cache hit rate
   - Check database query performance
   - Review async task queue

## DONNA Integration

This project integrates with DONNA for:
- Automated deadline monitoring
- Error pattern recognition
- Submission orchestration
- Compliance trend analysis

## Cognitive Order Assignment

- **Regulatory Interpreter Agent**: Order 5 (Complex interpretation)
- **Data Validation Agent**: Order 4 (Pattern recognition)
- **Report Generation Agent**: Order 3 (Template application)
- **Compliance Monitor Agent**: Order 6 (Predictive analysis)
