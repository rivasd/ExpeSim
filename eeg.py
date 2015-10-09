
#Figure out which operating system we are running on. if windows, then import the Windows API Library for Python, else try with subprocess
import os.name as OPERATING_SYSTEM
if OPERATING_SYSTEM == 'nt':
	import win32con
	import win32api
	import win32gui
	import win32process
else:
	import subprocess
	
class EEGConnection:
	"""
	This object symbolizes a connection to an EEG Capture software, mainly BioSemi ActiView. 
	It is written as to encapsulate either internal (the EEG software runs on the same computer as this script)
	or external (EEG software runs on second machine and we send signals through parallel port) connections depending of how the constructor is called.
	
	This first version only supports Windows, and is designed to work with Biosemi ActiView software
	
	@todo support for UNIX environments (free software yay!)
	"""
	
	def __init__(self, path=None, same_computer=True):
		"""
		Initialize the EEG recording software at the provided 'path', opening the program
		
		@param path 					{String}: The absolute path to the ActiView executable on your computer,
		@param same_computer	{Boolean}	Sets the type of connection. If true, this constructor will start actiview on this computer and allow
																		us to send keypresses to the program through system calls/pipes/magic god knows.
																		If False, then we assume that ActiView runs on a second computer and that we can send trigger signals through 
																		parallel port. Actiview will not be started here (duh).
																		
		@attention: WARNING. Since the EEG software will be opened as a child process, it MAY close when the calling program exits, and data WILL BE LOST.
								Make sure to account for this in the calling script (e.g. wait for user confirmation before ending). I'm not totally sure this will happen but better safe than sorry!
		"""
		if same_computer == True:
			
			#setup a simple lookup dictionnary for the octal values of the function keys F1 to F9, to make things go faster
			self.FKeys = {
				'F1': win32con.VK_F1,
				'F2': win32con.VK_F2,
				'F3': win32con.VK_F3,
				'F4': win32con.VK_F4,
				'F5': win32con.VK_F5,
				'F6': win32con.VK_F6,
				'F7': win32con.VK_F7,
				'F8': win32con.VK_F8,
				1: win32con.VK_F1,
				2: win32con.VK_F2,
				4: win32con.VK_F3,
				8: win32con.VK_F4,
				16: win32con.VK_F5,
				32: win32con.VK_F6,
				64: win32con.VK_F7,
				128: win32con.VK_F8,
				}
				
			#to try to minimize lookup time, also set some object variables to remember the keyup and keydown event codes
			self.pressKey = win32con.WM_KEYDOWN
			self.releaseKey = win32con.WM_KEYUP
			
			#Attempt to start actiview, and set up this object as kind of a 'pipe' to that program.
			if OPERATING_SYSTEM == 'nt':
				
				if path == None:
					raise RuntimeError('You must provide the path parameter if you want this program to find and run ActiView!')
				#using Windows win32 library, create the process, effectively starting the program ActiView
				#this object now has two members pid and tid, representing the process ID and the thread ID of the ActiView instance
				_, _, self.pid, self.tid = win32process.CreateProcess(
			  None,    # name
			  path,     # command line
			  None,    # process attributes
			  None,    # thread attributes
			  0,       # inheritance flag
			  0,       # creation flag
			  None,    # new environment
			  None,    # current directory
			  win32process.STARTUPINFO ())
				
				#look through all the windows spawned by the actiview process, pass them to _findTargetWindow, which will attache the right one to the 'actiview' field
				win32gui.EnumThreadWindows(self.tid, self._findTargetWindow)
				
				#save a simple trace of what mode what requested, so that future method calls work the right way
				if same_computer:
					self.mode = "internal"
				else:
					self.mode = "external"
			
			
			else:
				#Only windows support for now! sorry :(
				raise RuntimeError("using Actiview on the same machine that runs the experiment is not yet supported on Linux!")
		else:
			#Set this object up as a sender of bytes through parallel port. code later since i'm lazy and not sure how to do that through a USB-to-Parallel adapter that we don't even have yet
			pass
		
	def _findTargetWindow(self, hwnd, *args, **kwargs):
		"""
  	From all the windows created by ActiView, find the window handle (hwnd) of the window that is actually capable of receiving keypresses,
  	and set self.actiview to point to this handle
  	(remember that even if starting ActiView seems to open one "window", it is actually made of multiple window-objects)
  	
  	This function is meant to be used as a parameter to win32gui.EnumThreadWindows
  	"""	
		#careful testing by me has shown that the name of the ActiView window that actually receives keypresses is "IME"
		if win32gui.GetClassName(hwnd) == 'IME':
			self.actiview = hwnd
		else:
			return True
		
	def sendTrigger(self, code=None, key=None, fast=False):
		"""
		send a trigger to the EEG software.
		
		if this connection object was created with same_computer == False, then triggers will be sent as a single byte through the parallel port
		else, triggers will be sent as virtual keypresses to the EEG software process (only Windows + Actiview setup supported so far for this mode)
		
		@param	code	{int}			The byte value to present on the parallel port, used with mode=='external' duh
		@param	key		{String}	A string describing which F-key to simulate pressing on the actiview software, e.g 'F1' or 'F2' (capital F)
		@param	fast	{Boolean}	Flag that can force to skip sanity checks. I realize EEG research is very time sensitive, if you find that your setup could use
														any performance gain it can get, set to true, although on any modern computer I doubt this will make a difference...
		"""
		#simple runtime checks
		if fast:
			if code == None and key == None:
				raise RuntimeError('You must specify either a byte value or a key to send!')
			
			if code != None and key != None:
				raise RuntimeError('specify either a byte or a key, not both! (one param only)')
		
		
		if self.mode == 'internal':
			#Actiview runs as a process on this computer, send a virtual function keypress to it!
			if code:
				if fast and not code in {1, 2, 4, 8, 16, 32, 64, 128}:
					raise RuntimeError('with internal mode, you can only send 8 different values, specifically powers of 2 up to 2**7')
				
				#send the keypress!
				win32api.PostMessage(self.actiview, self.pressKey, self.FKeys[code], self.releaseKey)
					
			
			else: #parameter 'key' was specified
				if fast and not key in {'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'}:
					raise RuntimeError('Acitview only supports keyboard triggers from function keys F1 up to F9')
				
				#send the keypress!
				win32api.PostMessage(self.actiview, self.pressKey, self.FKeys[key], self.releaseKey)
				
		elif self.mode == 'external':
			#Actiview runs somewhere else, send byte through parallel port
			#TODO: figure this out later if it same-computer setup doesn't work as expected
			pass
		