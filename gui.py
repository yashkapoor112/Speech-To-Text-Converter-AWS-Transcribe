from tkinter import *
import pyaudio
import time
import wave
import boto3
import sys

 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5


def clicked():
 
    lbl.configure(text="Processing ")

def process_complete():
 
    lbl.configure(text="Process Completed")

def both():
	clicked()
	sound_rec()

def sound_rec():
	

	audio = pyaudio.PyAudio()
	 
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
	                rate=RATE, input=True,
	                frames_per_buffer=CHUNK)
	print ("recording...")
	frames = []
	 
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print ("finished recording")
	clicked()
	 
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	 
	waveFile = wave.open("file.wav", 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

	

	s3 = boto3.client('s3')

	filename = 'NAME OF THE FILE WITH THE EXTENSION'
	bucket_name = 'NAME OF THE BUCKET'

	# Uploads the given file using a managed uploader, which will split up large
	# files automatically and upload parts in parallel.
	s3.upload_file(filename, bucket_name, filename)
	time.sleep(10)
	transcribe = boto3.client('transcribe')
	job_name = "JOBNAME IN AWS TRANSCRIBE SHOULD BE UNIQUE EVERYTIME"
	job_uri = "LINK OF THE FILE IN S3"
	transcribe.start_transcription_job(
	    TranscriptionJobName=job_name,
	    Media={'MediaFileUri': job_uri},
	    MediaFormat='wav',
	    LanguageCode='en-US'
	)
	while True:
	    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
	    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
	        break

		
	time.sleep(10)
	lbl.configure(text="Process Completed")
	print(status)
	return "TESTING"

	process_complete()

root = Tk()




root.title("Audio Converter")
 
root.geometry('350x200')
 
lbl = Label(root, text="Click the Button to start recording")
 
lbl.grid(column=0, row=0)
 

 
btn = Button(root, text="Click Me", command=clicked)
button1 = Button(root,text="Start Recording",command =both)
 
button1.grid(column=1, row=0)
 
root.mainloop()



theLabel = Label(root,text = "Sound Recorder")
theLabel.pack()

topFrame =Frame(root)	
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)

button1 = Button(topFrame,text = "Start Recording",fg = "red")
button2 = Button(topFrame,text = "Start Recording",fg = "green")
button3 = Button(bottomFrame,text = "Start Recording",fg = "blue")
button4 = Button(bottomFrame,text = "Start Recording",fg = "cyan")

button1.pack(side = LEFT)
button2.pack(side = LEFT)
button3.pack(side = LEFT)
button4.pack(side = BOTTOM)

one = Label(root,text= "One",bg ="red" ,fg = "white")
one.pack()
two = Label(root,text= "two",bg ="red" ,fg = "white")
two.pack(fill = X)
three = Label(root,text= "three",bg ="red" ,fg = "white")
three.pack(fill = Y,side = LEFT)


label1 = Label(root,text = "Name")
label2 = Label(root,text = "Password")
entry1 = Entry(root)
entry2 = Entry(root)

label1.grid(row=0,sticky=E)
label2.grid(row=1,sticky=E)
entry1.grid(row=0,column=1)
entry2.grid(row=1,column=1)
c = Checkbutton(root,text = "Keep me logged in")
c.grid(columnspan=2)




root.mainloop()
