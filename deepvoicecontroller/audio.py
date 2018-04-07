from scipy.io import wavfile
import numpy as np
import librosa
import time
# import audiolab, scipy
import os


no_of_mels = 64
msg_width = 64

def give_merged_noise(my_wav,desired_wave_length):
    # TODO :merge noise return array of wave
    result=[my_wav]
    noise_dir=os.path.join(getDatasetDir(),"_background_noise_")
    # with_noise_data=os.path.join(getDatasetDir(),"_background_noise_")
    for file_ in listdir(noise_dir):
        sample_r, waveform = wavfile.read(os.path.join(noise_dir,file_))

        if desired_wave_length > len(waveform):
            waveform = np.pad(waveform, (0, desired_wave_length - len(waveform)), 'median')

        elif len(waveform) > desired_wave_length:
            waveform = waveform[:desired_wave_length]
        result.append( 0.6 * my_wav + 0.4 * waveform)    
            
        # audiolab.wavwrite(c, , fs, enc)
    return result

def load_and_preprocess_audio(audio_filename, add_noise = False):
    sample_rate = 16000
    duration_in_seconds = 1.0  
    no_of_fft = 512

    sample_r, waveform = wavfile.read(audio_filename)
    length_of_hop = int(1 + duration_in_seconds * sample_rate // (msg_width - 1))
    desired_wave_length = int(length_of_hop * (msg_width - 1))

    if desired_wave_length > len(waveform):
        waveform = np.pad(waveform, (0, desired_wave_length - len(waveform)), 'median')

    elif len(waveform) > desired_wave_length:
        waveform = waveform[:desired_wave_length]
    waveforms = [np.array(waveform, dtype=float)]
    if add_noise:
        waveforms.extends(give_merged_noise(waveforms[0], desired_wave_length))
    # print(waveform)
    msgs = []
    for waveform in waveforms:
        msg = librosa.feature.melspectrogram(
            y=waveform,
            sr=sample_rate,
            hop_length=length_of_hop,
            n_fft=no_of_fft,
            n_mels=no_of_mels)
        # msg = librosa.core.logamplitude(msg**2, ref_power=1.)
        # if exit:
        # 64 x 64
        # print(np.shape(msg))
            # exit()
        assert msg_width == msg.shape[1]
        msgs.append(msg)
    return msgs

# def capture_audio(callback):
#     import pyaudio
#     import wave as wv
#     from array import array

#     FORMAT=pyaudio.paInt16
#     RATE=16000
#     CHUNK=1024
#     COUNTCHUNK= (RATE+CHUNK-1)/CHUNK
#     RECORD_SECONDS=1
#     FILE_NAME="/tmp/mic_rec.wav"

#     audio=pyaudio.PyAudio()

#     stream=audio.open(format=FORMAT,
#                       rate=RATE,
#                       channels=1,
#                       input=True,
#                       frames_per_buffer=CHUNK)

#     #starting recording
#     wave=[]
#     callback_free = [True]
#     print("started")
#     last = time.time()
#     lastloudsoundtime = time.time()-100000
    
#     while True:
#         data=stream.read(CHUNK)
#         data_chunk=array('h',data)
#         vol=max(data_chunk)
#         wave.append(data)
#         if len(wave) > COUNTCHUNK:
#             wave.pop(0)
#         if(vol>=1500):
#             lastloudsoundtime = time.time()
#         if(time.time()-last>0.05 and time.time()-lastloudsoundtime<0.8):
#             last = time.time()
#             if len(wave) == COUNTCHUNK:
#                 #writing to file
#                 wavfile=wv.open(FILE_NAME,'wb')
#                 wavfile.setnchannels(1)
#                 wavfile.setsampwidth(audio.get_sample_size(FORMAT))
#                 wavfile.setframerate(RATE)
#                 wavfile.writeframes(b''.join(wave))
#                 wavfile.close()
#                 if callback_free[0]:
#                     callback_free[0]=False
#                     callback(callback_free,FILE_NAME)
#                     # print("Something is said")
#         else:
#             pass
#             # callback(None,None)
#             # print("Nothing is said")
#         # print("\n")

def capture_audio(callback,final_callback ):
    import pyaudio
    import wave as wv
    from array import array

    FORMAT=pyaudio.paInt16
    RATE=16000
    CHUNK=1024
    COUNTCHUNK= (RATE+CHUNK-1)/CHUNK
    RECORD_SECONDS=1
    FILE_NAME="/tmp/mic_rec.wav"

    audio=pyaudio.PyAudio()

    stream=audio.open(format=FORMAT,
                      rate=RATE,
                      channels=1,
                      input=True,
                      frames_per_buffer=CHUNK)

    #starting recording
    wave=[]
    callback_free = [True]
    print("started")
    last = time.time()
    lastloudsoundtime = time.time()-100000
    
    while True:
        data=stream.read(CHUNK)
        data_chunk=array('h',data)
        vol=max(data_chunk)
        # print("Volume {}".format(vol))
        wave.append(data)
        if len(wave) > COUNTCHUNK:
            wave.pop(0)
        if(vol>=2500):
            lastloudsoundtime = time.time()
        if(time.time()-last>0.05 and time.time()-lastloudsoundtime<0.8):
            last = time.time()
            if len(wave) == COUNTCHUNK:
                #writing to file
                wavfile=wv.open(FILE_NAME,'wb')
                wavfile.setnchannels(1)
                wavfile.setsampwidth(audio.get_sample_size(FORMAT))
                wavfile.setframerate(RATE)
                wavfile.writeframes(b''.join(wave))
                wavfile.close()
                if callback_free[0]:
                    callback_free[0]=False
                    callback(callback_free,FILE_NAME,final_callback)
                    # print("Something is said")
        else:
            pass
            # callback(None,None)
            # print("Nothing is said")
        # print("\n")
 
 
