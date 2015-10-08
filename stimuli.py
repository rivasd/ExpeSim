"""
This module provides classes that assist in fetching the correct stimuli from
the filesystem, and possibly create them on the fly in future versions

Author:
    Daniel Rivas

Creation Date:
    2015-10-05
"""
#just importing some useful functions from the standard libraries...
from os import path, getcwd
import fnmatch

class BaseStim():
  """
  Base class providing standard interface to serve stimuli pairs and accept configuration
  Used to keep repeated code at a minimum.
  """
  
  def __init__(self, basedir=None, difficulties=None, types=None):
    self.basedir = basedir or getcwd()
    self.difficulties = difficulties or [6, 5 ,4]
    self.types = types or ['ll', 'kl', 'lk', 'kk']
    pass
  

class StimFetcher(BaseStim):
  """
  Use this class when stimuli are already made and sit in the filesystem
  """
    
  def __init__(self, searchString=None, *args, **kwargs):
    self.searchString = searchString or "{difficulty}\\{type}\\pair{number}-{type}{distance}{pair}"
    super(StimFetcher, self).__init__(*args, **kwargs)
    