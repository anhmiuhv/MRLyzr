How to install;

Current for Mac only

1. Install music21 by unzip music21-2.2.1.tar file

   	   - Run the installer.py in the unzipped folder
	   - Follow the instruction to install music21
2. Move chordAnalysis.py to the Downloads folder
3. Unzip shell.zip file and change the file configuration in Max to use the shell object inside the unziped folder
4. Run interface v2.maxpat to use the software or you can use the commandline interface through terminal by running the command:

		python ~/Downloads/chordAnalysis.py -h to open help

   Example:

		python ~/Downloads/chordAnalysis.py test.xml -c to do a chord analysis of test.xml


*Note: For maximum stability, you can import the xml file using Finale and export that xml file using Finale. This is because many xml files have differents offsets, parts and formats.