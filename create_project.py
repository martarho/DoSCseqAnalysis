#!/usr/bin/env python
 
import os, sys
from jinja2 import Environment, FileSystemLoader
from optparse import OptionParser
import tempfile

pathToEnv = "~/"
env = Environment(loader=FileSystemLoader(pathToEnv))
def split_input(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(' '))
  
class dropseq_project(object):
	def __init__(self, obj):
		# PATHS, TOOLS, STATIC
		# Parse binary file
		self.parse_binaries(obj.binaries_file)
		self.quality             = obj.quality        
		self.project_directory   = obj.project_path        
		self.tmpdir              = obj.tmpdir
		self.GenomeDir           = obj.genome_path
		self.nthreads            = obj.threads if obj.threads > 0 else 1
		self.reference           = obj.reference
		self.refflat             = obj.refflat
		self.makefile            = obj.template
		self.project			 = obj.project_name
		self.scale               = obj.scale if obj.scale > 0 else 5000
		# INPUT - Assign names depending on input (priority: Fastq >> BAM)
		if obj.fastq is not None:
			self.pair1           = obj.fastq.split(",")[0]
			self.pair2           = obj.fastq.split(",")[1]
			self.unmapped_bam    = "unmapped.bam"
		else:
			self.pair1           = False
			self.unmapped_bam        = obj.unmapped_bam
		
		self.num_barcodes        = obj.num_barcodes
		self.dge_num_barcodes    = False
	def parse_binaries(self, fl):
		f = open(fl, "r")
		txt = f.read()
		d = dict(item.split("=") for item in txt.split("\n"))
		f.close()
		self.dropseq   = d["DROPSEQ"]
		self.picard    = d["PICARD"]
		self.star      = d["STAR"]
		self.fastqc    = d["FASTQC"]
		self.rscripts    = d["RSCRIPTS"]
	def create_makefile(self):
		template = env.get_template(self.makefile)
		makefile = template.render(dropseq=self)
		f = open(os.path.join(self.project_directory,"Makefile"), "w")
		f.write(makefile)
		f.close()
	def create_folder_structure(self):
		# Create project directory
		if not os.path.exists(self.project_directory):
			os.makedirs(self.project_directory)
		
		# Create subfolders directory
		if not os.path.exists( os.path.join(self.project_directory,"Reports") ):
			os.makedirs( os.path.join(self.project_directory,"Reports") )
		
		
		# Create Tmpdir and assign if not done yet
		if self.tmpdir is None:
			self.tmpdir = tempfile.mkdtemp()            
		elif not os.path.exists(self.tmpdir):
			os.makedirs(self.tmpdir)
        
    
# Parser - Get all the options!

# Directories of executables
parser = OptionParser()
parser.add_option("-b", "--binaries", dest="binaries_file", help="Path to Binaries file",
                  metavar="TMP", type="string", default="~/mybinaries.txt")
# FASTQC?
parser.add_option("-q", "--quality", dest="quality", help="[OPTIONAL]: Run FastQC on fastq/bam files", 
                  metavar="FASTQ", default=False)

# Input files (FASTQ / BAM)
parser.add_option("-f", "--fastq", dest="fastq", help="Input comma separated pairs", 
                  metavar="FASTQ1,FASTQ2", default=None)
parser.add_option("-u", "--unmapped_bam", dest="unmapped_bam", help="Input unmapped BAM", 
                  metavar="BAM", type='string', default=None)

# Project related info
parser.add_option("-d", "--dir", dest="project_path", 
				  help="Project directory (Default: dropseq)", 
                  metavar="DIR", type='string', default="dropseq_run")
parser.add_option("-t", "--tmp", dest="tmpdir", 
				  help="[OPTIONAL]: Temporary directory (Default: Randomly generated)",metavar="TMP", type="string", default=None)
parser.add_option("-g", "--genome", dest="genome_path", help="Genome path",
                  metavar="DIR", type="string")
parser.add_option("-p", "--n_threads", dest="threads", 
				  help="Number of threads (for STAR/Samtools; default: 10)", 
				  type=int, default=10)
parser.add_option("-r", "--reference", dest="reference", help="Genome fasta reference",
                  metavar="FA", type="string")
parser.add_option("-a", "--refflat_annotation", dest="refflat", 
				  help="RefFlat annotation", type=str)
parser.add_option("-m", "--make_template", dest="template", 
				  help="Template to use (default: dropseq.make)", type=str, default="dropseq.make")

parser.add_option("-s", "--n_barcodes_synthesis_error", dest="num_barcodes", 
				  help="[OPTIONAL]: Number of barcodes to consider when doing bead synthesis error correction", type=int, default=12000)
parser.add_option("-e", "--dge_barcodes", dest="dge_num_barcodes", 
				  help="[OPTIONAL]: Fix number of barcodes to use for DGE (Default: automatically set by knee-threshold finding) ",default=False)
parser.add_option("-n", "--name", dest="project_name", 
				  help="[OPTIONAL]: scale ",default="dropseq")
parser.add_option("--scale", dest="scale", 
				  help="[OPTIONAL]: scale",default=5000)
(opts, args) = parser.parse_args()

if not opts.genome_path:
	parser.error('Genome path required!')
if not opts.reference:
	parser.error('Reference fasta required!')
if not opts.refflat:
	parser.error('ReFflat annotation file required!')
if opts.fastq is None and opts.unmapped_bam is None:
	parser.error('At least an input file needed! (Fastq or BAM file)')

dropseq = dropseq_project(opts)
 
def main():
    
    # Load parameters
    dropseq = dropseq_project(opts)

    # Create folder structure
    dropseq.create_folder_structure()
    
    # Create makefile
    dropseq.create_makefile()
 
########################################
 
if __name__ == "__main__":
    main()

