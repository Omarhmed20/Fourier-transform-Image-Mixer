import cv2
import numpy as np
from PIL import Image
from scipy.fft import fftfreq, rfftn, irfftn, fft2, ifft2, fftn, ifftn, fftshift


class UploadedImage:
    def __init__(self, file_path):
        self.file_path = file_path


    def calculate_magnitude_plot(self):
        # Load the image
        image = Image.open(self.file_path).convert('L')
    
        # Convert the image to a NumPy array
        image_array = np.array(image)

        # Perform Fast Fourier Transform (FFT)
        fft = np.fft.fft2(image_array)

        # Calculate magnitude
        magnitude = np.abs(fft)

        return magnitude
    
    def calculate_phase_plot(self):
        # Load the image
        image = Image.open(self.file_path).convert('L')

        # Convert the image to a NumPy array
        image_array = np.array(image)

        # Perform Fast Fourier Transform (FFT)
        fft = np.fft.fft2(image_array)

        # Calculate phase 
        phase = np.angle(fft)
        return phase
    
    def calculate_real_plot(self):
        # Load the image
        image = Image.open(self.file_path).convert('L')
        width, height = image.size

        # Perform Fast Fourier Transform (FFT)
        fft = np.fft.fft2(image)

        return np.real(fft)

    def calculate_imaginary_plot(self):
        # Load the image
        image = Image.open(self.file_path).convert('L')
        width, height = image.size

        # Convert the image to a NumPy array
        image_array = np.array(image)

        # Perform Fast Fourier Transform (FFT)
        fft = np.fft.fft2(image_array)

        return np.imag(fft)
    
    def display_magnitude_plot(self):
        # Load the image
        img = cv2.imread(self.file_path, 0)

        # Compute the discrete Fourier Transform of the image
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)

        # Shift the zero-frequency component to the center of the spectrum
        dft_shift = np.fft.fftshift(dft)

        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

        return magnitude_spectrum
    
    def display_phase_plot(self):
        # Load the image
        img = cv2.imread(self.file_path, 0)


        # Compute the discrete Fourier Transform of the image
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT | cv2.DFT_SCALE)

        # Shift the zero-frequency component to the center of the spectrum
        dft_shift = np.fft.fftshift(dft)

        # Calculate the magnitude of the complex numbers
        magnitude = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])

        # Add a small positive value to the magnitude array
        magnitude += 1e-5

        # Calculate the phase spectrum
        phase_spectrum = np.arctan2(dft_shift[:,:,1], dft_shift[:,:,0])        

        # Normalize the phase spectrum values to the range [0, 255]
        phase_spectrum = cv2.normalize(phase_spectrum, None, 0, 255, cv2.NORM_MINMAX)

        # Convert the phase spectrum values to 8-bit unsigned integers
        phase_spectrum = phase_spectrum.astype(np.uint8)

        return phase_spectrum
    
    def display_real_plot(self):
        # Load the image
        img = cv2.imread(self.file_path, 0)

        # Compute the discrete Fourier Transform of the image
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)

        # Shift the zero-frequency component to the center of the spectrum
        dft_shift = np.fft.fftshift(dft)

        # Extract the real part of the DFT
        real_dft = dft_shift[:,:,0]

        # Shift the values of the real part to the positive range
        real_dft += np.abs(np.min(real_dft))

        # Normalize the values of the real part to the range [0, 255]
        real_dft = cv2.normalize(real_dft, None, 0, 255, cv2.NORM_MINMAX)

        # Convert the values of the real part to 8-bit unsigned integers
        real_dft = real_dft.astype(np.uint8)

        return real_dft

    def display_imaginary_plot(self):
        # Load the image
        img = cv2.imread(self.file_path, 0)

        # Compute the discrete Fourier Transform of the image
        dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)

        # Shift the zero-frequency component to the center of the spectrum
        dft_shift = np.fft.fftshift(dft)

        # Extract the imaginary part of the DFT
        imaginary_dft = dft_shift[:,:,1]

        # Shift the values of the imaginary part to the positive range
        imaginary_dft += np.abs(np.min(imaginary_dft))

        # Normalize the values of the imaginary part to the range [0, 255]
        imaginary_dft = cv2.normalize(imaginary_dft, None, 0, 255, cv2.NORM_MINMAX)

        # Convert the values of the imaginary part to 8-bit unsigned integers
        imaginary_dft = imaginary_dft.astype(np.uint8)

        return imaginary_dft

    def calculate_uniform_phase(self):

        img = self.display_phase_plot()
        img = img*0
        return img
    


    def phase_for_unipmag(self):
        # Load the image
        image = Image.open(self.file_path).convert('L')
    
        # Convert the image to a NumPy array
        image_array = np.array(image)
        self.fftdata = rfftn(image_array)
        phase = np.exp(np.multiply(1j, np.angle(self.fftdata)))

        return phase

    def mag_for_unimag(self):
        # Load the image
        image = Image.open(self.file_path).convert('L')
    
        # Convert the image to a NumPy array
        image_array = np.array(image)
        self.fftdata = rfftn(image_array)
        mag = np.abs(self.fftdata)

        return mag
