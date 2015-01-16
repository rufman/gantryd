import docker
from docker.utils import kwargs_from_env
import datetime
import socket
import logging

from termcolor import colored, cprint

def enum(*sequential, **named):
    """ Represent an enumeration. Originally from: http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

ReportLevels = enum(BACKGROUND=-2, EXTRA=-1, NORMAL=0, IMPORTANT=1)

client = docker.Client(base_url='unix://var/run/docker.sock')

def setUpMacDockerClient():
    global client
    client = docker.Client(**kwargs_from_env())

def pickUnusedPort():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('localhost', 0))
  addr, port = s.getsockname()
  s.close()
  return port

def report(msg, level=ReportLevels.NORMAL, project=None, component=None):
  """ Reports a message to the console. """
  print_string = ''
  if component:
    print_string += colored('[' + component.getName() + '] ', 'green')

  color = 'white'
  attrs = []

  if level == ReportLevels.BACKGROUND or level == ReportLevels.EXTRA:
    attrs.append('dark')
  elif level == ReportLevels.IMPORTANT:
    attrs.append('bold')

  if level == ReportLevels.BACKGROUND:
    dtstring = datetime.datetime.now().strftime("%d/%m/%Y %I:%M%p")
    msg = dtstring + ' | ' + msg

  print_string += colored(msg, color, attrs=attrs)
  print print_string

def fail(reason, project=None, component=None, exception=None):
  """ Fails due to some unexpected error. """
  raise Exception(reason)

def getDockerClient():
  """ Returns the docker client. """
  return client

def setUpLogging(logger):
  logger.setLevel(logging.DEBUG)
  fh = logging.FileHandler('gantryd.log')
  fh.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(formatter)
  logger.addHandler(fh)
