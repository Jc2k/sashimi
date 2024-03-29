__author__ = 'Richard Mitchell <richard.mitchell@isotoma.com>'
__docformat__ = 'restructuredtext en'

import os
import re

class PythonScript:
    """ This class is designed to run .py, .cpy & .vpy files from Zope / Plone
        with the bare minimum of code for unit testing purposes. Beware that
        using this script runner will not flag up errors in incorrect use of
        restricted python. This also means that use of this could result in
        nasty things happening, though if your unit tests have nasty side-
        effects, that's your own fault.

        Initialisation returns a callable object, which may be called with
        keyword parameters as if it were called from the web with those
        parameters.
    """

    def __init__(self, filename, id=None, container=None, context=None, namespace=None, script=None, traverse_subpath=None, state=None, g={}):
        """ Wraps an existing Plone-style python script and makes it runnable.
            filename is the full path to the file which we should wrap
            id=None  is the id given to the function. By default will be set to
                     the basename of the file, less the extension and any
                     invalid characters.
            container, context, namespace, script, traverse_subpath, state may
                     all be substituted with values which they should take when
                     the script is run.
            g={}     a dictionary of variables which should be global when the
                     script is run.
        """
        # Try to open the file before we proceed, that way we raise any
        # filesystem errors early.
        f = open(filename)
        f.close()

        self.__filename = filename
        self.__fileheader = []
        self.__signature = {}
        self.__filecontents = []
        self.__compiled_code = None
                          # strip the extension and any invalid characters for a function id
        self.__id = id or re.sub(r'[^\w_]', '', os.path.basename(filename).rsplit('.',1)[0])
        self.container = container
        self.context = context
        self.namespace = namespace
        self.script = script
        self.traverse_subpath = traverse_subpath
        self.state = state
        self.__parameters = {}
        self.__use_kwargs = ''

        self.__setglobals = g
        self.__globals = {}

    def _parseHeaders(self):
        """ Parses the binds and parameters set in the comments in the header of
            Zope/Plone scripts and stores them in the object for later.
        """
        self.__globals = dict([(k, '__me__._getGlobal("%s")'%k) for k in self.__setglobals])
        for line in self.__fileheader:
            line = line[2:].strip()
            # binds
            if line.startswith('bind'):
                match = re.match(r'^bind\s+([^\s=]+)\s*=\s*([^\s]+)$', line)
                if match:
                    key, value = match.groups()
                    value = 'getattr(__me__, "%(v)s", "%(v)s")' % {'v': value}
                    self.__globals.setdefault(key, value)
            # parameters
            if line.startswith('parameters'):
                match = re.match(r'^parameters\s*=\s*(.*?)\s*$', line)
                if match:
                    params = match.group(1)
                    kwargs = re.search(',?(\*\*[^,$]+)\w*(,|$)', params)
                    if kwargs:
                        self.__use_kwargs = kwargs.group(1)
                        params = re.sub(',?\*\*[^,$]+\w*(,|$)', '\\1', params)
                    self.__signature = eval('dict('+params+')')


    def reloadFile(self):
        """ Reloads the script contents from the file system.
        """
        self.__fileheader = []
        self.__filecontents = []
        f = open(self.__filename)
        for line in f:
            if line.startswith('##'):
                self.__fileheader.append(line.strip())
            else:
                self.__filecontents.append(line)
        f.close()
        self._parseHeaders()
        self._compileFunction()

    def _getGlobal(self, n):
        """ Used within the script wrapper function to retrieve globals set at
            initialization.
        """
        return self.__setglobals[n]

    def _compileFunction(self):
        """ Wraps the script code in a function and then our own wrapper
            function and stores it in the object for execution later.
        """
        # set the function signature up, based on the parameters from the header
        sig = ','.join([k+'='+v.__repr__() for k,v in self.__signature.items()])
        if self.__use_kwargs:
            sig = (sig and sig+', ' or '') + self.__use_kwargs
        f = ['def ' + self.__id + '('+sig+'):\n']

        # apply indent
        for line in self.__filecontents:
            f.append('    '+line)

        # wrap in our own function which will set up 'globals'
        code = 'def compiled_code(__me__, **kwargs):\n' +                                            \
               '    '+'    '.join(['global %s\n' % k for k in self.__globals])+'    \n' +            \
               '    '+'    '.join(['%s=%s\n' % (k,v) for k, v in self.__globals.items()])+'    \n' + \
               '    '+'    '.join(f)+'    \n' +                                                      \
               '    \n' +                                                                            \
               '    return '+self.__id+'(**kwargs)\n'

        exec code
        self.__compiled_code = compiled_code

    def _runFunction(self, **kwargs):
        """ Passes the keyword arguments to the script, less any which do not
            appear in the parameters list at the head of the script; runs the
            script and returns the result.
        """
        dels = []
        params = kwargs.copy()
        # least efficient looping ever.
        # kill off any kwargs that we don't expect in the signature
        for k in params:
            if k not in self.__signature:
                dels.append(k)
        for d in dels:
            del params[d]

        return self.__compiled_code(self, **params)

    def __call__(self, **kwargs):
        """ (Re)loads the script from the filesystem and runs it, returning the
            result. Any keyword arguments passed to this function are passed on
            to the script.
        """
        self.reloadFile()
        return self._runFunction(**kwargs)
