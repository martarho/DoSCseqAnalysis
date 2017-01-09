SHELL=/bin/bash -o pipefail
.DELETE_ON_ERROR:
.PHONY: clean

all: star_gene_exon_tagged.bam dge.txt.gz

# Trim reads
{% if project.paired %}
fastq_p1 := $(wildcard {{project.fastq.folder}}/*_1.fastq.gz)
fastq_p2 := $(wildcard {{project.fastq.folder}}/*_2.fastq.gz)
fastq_p1_trimmed := $(fastq_p1:_1.fastq.gz=_1.trimmed.fastq.gz)
fastq_p2_trimmed := $(fastq_p1:_1.fastq.gz=_2.trimmed.fastq.gz)
fastq_basename := $(fastq_p1:_1.fastq.gz=)
bamfiles := $(fastq_p1:_1.fastq.gz=.bam)

$(fastq_p1_trimmed) $(fastq_p2_trimmed) : $(fastq_p1) $(fastq_p2)
    flexbar -r $(word 1,$^) -p $(word 2,$^) -n 4 -t $(word 3,$^)


{% else %}

{% endif %}

# Load genome

# Map


