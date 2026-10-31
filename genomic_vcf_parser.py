"""Genomic VCF Variant Parser CLI
Author: Irfan Chowdhury
Description: Parses VCF files line-by-line, extracts variant metrics, and outputs structured CSVs.
"""

import argparse
import sys

def parse_vcf(vcf_path: str, output_csv: str):
    """Parses a VCF file, computes allele counts, identifies biallelic variants, and exports to CSV."""
    nb_biallelic = 0

    try:
        with open(vcf_path, "r", encoding="utf-8") as vcf_file, open(output_csv, "w", encoding="utf-8") as csv_file:
            # Write CSV header
            csv_file.write("variant_id,nb_alleles,ref,alts\n")

            for line in vcf_file:
                # Skip VCF metadata and header lines
                if line.startswith("#"):
                    continue

                # Extract fields of interest
                fields = line.rstrip().split("\t")
                if len(fields) < 5:
                    continue  # Skip malformed lines

                chrom = fields[0]
                pos = fields[1]
                ref = fields[3]
                alt = fields[4]

                # Create variation ID (chrom:pos:ref)
                variant_id = f"{chrom}:{pos}:{ref}"

                # Calculate total number of alleles (reference + alternatives)
                alts = alt.split(",")
                nb_alleles = 1 + len(alts)

                # Calculate total biallelic variant
                if nb_alleles == 2:
                    nb_biallelic += 1

                # Write variant information to the CSV file
                alts_csv = "/".join(alts)
                csv_file.write(f"{variant_id},{nb_alleles},{ref},{alts_csv}\n")

        print(f"Parsing complete. Results successfully saved to '{output_csv}'.")
        print("Biallelic variation count:", nb_biallelic)

    except FileNotFoundError:
        print(f"Error: The file '{vcf_path}' could not be found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during VCF processing: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Parse a VCF file and export variant summaries to a CSV file.")
    parser.add_argument("-i", "--input", required=True, help="Path to input VCF file")
    parser.add_argument("-o", "--output", default="results.csv", help="Path to output CSV file (default: results.csv)")
    
    args = parser.parse_args()
    parse_vcf(args.input, args.output)

if __name__ == "__main__":
    main()