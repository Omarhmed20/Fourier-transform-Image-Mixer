import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from PIL import ImageTk, Image
from displaytemplate import DisplayTemplate
import numpy as np
import cv2  
# import logging
# from datetime import datetime

class GUI:
    def __init__(self):

        # logging.basicConfig(
        #     filename='logs.txt',
        #     level=logging.INFO,
        #     format='%(asctime)s.%(msecs)03dZ | %(levelname)s | %(message)s',
        #     datefmt='%Y-%m-%dT%H:%M:%S'
        # )


        # Create the main window
        self.window = tk.Tk()
        self.window.title('Image Mixer')

        self.frame = tk.Frame(self.window)
        self.frame.pack()

        self.frame2 = tk.Frame(self.window)
        self.frame2.pack(side=tk.LEFT)

        # Create a button to browse for image files
        self.browse_button = tk.Button(self.frame, text='Browse', command=self.browse_files)
        self.browse_button.pack(side=tk.LEFT)






















































































        

        # Create a button to toggle the mixing panel
        self.mixing_button = tk.Button(self.frame, text='Toggle Mixing Panel', command=self.toggle_mixing_panel)
        self.mixing_button.pack(side=tk.LEFT) 

        # Initialize instance variables
        self.displays = []
        self.mixing_frame = None
        self.output_displays = []
        
    def browse_files(self):
        # Open a file dialog to browse for multiple image files
        file_paths = filedialog.askopenfilenames(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])

        if file_paths:
            # Check if the selected images have the same dimensions
            sizes = [Image.open(file_path).size for file_path in file_paths]
            if len(set(sizes)) > 1:
                # Display an error message if the images do not have the same dimensions
                messagebox.showerror('Error', 'The selected images do not have the same dimensions.')
                # logging.critical('files uploaded not of the same size')
            else:
                # Create two instances of the DisplayTemplate class
                for i in range(2):
                    display = DisplayTemplate(self.frame2)

                    # Set the file paths of the two images
                    display.set_file_paths(file_paths[0], file_paths[1])

                    # Add the display to the list of displays
                    self.displays.append(display)

    def toggle_mixing_panel(self):
        if not self.displays:
            # Display an error message if no images have been uploaded
            messagebox.showerror('Error', 'Please upload two images before using the mixing panel.')
            # logging.warning('mixing panel toggled when there is no images to work with')
        else:
            if self.mixing_frame:
                # Hide the mixing frame if it is already visible
                self.mixing_frame.pack_forget()
                self.mixing_frame.destroy()
                self.mixing_frame = None

                # Hide the output display areas
                self.output_display1.pack_forget()
                self.output_display1.destroy()
                self.output_display2.pack_forget()
                self.output_display2.destroy()
            else:
                # Create a frame to hold the mixing widgets
                self.mixing_frame = tk.Frame(self.window)
                self.mixing_frame.pack()

                # Create drop-down menus to select the plots to mix
                self.plot1_var = tk.StringVar(self.mixing_frame)
                self.plot1_var.set('Image 1')
                self.plot1_menu = tk.OptionMenu(self.mixing_frame, self.plot1_var, 'Image 1', 'Image 2', command=lambda _:self.mix_plots)
                self.plot1_menu.grid(row=0, column=0)

                self.plot2_var = tk.StringVar(self.mixing_frame)
                self.plot2_var.set('Magnitude')
                self.plot2_menu = tk.OptionMenu(self.mixing_frame, self.plot2_var, 'Magnitude','uniform magnitude', 'Phase','uniform phase', 'Real', 'Imaginary', command=lambda _:self.mix_plots)
                self.plot2_menu.grid(row=0, column=1)

                self.plot3_var = tk.StringVar(self.mixing_frame)
                self.plot3_var.set('Image 1')
                self.plot3_menu = tk.OptionMenu(self.mixing_frame, self.plot3_var, 'Image 1', 'Image 2', command=lambda _:self.mix_plots)
                self.plot3_menu.grid(row=2, column=0, pady=[20,0])

                self.plot4_var = tk.StringVar(self.mixing_frame)
                self.plot4_var.set('Magnitude')
                self.plot4_menu = tk.OptionMenu(self.mixing_frame, self.plot4_var, 'Magnitude','uniform magnitude', 'Phase','uniform phase', 'Real', 'Imaginary', command=lambda _:self.mix_plots)
                self.plot4_menu.grid(row=2, column=1, pady=[20,0])

                # Create sliders to specify the mixing factors
                self.factor1_var = tk.DoubleVar(self.mixing_frame)
                self.factor1_var.set(0.5)
                self.factor1_slider = tk.Scale(self.mixing_frame, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, variable=self.factor1_var, command=lambda _:self.mix_plots())
                self.factor1_slider.grid(row=1, column=0, columnspan=2)

                self.factor2_var = tk.DoubleVar(self.mixing_frame)
                self.factor2_var.set(0.5)
                self.factor2_slider = tk.Scale(self.mixing_frame, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, variable=self.factor2_var, command=lambda _:self.mix_plots())
                self.factor2_slider.grid(row=3, column=0, columnspan=2)

                # Create a drop-down menu to select the output display
                self.output_var = tk.StringVar(self.mixing_frame)
                self.output_var.set('Output Display 1')
                self.output_menu = tk.OptionMenu(self.mixing_frame, self.output_var, 'Output Display 1', 'Output Display 2', command=lambda _:self.mix_plots())
                self.output_menu.grid(row=4, column=0, columnspan=2, pady=[20,0])

                # Create two display areas for the output
                self.output_display1 = tk.Label(self.window)
                self.output_display1.pack(side=tk.LEFT,pady=[67,0])

                self.output_display2 = tk.Label(self.window)
                self.output_display2.pack(side=tk.LEFT,pady=[67,0])

                # Create a transparent image with the same dimensions as the images in the displays
                width, height = Image.open(self.displays[0].file_path1).size
                img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                img.thumbnail((400, 400))
                img = ImageTk.PhotoImage(img)

                # Display the transparent image in both output displays
                self.output_display1.config(image=img)
                self.output_display1.image = img
                self.output_display2.config(image=img)
                self.output_display2.image = img

                # Display the output of the initial values of the sliders and plots in the first output display
                self.mix_plots()

    def mix_plots(self):
        # Get the selected plots and mixing factors from the mixing panel
        plot1 = (self.plot1_var.get(), self.plot2_var.get())
        factor1 = self.factor1_var.get()
        plot2 = (self.plot3_var.get(), self.plot4_var.get())
        factor2 = self.factor2_var.get()

        if(plot1[1]=="Real" and plot2[1]=="Imaginary" or plot1[1]=="Imaginary" and plot2[1]=="Real"):
            plot1_tuple = (plot1, factor1)
            plot2_tuple = (plot2, factor2)

            parameter_tuple = (plot1_tuple, plot2_tuple)

            sorted_tuple = sorted(parameter_tuple, key=lambda x: x[0][1] != "Real")

            image_reconstructed = self.mixing_real_imaginary(self.get_plot_data(sorted_tuple[0][0]), sorted_tuple[0][1], self.get_plot_data(sorted_tuple[1][0]), sorted_tuple[1][1])
            img = Image.fromarray(image_reconstructed.astype(np.uint8))

            # logging.info('%s is being combined with %s', sorted_tuple[0][0], sorted_tuple[0][1])


        elif plot1[1] == "uniform magnitude" or plot2 [1] == "uniform magnitude": 
            plot1_tuple = (plot1, factor1)
            plot2_tuple = (plot2, factor2)

            parameter_tuple = (plot1_tuple, plot2_tuple)

            sorted_tuple = sorted(parameter_tuple, key=lambda x: x[0][1] != "uniform magnitude")

            image_reconstructed = self.mixing_magnitude_phase(self.get_plot_data(sorted_tuple[0][0]), sorted_tuple[0][1], self.get_plot_data(sorted_tuple[1][0]), sorted_tuple[1][1]) * 1000
            img = Image.fromarray(image_reconstructed.astype(np.uint8))
            # logging.info('%s is being combined with %s', sorted_tuple[0][0], sorted_tuple[0][1])
            print(sorted_tuple)

        elif plot1[1] == "uniform phase" or plot2[1] == "uniform phase":
            plot1_tuple = (plot1, factor1)
            plot2_tuple = (plot2, factor2)

            parameter_tuple = (plot1_tuple, plot2_tuple)

            sorted_tuple = sorted(parameter_tuple, key=lambda x: x[0][1] != "Magnitude")

            image_reconstructed = self.mixing_magnitude_phase(self.get_plot_data(sorted_tuple[0][0]), sorted_tuple[0][1], self.get_plot_data(sorted_tuple[1][0]),1)
            img = Image.fromarray(image_reconstructed.astype(np.uint8))


        else:
            plot1_tuple = (plot1, factor1)
            plot2_tuple = (plot2, factor2)

            parameter_tuple = (plot1_tuple, plot2_tuple)

            sorted_tuple = sorted(parameter_tuple, key=lambda x: x[0][1] != "Magnitude")

            image_reconstructed = self.mixing_magnitude_phase(self.get_plot_data(sorted_tuple[0][0]), sorted_tuple[0][1], self.get_plot_data(sorted_tuple[1][0]), sorted_tuple[1][1])
            img = Image.fromarray(image_reconstructed.astype(np.uint8))
            # logging.info('%s is being combined with %s', sorted_tuple[0][0], sorted_tuple[0][1])

        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)

        # Get the selected output display from the drop-down menu
        output_display = self.output_var.get()

        # Update the selected output display with the mixed image
        if output_display == 'Output Display 1':
            # Clear any previously displayed images in both output displays
            self.output_display1.config(image='')
            self.output_display2.config(image='')

            # Display the mixed image in the selected output display
            self.output_display1.config(image=img, compound=tk.BOTTOM)
            self.output_display1.image = img

            # Set the content of the non-selected output display to a transparent image with the same dimensions as the image displayed in the selected output display
            width, height = img.width(), img.height()
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            img = ImageTk.PhotoImage(img)
            self.output_display2.config(image=img, compound=tk.BOTTOM)
            self.output_display2.image = img

            # logging.info('first output display selected')
        elif output_display == 'Output Display 2':
            # Clear any previously displayed images in both output displays
            self.output_display1.config(image='')
            self.output_display2.config(image='')

            # Display the mixed image in the selected output display
            self.output_display2.config(image=img, compound=tk.BOTTOM)
            self.output_display2.image = img

            # Set the content of the non-selected output display to a transparent image with the same dimensions as the image displayed in the selected output display
            width, height = img.width(), img.height()
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            img = ImageTk.PhotoImage(img)
            self.output_display1.config(image=img, compound=tk.BOTTOM)
            self.output_display1.image = img

            # logging.info('second output display selected')

    def get_output_display_frame(self, output_display):
        # Get the frame corresponding to the selected output display
        if output_display == 'Output Display 1':
            return self.output_display1
            #return self.display1_frame
        elif output_display == 'Output Display 2':
            return self.output_display2
            #return self.display2_frame
        else:
            return None
        
    def get_plot_data(self, plot):
        # Get the data for the specified plot
        image_index = int(plot[0][-1]) - 1
        plot_type = plot[1]
        display = self.displays[image_index]
        uploaded_image = display.uploaded_image1 if plot[0] == 'Image 1' else display.uploaded_image2
        if plot_type == 'Magnitude':
            return uploaded_image.calculate_magnitude_plot()
        elif plot_type == 'Phase':
            return uploaded_image.calculate_phase_plot()
        elif plot_type == 'Real':
            return uploaded_image.calculate_real_plot()
        elif plot_type == 'Imaginary':
            return uploaded_image.calculate_imaginary_plot()
        elif plot_type == 'uniform phase':
            return uploaded_image.calculate_phase_plot() * 0.2
        elif plot_type == 'uniform magnitude':
            return 1

    def run(self):
        # Run the main loop of the GUI
        self.window.mainloop()




    def mixing_magnitude_phase(self, plotData1, factor1, plotData2, factor2):

        mixed_image = plotData1 * factor1 *  np.exp(1j * plotData2 * factor2)
        mixed_image = np.fft.ifft2(mixed_image).real

        return mixed_image
    
    def mixing_real_imaginary(self, plotData1, factor1, plotData2, factor2):

        mixed_image = (plotData1 * factor1) +(1j * plotData2 * factor2)
        mixed_image = np.fft.ifft2(mixed_image).real

        return mixed_image
