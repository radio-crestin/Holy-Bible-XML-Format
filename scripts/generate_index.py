#!/usr/bin/env python3
"""
Generate bibles.xml for Holy-Bible-XML-Format repository.

This script scans all Bible XML files in the data directory and generates
a bibles.xml file containing metadata for each Bible translation.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def extract_bible_metadata(file_path: Path) -> dict | None:
    """
    Extract metadata from a Bible XML file.

    Uses iterative parsing to efficiently read only the root element
    without loading the entire file into memory.
    """
    try:
        for event, elem in ET.iterparse(str(file_path), events=['start']):
            if elem.tag == 'bible':
                return {
                    'filename': file_path.name,
                    'translation': elem.get('translation', file_path.stem),
                    'status': elem.get('status'),
                    'source_link': elem.get('link'),
                }
            break
    except ET.ParseError as e:
        logger.warning(f"Failed to parse {file_path.name}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Error reading {file_path.name}: {e}")
        return None

    return None


def generate_bibles_xml(
    data_dir: Path,
    output_path: Path,
    repo_url: str,
    tag: str
) -> None:
    """
    Generate bibles.xml containing all Bible translations metadata.
    """
    xml_files = sorted(data_dir.glob('*.xml'))

    if not xml_files:
        logger.error(f"No XML files found in {data_dir}")
        sys.exit(1)

    logger.info(f"Found {len(xml_files)} Bible XML files")

    root = ET.Element('bibles')
    root.set('version', tag)
    root.set('generated', 'true')
    root.set('repository', repo_url)

    metadata_elem = ET.SubElement(root, 'metadata')
    ET.SubElement(metadata_elem, 'total_translations').text = str(len(xml_files))
    ET.SubElement(metadata_elem, 'repository').text = repo_url
    ET.SubElement(metadata_elem, 'tag').text = tag

    translations_elem = ET.SubElement(root, 'translations')

    success_count = 0
    for xml_file in xml_files:
        metadata = extract_bible_metadata(xml_file)

        if metadata is None:
            logger.warning(f"Skipping {xml_file.name} - could not extract metadata")
            continue

        translation_elem = ET.SubElement(translations_elem, 'translation')

        ET.SubElement(translation_elem, 'name').text = metadata['translation']
        ET.SubElement(translation_elem, 'filename').text = metadata['filename']

        download_url = f"{repo_url}/raw/refs/tags/{tag}/data/{metadata['filename']}"
        ET.SubElement(translation_elem, 'download_url').text = download_url

        if metadata['status']:
            ET.SubElement(translation_elem, 'copyright').text = metadata['status']

        if metadata['source_link']:
            ET.SubElement(translation_elem, 'source_link').text = metadata['source_link']

        success_count += 1

    logger.info(f"Successfully processed {success_count}/{len(xml_files)} files")

    xml_string = ET.tostring(root, encoding='unicode')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent='  ', encoding='UTF-8')

    lines = pretty_xml.decode('utf-8').split('\n')
    clean_lines = [line for line in lines if line.strip()]
    final_xml = '\n'.join(clean_lines) + '\n'

    output_path.write_text(final_xml, encoding='utf-8')
    logger.info(f"Generated bibles.xml at {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate bibles.xml for Bible translations'
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path('data'),
        help='Directory containing Bible XML files (default: data)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('bibles.xml'),
        help='Output path for bibles.xml (default: bibles.xml)'
    )
    parser.add_argument(
        '--repo-url',
        type=str,
        default='https://github.com/radio-crestin/Holy-Bible-XML-Format',
        help='GitHub repository URL'
    )
    parser.add_argument(
        '--tag',
        type=str,
        required=True,
        help='Release tag (e.g., v1.0.0)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    script_dir = Path(__file__).parent.parent

    data_dir = args.data_dir
    if not data_dir.is_absolute():
        data_dir = script_dir / data_dir

    output_path = args.output
    if not output_path.is_absolute():
        output_path = script_dir / output_path

    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        sys.exit(1)

    generate_bibles_xml(
        data_dir=data_dir,
        output_path=output_path,
        repo_url=args.repo_url,
        tag=args.tag
    )


if __name__ == '__main__':
    main()
