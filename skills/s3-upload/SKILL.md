---
name: s3-upload
description: "Upload files to AWS S3 (ricardo-dashboard bucket) and return permanent URLs. Use when user needs to publish files, share report assets, or create downloadable links."
---

# S3 Upload Skill

Upload files to AWS S3 with stable, permanent URLs for use in GTA reports and publications.

## Usage

```
/s3-upload <file> --folder <s3-folder>
/s3-upload results/chartbook.pdf --folder reports/eu-countermeasures
/s3-upload charts/*.png --folder reports/eu-countermeasures/charts
```

## Prerequisites

Requires credentials in `jf-thought/.env`:
```
AWS_ACCESS_KEY_ID=<your_key>
AWS_SECRET_ACCESS_KEY=<your_secret>
AWS_REGION=eu-west-1
S3_BUCKET_NAME=ricardo-dashboard
```

Also requires: `pip install boto3`

## S3 Configuration

| Setting | Value |
|---------|-------|
| Bucket | `ricardo-dashboard` |
| Region | `eu-west-1` |
| ACL | `public-read` |
| URL Pattern | `https://ricardo-dashboard.s3.eu-west-1.amazonaws.com/<key>` |

## Behavior

When invoked, this skill:

1. **Loads AWS credentials** from `jf-thought/.env`
2. **Uploads files** to S3 with public-read access
3. **Uses stable keys** (not timestamped) for permanent URLs
4. **Returns public URLs** for use in reports

## Implementation

### Step 1: Load AWS Credentials

```python
from pathlib import Path

def load_aws_config():
    # Look for .env in jf-thought directory
    env_file = Path(__file__).resolve()
    while env_file.name != 'jf-thought' and env_file.parent != env_file:
        env_file = env_file.parent
    env_file = env_file / ".env"
    
    config = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return {
        'access_key': config.get('AWS_ACCESS_KEY_ID'),
        'secret_key': config.get('AWS_SECRET_ACCESS_KEY'),
        'region': config.get('AWS_REGION', 'eu-west-1'),
        'bucket': config.get('S3_BUCKET_NAME', 'ricardo-dashboard'),
    }
```

### Step 2: Create S3 Client

```python
import boto3

def get_s3_client(config):
    return boto3.client(
        's3',
        aws_access_key_id=config['access_key'],
        aws_secret_access_key=config['secret_key'],
        region_name=config['region']
    )
```

### Step 3: Upload File

```python
def upload_file(file_path, s3_key, config):
    """Upload a file to S3 with public-read access."""
    s3_client = get_s3_client(config)
    
    s3_client.upload_file(
        str(file_path),
        config['bucket'],
        s3_key,
        ExtraArgs={'ACL': 'public-read'}
    )
    
    public_url = f"https://{config['bucket']}.s3.{config['region']}.amazonaws.com/{s3_key}"
    return public_url
```

## URL Naming Convention

Use stable, descriptive S3 keys (not timestamped) for permanent URLs:

### Good (Stable URLs)
```
reports/eu-countermeasures-chartbook/GTA-EU-Countermeasures-Chartbook.pdf
reports/eu-countermeasures-chartbook/GTA-EU-Countermeasures-Data.zip
reports/eu-countermeasures-chartbook/charts/Figure_01_wave_schedule.png
```

### Avoid (Timestamped URLs)
```
reports/1768980411802_EU-Countermeasures.pdf  # Timestamp prefix breaks permanence
reports/upload_20260121_chartbook.pdf         # Date in filename
```

## Common Upload Patterns

### Single PDF Report
```python
url = upload_file(
    "results/chartbook/GTA - EU Countermeasures.pdf",
    "reports/eu-countermeasures/GTA-EU-Countermeasures-Chartbook.pdf",
    config
)
# https://ricardo-dashboard.s3.eu-west-1.amazonaws.com/reports/eu-countermeasures/GTA-EU-Countermeasures-Chartbook.pdf
```

### Data Files as ZIP
```python
import zipfile

# Create ZIP
with zipfile.ZipFile("data_package.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
    for xlsx in Path("results").glob("*.xlsx"):
        zf.write(xlsx, xlsx.name)

# Upload
url = upload_file(
    "data_package.zip",
    "reports/eu-countermeasures/GTA-EU-Countermeasures-Data.zip",
    config
)
```

### Multiple Charts
```python
chart_urls = {}
for chart in Path("results/charts").glob("Figure_*.png"):
    s3_key = f"reports/eu-countermeasures/charts/{chart.name}"
    chart_urls[chart.stem] = upload_file(chart, s3_key, config)
```

## Full Upload Script Template

```python
#!/usr/bin/env python3
"""Upload project files to S3 with stable URLs."""

import zipfile
from pathlib import Path
import boto3

def load_aws_config():
    jf_thought = Path(__file__).resolve()
    while jf_thought.name != 'jf-thought' and jf_thought.parent != jf_thought:
        jf_thought = jf_thought.parent
    env_file = jf_thought / ".env"
    
    config = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return {
        'access_key': config['AWS_ACCESS_KEY_ID'],
        'secret_key': config['AWS_SECRET_ACCESS_KEY'],
        'region': config.get('AWS_REGION', 'eu-west-1'),
        'bucket': config.get('S3_BUCKET_NAME', 'ricardo-dashboard'),
    }


def upload_file(file_path, s3_key, config):
    s3 = boto3.client(
        's3',
        aws_access_key_id=config['access_key'],
        aws_secret_access_key=config['secret_key'],
        region_name=config['region']
    )
    
    print(f"Uploading {file_path.name}...")
    s3.upload_file(str(file_path), config['bucket'], s3_key, ExtraArgs={'ACL': 'public-read'})
    
    url = f"https://{config['bucket']}.s3.{config['region']}.amazonaws.com/{s3_key}"
    print(f"  ✓ {url}")
    return url


def main():
    config = load_aws_config()
    S3_FOLDER = "reports/my-project"
    
    results_dir = Path("results")
    urls = {}
    
    # 1. Upload PDF
    pdf = results_dir / "report.pdf"
    if pdf.exists():
        urls['pdf'] = upload_file(pdf, f"{S3_FOLDER}/Report.pdf", config)
    
    # 2. Create and upload data ZIP
    data_zip = results_dir / "data.zip"
    xlsx_files = list(results_dir.glob("*.xlsx"))
    if xlsx_files:
        with zipfile.ZipFile(data_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for f in xlsx_files:
                zf.write(f, f.name)
        urls['data'] = upload_file(data_zip, f"{S3_FOLDER}/Data.zip", config)
    
    # 3. Upload charts
    for chart in results_dir.glob("*.png"):
        urls[chart.stem] = upload_file(chart, f"{S3_FOLDER}/charts/{chart.name}", config)
    
    print("\nAll URLs:")
    for name, url in urls.items():
        print(f"  {name}: {url}")
    
    return urls


if __name__ == "__main__":
    main()
```

## Integration with GTA Reports

After uploading, register attachments in the GTA database:

```python
import pymysql

def register_attachment(report_id, file_title, file_url, type_id=1):
    """
    type_id: 1 = Report File, 2 = Appendix
    """
    conn = pymysql.connect(
        host='gtaapi.cp7esvs8xwum.eu-west-1.rds.amazonaws.com',
        user='gtaapi',
        password='<from_env>',
        database='gtaapi'
    )
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO core_report_file_log (file_title, file_url, report_id, type_id)
                VALUES (%s, %s, %s, %s)
            """, (file_title, file_url, report_id, type_id))
        conn.commit()
    finally:
        conn.close()

# Example
register_attachment(364, "EU Countermeasures Chartbook (PDF)", urls['pdf'], type_id=1)
register_attachment(364, "Data Files (ZIP)", urls['data'], type_id=2)
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `NoCredentialsError` | AWS keys not in `.env` | Add AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY |
| `AccessDenied` | Invalid credentials or no bucket access | Verify credentials have S3 write permission |
| `FileNotFoundError` | Local file doesn't exist | Check file path |
| `SSLError` | Network/proxy issues | Try `--trusted-host` flags if using pip |

## Existing Examples

Reference implementation:
```
jf-thought/sgept-analytics/data-queries/250801 Relative Trump Tariff Advantage/code/upload_results.py
jf-thought/sgept-analytics/eu-tariff-barrier-estimates/code/countermeasures/upload_and_attach.py
```

## Proactive Invocation

Suggest this skill when:
1. User has files to share publicly (PDFs, data files, charts)
2. User needs permanent URLs for report attachments
3. User is preparing to publish analysis to GTA
4. User mentions uploading to S3 or AWS
5. User wants to make files available for download
