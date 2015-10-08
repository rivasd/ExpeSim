"""
Holds multiple global constants that set the various parameters in the experiment

Author:
    Daniel Rivas

Creation date:
    2015-10-04
    
Good luck fellow researcher :)
"""

EXPERIMENTAL_SETTINGS = {
		'nb_of_repeats': 30, #how many trials of each of the 4 types to present to subjects ( do x4 to get total number of trials) 
		
		#this sets the codes that the experiment and data will use to name our 2 categories, set to the letters L and K by default
		'1st_category_label': 'L',
		'2nd_category_label': 'K',
		
		#should we try to recover the vectorial distance of a pair from the name of the images? e.g from a stim named "pair40-L5.png"
		#we could try to recover that it is part of a pair that has exactly 5 attributes set to different values
		'gather_distances': True,
		
		#this parametrized string tells the program how to construct the path to the appropriate image file for a given request
		#components between curly braces are meant to be filled with the request parameters
		#e.g. the default string below, once filled with the request parameters, will create a path like: currentdirectory\6\LK\pair23-lk3B.png
		#this path will be used to try to load the image file, make sure it actually leads to the right image!
		'search_path': "{difficulty}\\{type}\\pair{number}-{type}{distance}{pair}.png",
		
		#the language to display the instructions for this run
		'language': 'english'
}

INSTRUCTIONS_FR = {
		
	}

INSTRUCTIONS_EN = {
									
	}