# Bible in XML

Welcome. Here you will find XML Bibles from various languages, created from the past 15 years.
200+ Languages and 1000+ Bible Versions.

Any questions or comments: andrey@beblia.com

Use at your own discretion, no need to ask for permission, no warranty's.

Author: Proud Slave of Christ

Visit our site: https://beblia.com

God Bless. Thank you.

## Repository Structure

```
Holy-Bible-XML-Format/
├── data/                    # All Bible XML files
│   ├── EnglishNIVBible.xml
│   ├── RomanianBible.xml
│   └── ... (1000+ files)
├── scripts/
│   └── generate_index.py    # Script to generate bibles.xml
├── tools/
│   └── django_importer/     # Django import utilities
├── .github/
│   └── workflows/
│       └── generate-index.yml  # GitHub Action for releases
└── README.md
```

## Using bibles.xml

The `bibles.xml` file is automatically generated on each release and provides a structured directory of all available Bible translations.

### Accessing bibles.xml

You can access the latest `bibles.xml` directly from the releases:

```bash
# Get the latest bibles.xml
curl -L https://github.com/radio-crestin/Holy-Bible-XML-Format/releases/latest/download/bibles.xml

# Or from a specific release tag
curl -L https://github.com/radio-crestin/Holy-Bible-XML-Format/raw/refs/tags/v1.0.0/bibles.xml
```

### bibles.xml Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bibles version="v1.0.0" generated="true" repository="https://github.com/radio-crestin/Holy-Bible-XML-Format">
  <metadata>
    <total_translations>1045</total_translations>
    <repository>https://github.com/radio-crestin/Holy-Bible-XML-Format</repository>
    <tag>v1.0.0</tag>
  </metadata>
  <translations>
    <translation>
      <name>English NIV</name>
      <filename>EnglishNIVBible.xml</filename>
      <download_url>https://github.com/radio-crestin/Holy-Bible-XML-Format/raw/refs/tags/v1.0.0/data/EnglishNIVBible.xml</download_url>
    </translation>
    <translation>
      <name>Romanian VDC 1924 (...)</name>
      <filename>RomanianBible.xml</filename>
      <download_url>https://github.com/radio-crestin/Holy-Bible-XML-Format/raw/refs/tags/v1.0.0/data/RomanianBible.xml</download_url>
      <copyright>...</copyright>
      <source_link>https://www.bible.com/bible/191/PSA.10.VDC</source_link>
    </translation>
    <!-- ... more translations -->
  </translations>
</bibles>
```

### Example: Parsing bibles.xml in Python

```python
import xml.etree.ElementTree as ET
import requests

# Fetch the bibles.xml
response = requests.get(
    'https://github.com/radio-crestin/Holy-Bible-XML-Format/releases/latest/download/bibles.xml'
)
root = ET.fromstring(response.content)

# List all translations
for translation in root.findall('.//translation'):
    name = translation.find('name').text
    download_url = translation.find('download_url').text
    print(f"{name}: {download_url}")
```

### Example: Parsing bibles.xml in JavaScript

```javascript
const response = await fetch(
  'https://github.com/radio-crestin/Holy-Bible-XML-Format/releases/latest/download/bibles.xml'
);
const text = await response.text();
const parser = new DOMParser();
const doc = parser.parseFromString(text, 'text/xml');

// List all translations
const translations = doc.querySelectorAll('translation');
translations.forEach(t => {
  const name = t.querySelector('name').textContent;
  const url = t.querySelector('download_url').textContent;
  console.log(`${name}: ${url}`);
});
```

## Bible XML Format

Each Bible file follows this structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bible translation="Translation Name" status="Copyright info" link="Source URL">
  <testament name="Old">
    <book number="1">
      <chapter number="1">
        <verse number="1">In the beginning...</verse>
      </chapter>
    </book>
  </testament>
  <testament name="New">
    <!-- ... -->
  </testament>
</bible>
```

### Attributes

- `translation` (required): Name of the Bible translation
- `status` (optional): Copyright or license information
- `link` (optional): Source URL for the translation

## GitHub Action

The repository includes a GitHub Action that automatically generates `bibles.xml` on each release:

1. **Triggered on**: New release published
2. **What it does**:
   - Scans all XML files in the `data/` directory
   - Extracts metadata from each Bible file
   - Generates `bibles.xml` with versioned download URLs
   - Commits the file to the repository
   - Uploads it as a release artifact

You can also trigger it manually via the "Actions" tab with a specific tag.

## Tools

### Django OSIS Importer

Located in `tools/django_importer/`, this tool imports OSIS-format XML Bibles into a Django database. See the [importer README](tools/django_importer/README.md) for details.
