from scipy.io import wavfile
import numpy as np
import librosa


def load_and_preprocess_audio(audio_filename):
    # TODO : Preprocess Audio
    msg_width = 64
    sample_rate = 16000
    duration_in_seconds = 1.0  
    no_of_fft = 512
    no_of_mels = 64

    sample_r, waveform = wavfile.read(audio_filename)
    length_of_hop = int(1 + duration_in_seconds * sample_rate // (msg_width - 1))
    desired_wave_length = int(length_of_hop * (msg_width - 1))

    if desired_wave_length > len(waveform):
        waveform = np.pad(waveform, (0, desired_wave_length - len(waveform)), 'median')

    elif len(waveform) > desired_wave_length:
        waveform = waveform[:desired_wave_length]

    msg = librosa.feature.melspectrogram(
        y=waveform,
        sr=sample_rate,
        hop_length=length_of_hop,
        n_fft=no_of_fft,
        n_mels=no_of_mels)
    # msg = librosa.core.logamplitude(msg**2, ref_power=1.)
    assert msg_width == msg.shape[1]
    return msg
