# DoSCseqAnalysis
## What is it?
Create and populate Makefiles to execute single cell pipelines (and potentially other kind of high-throughput pipelines) using jinja2 templates and Make

## How it works?
python create_project.py -h
Usage: create_project.py [options]

Options:
  -h, --help            show this help message and exit
  -b TMP, --binaries=TMP
                        Path to Binaries file
  -q FASTQ, --quality=FASTQ
                        [OPTIONAL]: Run FastQC on fastq/bam files
  -f FASTQ1,FASTQ2, --fastq=FASTQ1,FASTQ2
                        Input comma separated pairs
  -u BAM, --unmapped_bam=BAM
                        Input unmapped BAM
  -d DIR, --dir=DIR     Project directory (Default: dropseq)
  -t TMP, --tmp=TMP     [OPTIONAL]: Temporary directory (Default: Randomly
                        generated)
  -g DIR, --genome=DIR  Genome path
  -p THREADS, --n_threads=THREADS
                        Number of threads (for STAR/Samtools; default: 10)
  -r FA, --reference=FA
                        Genome fasta reference
  -a REFFLAT, --refflat_annotation=REFFLAT
                        RefFlat annotation
  -m TEMPLATE, --make_template=TEMPLATE
                        Template to use (default: dropseq.make)
  -s NUM_BARCODES, --n_barcodes_synthesis_error=NUM_BARCODES
                        [OPTIONAL]: Number of barcodes to consider when doing
                        bead synthesis error correction
  -e DGE_NUM_BARCODES, --dge_barcodes=DGE_NUM_BARCODES
                        [OPTIONAL]: Fix number of barcodes to use for DGE
                        (Default: automatically set by knee-threshold finding)
  -n PROJECT_NAME, --name=PROJECT_NAME
  --scale=SCALE         [OPTIONAL]: scale
