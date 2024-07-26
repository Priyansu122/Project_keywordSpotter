import wave
import numpy as np
import matplotlib.pyplot as plt

def read_pcm_from_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        n_channels = wav_file.getnchannels()
        sampwidth = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()

        print(f"Channels: {n_channels}, Sample Width: {sampwidth}, Frame Rate: {framerate}, Frames: {n_frames}")

        if sampwidth != 1:
            raise ValueError("This script only supports 8-bit PCM data.")

        pcm_data = wav_file.readframes(n_frames)
    return pcm_data

def serialize_pcm_data(pcm_data):
    serial_data = []
    for byte in pcm_data:
        for i in range(8):
            # Shift and mask to get each bit
            bit = (byte >> (7 - i)) & 1
            serial_data.append(bit)
    return serial_data

def save_serial_data(serial_data, output_file):
    with open(output_file, 'w') as file:
        for bit in serial_data:
            file.write(str(bit))

wav_file_path = 'speech_signal.wav'
output_file_path = "D:\Desktop\serial_data.txt"
#################################################################
# Read the PCM data from the .wav file
pcm_data = read_pcm_from_wav("D:\Desktop\helloliku_4K_8b.wav")
#################################################################
# Serialize the PCM data
serial_data = serialize_pcm_data(pcm_data)

# Save the serialized data to a file
save_serial_data(serial_data, output_file_path)

print(f"Serialized data saved to {output_file_path}")

# To know how many bits are there in the text file which contains binary values

# Read the contents of the file
with open(output_file_path, 'r') as file:
    data = file.read()

# Count the number of binary values
num_binary_values = len(data)

print(f'The number of binary values in the file is: {num_binary_values}')

# Creat frames and store data with 50 % overlap time is = 10ms in our case

def create_frames(serial_data, frame_size=40, overlap=20):
    frames = []
    num_samples = len(serial_data)
    step_size = frame_size - overlap
    
    for start in range(0, num_samples - frame_size + 1, step_size):
        frame = serial_data[start:start + frame_size]
        frames.append(frame)
    
    return frames

'''
def save_frames_to_file(frames, output_file):
    with open(output_file, 'w') as file:
        for i, frame in enumerate(frames):
            frame_str = ' '.join(map(str, frame))
            file.write(f"Frame {i + 1}: {frame_str}\n")


frame_file_path = "D:\Desktop\frames.txt"

'''
# Create frames with the specified overlap
frames = create_frames(data, frame_size=40, overlap=20)
#print(frames)

#------ERROR PART---------------------------
# Save the frames to a file
#save_frames_to_file(frames, frame_file_path)

#print(f"Frames saved to {output_file_path}")
#----------------------------------------------

'''
Applying the Hamming window and print the results

'''

def apply_hamming_window_to_frame(frame):
    
    # Convert each character in the string to an integer and create a list
    frame_list = [int(char) for char in frame]

    # Generate the Hamming window based on the length of the frame
    hamming_window = np.hamming(len(frame_list))
    
    # Apply the Hamming window to the frame using element-wise multiplication
    frame_with_hamming = frame_list * hamming_window
    
    return frame_with_hamming.tolist()  # Convert back to a nested list

def apply_hamming_window_to_frames(frames):
    # Apply Hamming window to each frame in the list
    frames_with_hamming = [apply_hamming_window_to_frame(frame) for frame in frames]
    
    return frames_with_hamming


# Apply Hamming window to each frame
frames_with_hamming = apply_hamming_window_to_frames(frames)

#print(frames_with_hamming)

'''
Apply 64 point fft 

'''

def zero_pad(frame_str, target_length=64):
    # Zero-pad the frame to the target length
    
    # Convert String to List
    frame = [int(char) for char in frame_str]
    
    padded_frame = np.pad(frame, (0, target_length - len(frame)), 'constant')
    return padded_frame

def perform_fft(frame_str):
    # Perform a 64-point FFT on the frame
    
    # Convert string to list
    frame = [int(char) for char in frame_str]
    
    fft_result = np.fft.fft(frame, n=64)
    return fft_result

def process_frames(frames):
    fft_results = []
    for frame in frames:
        # Zero-pad the frame to 64 points
        padded_frame = zero_pad(frame, target_length=64)
        # Perform the 64-point FFT
        fft_result = perform_fft(padded_frame)
        fft_results.append(fft_result)
    return fft_results

# Filterbank code
#-------------------------------------------------------------------------------------------
def hz_to_mel(hz):
    return 2595 * np.log10(1 + hz / 700)

def mel_to_hz(mel):
    return 700 * (10**(mel / 2595) - 1)

def mel_filterbank(num_filters, NFFT, samplerate):
    # Define frequency range
    low_freq = 0
    high_freq = samplerate / 2
    
    # Convert to Mel scale
    low_mel = hz_to_mel(low_freq)
    high_mel = hz_to_mel(high_freq)
    
    # Equally spaced Mel points
    mel_points = np.linspace(low_mel, high_mel, num_filters + 2)
    
    # Convert back to Hz
    hz_points = mel_to_hz(mel_points)
    
    # Convert Hz to FFT bin numbers
    bin_points = np.floor((NFFT + 1) * hz_points / samplerate).astype(int)
    
    # Create filterbank
    filterbank = np.zeros((num_filters, NFFT // 2 + 1))
    for i in range(1, num_filters + 1):
        left = bin_points[i - 1]
        center = bin_points[i]
        right = bin_points[i + 1]
        
        # Create triangular filters
        for j in range(left, center):
            filterbank[i - 1, j] = (j - bin_points[i - 1]) / (bin_points[i] - bin_points[i - 1])
        for j in range(center, right):
            filterbank[i - 1, j] = (bin_points[i + 1] - j) / (bin_points[i + 1] - bin_points[i])
    
    return filterbank, hz_points
#--------------------------------------------------------------------------------------------------
# Power Calculation
def power_spectrum(fft_result):
    return np.abs(fft_result[:NFFT // 2 + 1]) ** 2

def filter_bank_energies(power_spectrum, filter_bank):
    return np.dot(filter_bank, power_spectrum)
#---------------------------------------------------------------------------------------------------
# Cepstral coefficients
# Function to compute cepstral coefficients
def compute_cepstral_coefficients(log_filter_bank_energies, num_coefficients):
    K = len(log_filter_bank_energies)
    cepstral_coefficients = np.zeros(num_coefficients)
    for n in range(num_coefficients):
        sum_val = 0
        for k in range(1, K + 1):
            sum_val += log_filter_bank_energies[k - 1] * np.cos(n * (k - 0.5) * np.pi / K)
        cepstral_coefficients[n] = sum_val
    return cepstral_coefficients
#-------------------------------------------------------------------------------------------------


# Process the frames to get the FFT results
fft_results = process_frames(frames)

# Print the FFT result of the first frame
print("FFT of the first frame:")
print(fft_results[0])
#--------------------------------------------------------
# Parameters
num_filters = 20
NFFT = 64 #no of points in fft
samplerate = 4000

# Generate filterbank
filterbank, hz_points = mel_filterbank(num_filters, NFFT, samplerate)

print("filter bank",filterbank)
# Plot the filterbank
plt.figure(figsize=(10, 6))
for i in range(num_filters):
    plt.plot(np.linspace(0, samplerate / 2, NFFT // 2 + 1), filterbank[i])
plt.title('Mel Filterbank')
plt.xlabel('Frequency (Hz)')
#---------------------------------------------------------
# Filter bank energies
all_filter_bank_energies = []  

for fft_result in fft_results:
     
    # Compute power spectrum
    power_spec = power_spectrum(fft_result)
    
    # Compute filter bank energies
    filter_bank_energy = filter_bank_energies(power_spec, filterbank)
    all_filter_bank_energies.append(filter_bank_energy)

# Convert to numpy array for easier manipulation
all_filter_bank_energies = np.array(all_filter_bank_energies)

# Plot the filter bank energies for all frames
plt.imshow(all_filter_bank_energies.T, aspect='auto', origin='lower', interpolation='nearest')
plt.title("Mel Filter Bank Energies for All Frames")
plt.xlabel("Frame Index")
plt.ylabel("Filter Index")
plt.colorbar(label="Energy")
plt.show()
#-----------------------------------------------------
num_coefficients = 13  # Number of cepstral coefficients to compute
log_filter_bank_energies = np.log(all_filter_bank_energies + 1e-10)  # Adding a small value to avoid log(0)

# Compute cepstral coefficients for all frames
all_cepstral_coefficients = []
for log_energy in log_filter_bank_energies:
    cepstral_coefficients = compute_cepstral_coefficients(log_energy, num_coefficients)
    all_cepstral_coefficients.append(cepstral_coefficients)

# Convert to numpy array for easier manipulation
all_cepstral_coefficients = np.array(all_cepstral_coefficients)
full_cepstral_coefficients = all_cepstral_coefficients.tolist() #to see all components
print(all_cepstral_coefficients)

print(all_cepstral_coefficients)
# Plot the cepstral coefficients for all frames
plt.imshow(all_cepstral_coefficients.T, aspect='auto', origin='lower', interpolation='nearest')
plt.title("Cepstral Coefficients for All Frames")
plt.xlabel("Frame Index")
plt.ylabel("Cepstral Coefficient Index")
plt.colorbar(label="Coefficient Value")
plt.show()
 