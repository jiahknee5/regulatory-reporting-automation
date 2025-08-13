# Prompt Workflow - Regulatory Reporting Automation

## Overview

This document describes the prompt workflows for AI agents in the Regulatory Reporting system.

## Regulatory Interpreter Agent Prompts

### Rule Extraction Prompt
```
Given the following regulatory text, extract:
1. Specific requirements with clear actions
2. Data fields that must be reported
3. Deadlines and timing requirements
4. Conditions and exceptions

Text: {regulatory_text}

Format response as JSON with keys: requirements, data_fields, deadlines, conditions
```

### Ambiguity Resolution Prompt
```
The following regulatory requirement is ambiguous:
"{ambiguous_text}"

Context: {context}
Similar rules: {similar_rules}

Provide the most likely interpretation with confidence score.
```

## Data Validation Agent Prompts

### Anomaly Analysis Prompt
```
Analyze the following data for anomalies:
{data_summary}

Historical patterns: {historical_stats}
Expected ranges: {expected_ranges}

Identify any unusual values and explain why they are anomalous.
```

### Correction Suggestion Prompt
```
Data validation error found:
Field: {field_name}
Current value: {current_value}
Error type: {error_type}
Historical values: {historical_values}

Suggest the most likely correct value with explanation.
```

## Report Generation Agent Prompts

### Format Optimization Prompt
```
Convert the following data to {target_format} format:
{source_data}

Requirements:
- Regulator: {regulator}
- Report type: {report_type}
- Specific formatting rules: {format_rules}

Ensure all regulatory requirements are met.
```

## Compliance Monitor Agent Prompts

### Risk Assessment Prompt
```
Assess compliance risk for:
Entity: {entity}
Report type: {report_type}
Current status: {status}
Days until deadline: {days_remaining}
Historical issues: {past_issues}

Provide risk score (0-1) and key risk factors.
```

### Trend Analysis Prompt
```
Analyze compliance trends:
{compliance_history}

Identify:
1. Improving or declining areas
2. Recurring issues
3. Predicted future risks
4. Recommended actions
```

## Workflow Integration

### New Regulation Workflow
1. Regulatory text uploaded
2. Interpreter agent extracts requirements
3. Rule engine updated
4. Validation rules created
5. Report templates configured
6. Monitor agent tracks deadlines

### Report Generation Workflow
1. Data collected from sources
2. Validation agent checks quality
3. Errors corrected with AI assistance
4. Report agent generates output
5. Final validation performed
6. Submission processed

### Compliance Monitoring Workflow
1. Monitor agent tracks all requirements
2. Alerts generated for upcoming deadlines
3. Risk assessment performed
4. Resources allocated based on priority
5. Post-submission analysis conducted
