import tkinter as tk
from PIL import ImageTk, Image
from uploadedImage import UploadedImage

class DisplayTemplate:
    def __init__(self, parent):
        # Create a frame to hold the widgets
        self.frame = tk.Frame(parent)
        self.frame.pack()

         # Create a frame to hold the widgets
        self.frame2 = tk.Frame(self.frame)
        self.frame2.pack()

        self.frame3 = tk.Frame(self.frame)
        self.frame3.pack()




        # Create a drop-down menu to select the image
        self.image_var = tk.StringVar(self.frame2)
        self.image_var.set('Image 1')
        self.image_menu = tk.OptionMenu(self.frame2, self.image_var, 'Image 1', 'Image 2', command=self.update_plot)
        self.image_menu.pack(side=tk.LEFT,padx=[0,20])

        # Create a drop-down menu to select the plot type
        self.plot_var = tk.StringVar(self.frame2)
        self.plot_var.set('Magnitude')
        self.plot_menu = tk.OptionMenu(self.frame2, self.plot_var, 'Magnitude', 'Phase', 'Real', 'Imaginary', command=self.update_plot)
        self.plot_menu.pack(side=tk.LEFT,padx=[5,0])

        # Create a label to display the image
        self.image_label = tk.Label(self.frame3)
        self.image_label.pack(side=tk.LEFT)

        # Create a label to display the plot
        self.plot_label = tk.Label(self.frame3)
        self.plot_label.pack(side=tk.LEFT)

    def set_file_paths(self, file_path1, file_path2):
        # Store the file paths of the two images
        self.file_path1 = file_path1
        self.file_path2 = file_path2

        # Create instances of the UploadedImage class for each file path
        self.uploaded_image1 = UploadedImage(file_path1)
        self.uploaded_image2 = UploadedImage(file_path2)

        # Update the image and plot labels
        self.update_plot()

    def update_plot(self, *args):
        # Clear the image and plot labels
        self.image_label.config(image='')
        self.plot_label.config(image='')

        # Get the selected image from the drop-down menu
        image = self.image_var.get()

        # Update the image label with the selected image
        if image == 'Image 1':
            img = Image.open(self.file_path1)
            uploaded_image = UploadedImage(self.file_path1)
        elif image == 'Image 2':
            img = Image.open(self.file_path2)
            uploaded_image = UploadedImage(self.file_path2)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

        # Update the plot label with the selected plot
        if uploaded_image:
            # Get the selected plot type from the drop-down menu
            plot_type = self.plot_var.get()

            # Calculate the selected plot
            if plot_type == 'Magnitude':
                plot_data = uploaded_image.display_magnitude_plot()
            elif plot_type == 'Phase':
                plot_data = uploaded_image.display_phase_plot()
            elif plot_type == 'Real':
                plot_data = uploaded_image.display_real_plot()
            elif plot_type == 'Imaginary':
                plot_data = uploaded_image.display_imaginary_plot()

            # Convert the plot data to an image and display it in the label
            img = Image.fromarray(plot_data)
            img.thumbnail((400, 400))
            img = ImageTk.PhotoImage(img)
            self.plot_label.config(image=img)
            self.plot_label.image = img
