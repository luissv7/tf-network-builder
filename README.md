# tf-network-builder
A python package I built to create a TF network by querying the different sources from the Harmonizome. It will take a list of gene names and for each gene, it will

The Transcription Factor Interactions are queried from the [Harmonizome](http://amp.pharm.mssm.edu/Harmonizome/)

The recommended citation from their website is:
Rouillard AD, Gundersen GW, Fernandez NF, Wang Z, Monteiro CD, McDermott MG, Ma'ayan A. The harmonizome: a collection of processed datasets gathered to serve and mine knowledge about genes and proteins. Database (Oxford). 2016 Jul 3;2016. pii: baw100.


The data in the directory TF directory, can be downloaded, for example, from [here](http://humantfs.ccbr.utoronto.ca/download.php) and if you use it please properly credit it.


The recommended citation on the website is:
Lambert SA, Jolma A, Campitelli LF, Das PK, Yin Y, Albu M, Chen X, Taipale J, Hughes TR, Weirauch MT.(2018) The Human Transcription Factors. Cell. 172(4):650-665. doi: 10.1016/j.cell.2018.01.029. Review.


1. Check if it is a transcription factor against the list provided by 
Lambert SA, Jolma A, Campitelli LF, Das PK, Yin Y, Albu M, Chen X, Taipale J, Hughes TR, Weirauch MT.(2018) The Human Transcription Factors. Cell. 172(4):650-665. doi: 10.1016/j.cell.2018.01.029. Review.

2. From the harmonizome, it will query the following:
* Transcription target genes from the CHEA Transcription Factor dataset 
Lachmann, A et al. (2010) ChEA: transcription factor regulation inferred from integrating genome-wide ChIP-X experiments. Bioinformatics. 26:2438-44.
* Transcription factor target genes from JASPAR
 Sandelin, A et al. (2004) JASPAR: an open-access database for eukaryotic transcription factor binding profiles. Nucleic Acids Res. 32:D91-4.
Mathelier, A et al. (2014) JASPAR 2014: an extensively expanded and updated open-access database of transcription factor binding profiles. Nucleic Acids Res. 42:D142-7.
* Transcription factor target genes from TRANSFAC, both predicted and curated:
Matys, V et al. (2003) TRANSFAC: transcriptional regulation, from patterns to profiles. Nucleic Acids Res. 31:374-8.
Matys, V et al. (2006) TRANSFAC and its module TRANSCompel: transcriptional gene regulation in eukaryotes. Nucleic Acids Res. 34:D108-10.

* Transcription factor targets from ENCODE:

ENCODE, Project Consortium et al. (2004) The ENCODE (ENCyclopedia Of DNA Elements) Project. Science. 306:636-40.
ENCODE, Project Consortium et al. (2011) A user's guide to the encyclopedia of DNA elements (ENCODE). PLoS Biol. 9:e1001046.

It will only keep the target genes that are in the original list by the user.

3. Finally, it will give you a CSV file that can be visualized in cytoscape. The nodes are transcription factors, and an edge (TF1,TF2) means that TF2 is a target gene for TF1. 




I make no promises that my code works correctly, so make sure you look at it and use at your own risk!
Also, if you do use this, please make sure you accredit the appropriate people.

Any questions should be sent to luis.sordovieira@jax.org









