## PDR, Version v_1.1 <br>
**Requirements: OS Windows 10 and Internet connection.** <br>

**The PDR – Primate Differential Redoxome** is an analytic program that detects unique cysteine residues in a query human protein sequence(s) present only in the primate orthologs of mammals. The program's algorithm uploads query protein sequence(s) onto the BLAST (NCBI)server, retrieves orthologous non-human mammalian sequences, aligns the retrieved and the query sequences, and identifies cysteine residues in the human query, which are present only in the primate orthologues.
How to use PDR program:
1.	Download PDR.zip package from https://github.com/Engel-Lab/PDR site to a working directory by pressing "Code" button and choosing "Download ZIP". Extract package, and launch the program by clicking PDR.exe.
 
2.	Choose Input.xlsx file containing the names and sequences of query human protein(s). The input file might be created by modifying the example Input.xlsx file found in the package.
 
3.	Adjust parameter **'Orthologs number'** to define how many ortholog proteins to be retrieved by BLAST (default value 250).

4.	Adjust parameter **'Sequence identity'** to define the lower limit of protein identity to the query protein. The default value is 80%, which means that only the proteins with sequence identity >80% to the query will be retrieved by BLAST. 
 
5.	Adjust parameter **'Cys conservation'** to set the upper limit of cysteine conservation. The default value is 30%, which means that if the query protein contains at least one cysteine residue, which is present in no more than 30% of the aligned orthologs (at the same position), the query will be subjected to further analysis.

6.	Adjust parameter **'Cys primates'**, which defines the lower limit of primate identity in the conserved orthologues. The default value is 80%, which means that at least 80% of the orthologous, in which a particular aligned cysteine is conserved, are required to be from primates in order the query to be assigned to the PDR.

7.	Press Start.

8.	A new directory with a name identical to that of the Input file is automatically created in the working directory. This directory contains a sub-directory called 'hits', which contains all the proteins that passed the criterion described in Step 5 and their analysis. Within the 'hits' directory, a directory called 'primate_hits' is created, which contains all the proteins that passed the criterion described in Step 6 and their analysis. 
9.	'Summary' file is created and constantly updated in the major directory, which contains names of all the human query proteins analyzed in the project, followed by tab-separated number(s) corresponding to the position(s) of the PDR cysteine residue(s), if found. Residue count corresponds to the query human sequence as specified in Input.xlsx file and begins with the first non-Met residue. The package includes a file, called 'Primates', which contains a list of primate names, which program uses to classify the BLAST hits. If needed, this list can be updated manually.
10.	The accessibility and performance of the BLAST server is the rate-limiting factor in this calculation, which varies on a daily-hourly basis.   
How to cite the PDR program:
Nachiyappan Venkatachalam, Shamchal Bakavayev, Daniel Engel, Zeev Barak, Stanislav Engel, Primate Differential Redoxome (PDR) – a paradigm for understanding neurodegenerative diseases, Redox Biology, 2020, https://doi.org/10.1016/j.redox.2020.101683.
11. Special case: When very few orthologs with a cysteine at the
same position as in the query are found in Step 6 (less than
5), the query is automatically assigned to the PDR.

How to contact us: <br>
E. mail: engels@bgu.ac.il <br><br>
All rights reserved.  
