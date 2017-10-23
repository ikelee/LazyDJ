'''
	Parse the folders in which data should be stored 
	
	Model looks like: 
		samples
		-> kick
		-> snare
		-> bass 
		-> synth
		-> vocal_lead
		-> vocal_harmony
		-> misc 
		instrumentals 
'''

import os
from madmom.features import DBNDownBeatTrackingProcessor as mmDBProcessor, RNNDownBeatProcessor

def analyze(top):
	#ListOfFolders should be ['instrumentals', 'samples']

	listUnderTop = filter(lambda link: str(link)[0] != '.', os.listdir(top))

	if listUnderTop != ["instrumentals", "samples"]:
		raise Exception("Error: incorrect folders under top level")

	listUnderSamples = filter(lambda link: str(link)[0] != '.', os.listdir(top + "samples"))
	listUnderInstrumentals = filter(lambda link: str(link)[0] != '.', os.listdir(top + "instrumentals"))


	if listUnderSamples != ['bass', 'kick', 'misc', 'snare', 'synth', 'vocal_harmony', 'vocal_lead']: 
		raise Exception("Error: incorrect folders under samples level")

	sampleAnalysis = {}
	'''
	sampleAnalysis is a dictionary of all the stems existing in our data, under key "stemType", will be list of dictionaries of each stem with its data

	samples = {
	"kick":
		{"filename1": {
			"Beat": beatInfo
			"Key" : key
			"Tempo": tempo
			"Chord progression": chord progression
			}
		"filename2": {
			"Beat": beatInfo
			"Key" : key
			"Tempo": tempo
			"Chord progression": chord progression
			}
	"bass": 
		{"filename1": {
			"Beat": beatInfo
			"Key" : key
			"Tempo": tempo
			"Chord progression": chord progression
			}
		"filename2": {
			"Beat": beatInfo
			"Key" : key
			"Tempo": tempo
			"Chord progression": chord progression
			}
	etc
	}

	'''

	for folder in listUnderSamples: 
		sampleAnalysis[folder] = {}
		stemsUnderFolder = filter(lambda link: str(link)[0] != '.', os.listdir(top + "samples/" + str(folder)))
		for stem in stemsUnderFolder: 
			sampleAnalysis[folder][stem] = {}

			proc = mmDBProcessor(beats_per_bar=4, fps = 100)
			beatInfo = proc(RNNDownBeatProcessor()(top + "samples/" + str(folder) + "/" + str(stem)))

			sampleAnalysis[folder][stem]["Beat"] = beatInfo

	print sampleAnalysis
