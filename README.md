MRLyzr
======

A music sheet analysis application

Function

* (beta) chord identifications
* (beta) key change identification
* (beta) simple form identification

Uses Max 7 as the UI

This is created based on Music21. Have to improve a lot in the future. This is just a propotype.



**How to install:**

Current for Mac only

1. Install music21

2. Move chordAnalysis.py to the Downloads folder
3. Unzip shell.zip file and change the file configuration in Max to use the shell object inside the unziped folder
4. Run interface v2.maxpat to use the software or you can use the commandline interface through terminal by running the command:

		python ~/Downloads/chordAnalysis.py -h to open help

   Example:

		python ~/Downloads/chordAnalysis.py test.xml -c to do a chord analysis of test.xml


*Note: For maximum stability, you can import the xml file using Finale and export that xml file using Finale. This is because many xml files have differents offsets, parts and formats.