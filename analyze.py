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

import os
import threading
from madmom.features import DBNDownBeatTrackingProcessor as mmDBProcessor, RNNDownBeatProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.processors import SequentialProcessor
from madmom.audio.chroma import DeepChromaProcessor
from statistics import mode

def detectBeat(listUnderSamples, top, folder, stem, sampleAnalysis): 
	proc = mmDBProcessor(beats_per_bar=4, fps = 100)
	beatInfo = proc(RNNDownBeatProcessor()(top + "samples/" + str(folder) + "/" + str(stem)))

	sampleAnalysis[folder][stem]["Beat"] = beatInfo

def detectKey(listUnderSamples, top, folder, stem, sampleAnalysis):
	dcp = DeepChromaProcessor()
	decode = DeepChromaChordRecognitionProcessor()
	chordrec = SequentialProcessor([dcp, decode])

	keyInfo = chordrec(top + "samples/" + str(folder) + "/" + str(stem))

	#TODO: map into keyInfo list and find the key

	sampleAnalysis[folder][stem]["Key"] = keyInfo

def analyze(top):
	#ListOfFolders should be ['instrumentals', 'samples']

	listUnderTop = list(filter(lambda link: str(link)[0] != '.', os.listdir(top)))

	if listUnderTop != ["instrumentals", "samples"]:
		raise Exception("Error: incorrect folders under top level")

	listUnderSamples = list(filter(lambda link: str(link)[0] != '.', os.listdir(top + "samples")))
	listUnderInstrumentals = list(filter(lambda link: str(link)[0] != '.', os.listdir(top + "instrumentals")))

	#TODO: Implement listUnderInstrumentals section
 

	if listUnderSamples != ['bass', 'kick', 'misc', 'snare', 'synth', 'vocal_harmony', 'vocal_lead']: 
		raise Exception("Error: incorrect folders under samples level")

	sampleAnalysis = {}

	for folder in listUnderSamples: 
		sampleAnalysis[folder] = {}
		stemsUnderFolder = list(filter(lambda link: str(link)[0] != '.', os.listdir(top + "samples/" + str(folder))))
		for stem in stemsUnderFolder: 
			sampleAnalysis[folder][stem] = {}

			findKey = threading.Thread( target = detectKey, args = (listUnderSamples, top, folder, stem, sampleAnalysis) )
			findBeat = threading.Thread( target = detectBeat, args = (listUnderSamples, top, folder, stem, sampleAnalysis) )

			findKey.start()
			findBeat.start()

			findKey.join()
			findBeat.join()

	print(sampleAnalysis)
