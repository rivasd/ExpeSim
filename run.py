#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.01), October 04, 2015, at 20:46
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
from ExpSettings import EXPERIMENTAL_SETTINGS, INSTRUCTIONS_EN, INSTRUCTIONS_FR
from eeg import EEGConnection
from psychopy import gui, core, visual, data

#Start by opening Actiview




#starting a dialog box to give time to configure actiview

def startExperiment():
	startEEGBox = gui.Dlg(title='waiting for Actiview')
	startEEGBox.addText('click OK when you are sure ActiView is ready')
	startEEGBox.show()
	if startEEGBox.OK == False:
		core.quit()
	
	#now that we made sure that actiview works and receives our triggers, display another dialog box
	#that will allow us to review and/or set the experimental settings for the run
	configBox = gui.Dlg(title='Choose settings for this run')
	configBox.addField('# of repeats', EXPERIMENTAL_SETTINGS['nb_of_repeats'], tip="how many trials per type of trials. remember there are 4 types of trials")
	configBox.addField(label='Language', initial = EXPERIMENTAL_SETTINGS['language'], color='', choices= ['english', 'french'])
	configBox.addField(label='Get distances from file name?', initial=True, color='', choices=[True, False], tip='set to true if the names of the stimuli contain a hint to the vectorial distance of the pair. We will recover it with using curly brace parameters on the searchstring setting below')
	configBox.addField(label="Search String", initial=EXPERIMENTAL_SETTINGS['search_path'], color='', tip="read the READMD.txt or try me: rivasdaniel1992@gmail.com if you are not sure :)")
	configBox.addField(label="Code for 1st category", initial=EXPERIMENTAL_SETTINGS['1st_category_label'])
	handle = configBox.addField(label="Code for 2nd category", initial=EXPERIMENTAL_SETTINGS['2nd_category_label'])
	configBox.show()
	
	#DEBUG STATEMENT
	print configBox.data
	print handle
	#this represent the window in which the experiment will be displayed 
	display = visual.Window(size=(1024, 760), fullscr=True, monitor = 'testMonitor', color='white')
	
	#this is a useful object to manage the order of trials and most of all save data! check the PsychoPy documentation to learn
	#how to use it!
	mainHandler = data.ExperimentHandler(version='1.0')
	
#if this file is executed (and not just imported for future use in another script), then simply run the experiment
if __name__ == '__main__':
	startExperiment()
		