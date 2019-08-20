from iocbuilder import Device, AutoSubstitution, Architecture, Xml
from iocbuilder.arginfo import *

from iocbuilder.modules.asyn import AsynPort
from iocbuilder.modules.ADCore import ADCore, includesTemplates, makeTemplateInstance, NDPluginBaseTemplate, NDFileTemplate

class FFmpegServer(Device):
    '''Library dependencies for ffmpeg'''
    Dependencies = (ADCore,)
    # Device attributes
    LibFileList = ['swresample', 'swscale', 'avutil', 'avcodec', 'avformat', 'avdevice', 'ffmpegServer']
    DbdFileList = ['ffmpegServer']  
    AutoInstantiate = True    

@includesTemplates(NDPluginBaseTemplate)
class _ffmpegStream(AutoSubstitution):
    TemplateFile = 'ffmpegStream.template'

class ffmpegStream(AsynPort):
    '''This plugin provides an http server that produces an mjpeg stream'''
    Dependencies = (FFmpegServer,)
    # This tells xmlbuilder to use PORT instead of name as the row ID
    UniqueName = "PORT"
    _SpecificTemplate = _ffmpegStream

    def __init__(self, PORT, NDARRAY_PORT, QUEUE = 2, HTTP_PORT = 8080, BLOCK = 0, NDARRAY_ADDR = 0, MEMORY = 0, ENABLED = 1, **args):
        # Init the superclass (AsynPort)
        self.__super.__init__(PORT)
        # Update the attributes of self from the commandline args
        self.__dict__.update(locals())
        # Make an instance of our template
        makeTemplateInstance(self._SpecificTemplate, locals(), args)

    # __init__ arguments
    ArgInfo = _SpecificTemplate.ArgInfo + makeArgInfo(__init__,
        ENABLED = Simple('Plugin Enabled at startup?', int),
        PORT = Simple('Port name for the NDStdArrays plugin', str),
        QUEUE = Simple('Input array queue size', int),
        HTTP_PORT = Simple('HTTP Port number', int),
        BLOCK = Simple('Blocking callbacks?', int),
        NDARRAY_PORT = Ident('Input array port', AsynPort),
        NDARRAY_ADDR = Simple('Input array port address', int),
        MEMORY = Simple('Max memory to allocate, should be maxw*maxh*nbuffer for driver and all attached plugins', int),
    )

    def InitialiseOnce(self):
        print "ffmpegServerConfigure(%(HTTP_PORT)d)" % self.__dict__

    def Initialise(self):
        print '# ffmpegStreamConfigure(portName, queueSize, blockingCallbacks, '\
            'NDArrayPort, NDArrayAddr, maxMemory)'
        print 'ffmpegStreamConfigure(' \
            '"%(PORT)s", %(QUEUE)d, %(BLOCK)d, "%(NDARRAY_PORT)s", ' \
            '"%(NDARRAY_ADDR)s", %(MEMORY)d)' % self.__dict__


@includesTemplates(NDPluginBaseTemplate, NDFileTemplate)
class _ffmpegFile(AutoSubstitution):
    '''Template containing the records for an NDColorConvert'''
    TemplateFile = 'ffmpegFile.template'

class ffmpegFile(AsynPort):
    '''This plugin can compress NDArrays to video and write them to file'''
    # This tells xmlbuilder to use PORT instead of name as the row ID
    UniqueName = "PORT"
    Dependencies = (FFmpegServer,)
    _SpecificTemplate = _ffmpegFile

    def __init__(self, PORT, NDARRAY_PORT, QUEUE = 2, BLOCK = 0, NDARRAY_ADDR = 0, BUFFERS = 50, MEMORY = 0, **args):
        # Init the superclass (AsynPort)
        self.__super.__init__(PORT)
        # Update the attributes of self from the commandline args
        self.__dict__.update(locals())
        # Make an instance of our template
        makeTemplateInstance(self._SpecificTemplate, locals(), args)

    ArgInfo = _SpecificTemplate.ArgInfo + makeArgInfo(__init__,
        PORT = Simple('Port name for the ffmpegFile plugin', str),
        QUEUE = Simple('Input array queue size', int),
        BLOCK = Simple('Blocking callbacks?', int),
        NDARRAY_PORT = Ident('Input array port', AsynPort),
        NDARRAY_ADDR = Simple('Input array port address', int),
        BUFFERS = Simple('Max buffers to allocate', int),
        MEMORY = Simple('Max memory to allocate, should be maxw*maxh*nbuffer for driver and all attached plugins', int))

    def Initialise(self):
        print '# ffmpegFileConfigure(portName,  queueSize, blockingCallbacks, NDArrayPort, NDArrayAddr, maxBuffers, maxMemory)' % self.__dict__
        print 'ffmpegFileConfigure  ("%(PORT)s", %(QUEUE)d, %(BLOCK)d, "%(NDARRAY_PORT)s", %(NDARRAY_ADDR)s, %(BUFFERS)d, %(MEMORY)d)' % self.__dict__


