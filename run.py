#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.01), October 04, 2015, at 20:46
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
import ExpSettings
from eeg import EEGConnection
from psychopy import gui, core, visual, data

#Start by opening Actiview




#starting a dialog box to give time to configure actiview

def startExperiment():
	configBox = gui.Dlg(title='waiting for Actiview')
	configBox.addText('click OK when you are sure ActiView is ready')
	configBox.show()
	if configBox.OK == False:
		core.quit()
	
	#this represent the window in which the experiment will be displayed 
	display = visual.Window(size=(1024, 760), fullscr=True, monitor = 'testMonitor', color='white')
	
	#this is a useful object to manage the order of trials and most of all save data! check the PsychoPy documentation to learn
	#how to use it!
	mainHandler = data.ExperimentHandler(version='1.0')
	
#if this file is executed (and not just imported for future use in another script), then simply run the experiment
if __name__ == '__main__':
	startExperiment()
		