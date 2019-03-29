Build-Environment
=================

Notes
-----
Note that words which begin with a dollar $ means said word can be ambiguous. A variable, if you will.

To successfully run this project, the following steps must be followed:
+ Make a $build-directory.
	+ mkdir $build-directory
+ Change directory to the $build-directory and create a repos folder.
	+ cd $build-directory
	+ mkdir repos
+ From this point there are a few repositories you need to clone:
	+ git clone $repository-link
	+ The dissertation repo: https://github.com/Monofoot/Dissertation.git
	+ Umoria: https://github.com/dungeons-of-moria/umoria.git
+ Choose branch A or B. Branch A is for running moria2txt and branch B is for txt2unity.

Branch A - moria2txt
--------------------
+ Requirements:
	+ MUST be using Python 3.
+ Running moria2txt is simple. You can either run it as it is, which means the default Moria constants are 
used (though this is messy and often produces unusable maps), or you can use your own variables (recommended).
+ argparse can be used to parse variables to the script.
	+ python moria2txt.py --help
	+ Recommended variables are rooms > 5 and < 15. Anything higher turns out rubbish.
+ The file path in argparse can actually be circumvented by manually piping to a text file, which is sometimes faster.
	+ python moria2txt.py --maxrooms=7 > moriamap.txt

Branch B - txt2unity
--------------------
+ Requirements:
	+ MUST have Unity on Linux machine.
+ Issues:
	+ Unity runs fine on Ubuntu 16.04, not tested on other Unix machines.
	+ The editor will NOT run on Windows as versions mis-match.
	+ Despite this, getting the editor to load on a Unix machine means you can build to both Linux and Windows executables.
	If a build is achieved (not necessary unless you want to run on Windows) then you can port the executable to a USB or harddrive and run from there.
+ Download Unity Hub from the experimental Linux forums.
+ You do not have to sign in.
+ Open the txt2moria folder in /src with the Unity Hub.
+ You should now be in the editor of Unity. Pressing the play button in the center top screen will play the scene.
+ To build the scene into an executable, select File > Build Settings.
	+ Select the platform you want to build on. Both Windows and Linux are safe.
	+ Click build, select directory.
+ There have been issues running this on Windows. I would recommend downloading an experimental Unity Hub and trying it on Linux.
+ If there are any problems please do not hesitate in shooting me a message - I have running versions on my laptop and external hard drive.
