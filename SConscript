#HYDRAD Build SConscript
#Will Barnes
#15 December 2015

#Import needed modules
import glob

#Import environment from SConstruct
Import('env')

sources = glob.glob('source/*.cpp')
txml2_sources = ['tinyxml2/tinyxml2.cpp']

objs = env.Object(sources+txml2_sources)

Return('objs')