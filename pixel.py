import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
import json

class PixelArtApp:
    def __init__(self, root, canvas_size=320, preview_scale=10):
        self.root = root
        self.canvas_size = canvas_size  # Fixed canvas size
        self.preview_scale = preview_scale
        self.selected_color = '#000000'
        self.grid_size = 16
        self.pixel_size = canvas_size // self.grid_size  # Calculate pixel size dynamically
        self.image_data = [[None] * self.grid_size for _ in range(self.grid_size)]  # Initialize with None for transparency

        # Apply the calm theme and update the window title
        self.apply_calm_theme()
        self.update_window_title()

        # Create menu, canvas, preview canvas, and palette frame
        self.create_menu()
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='#F0F0F0')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.preview_canvas = tk.Canvas(root, width=self.grid_size * preview_scale, height=self.grid_size * preview_scale, bg='#F0F0F0')
        self.preview_canvas.pack(side=tk.RIGHT, padx=10, pady=10)
        self.palette_frame = tk.Frame(root, bg='#E8E8E8')
        self.palette_frame.pack(pady=10)

        self.create_palette()
        self.create_grid()

    # Apply the calm theme to the app
    def apply_calm_theme(self):
        self.root.configure(bg='#E8E8E8')

    # Update the window title based on the grid size
    def update_window_title(self):
        if self.grid_size == 8:
            title = "Pixel Sprite Maker - 8-bit Grid"
        elif self.grid_size == 16:
            title = "Pixel Sprite Maker - 16-bit Grid"
        elif self.grid_size == 32:
            title = "Pixel Sprite Maker - 32-bit Grid"
        else:
            title = "Pixel Art Creator - Custom Grid"
        self.root.title(title)

    # Create the menu bar with file, settings, and help menus
    def create_menu(self):
        menu_bar = tk.Menu(self.root, bg='#E8E8E8', fg='#505050', activebackground='#D8D8D8', activeforeground='#303030')
        self.root.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0, bg='#E8E8E8', fg='#505050')
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_art)
        file_menu.add_command(label="Save As", command=self.save_as_art)
        file_menu.add_command(label="Save Project", command=self.save_project_as)
        file_menu.add_command(label="Load Project", command=self.load_project_as)
        file_menu.add_command(label="Clear", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Settings menu
        settings_menu = tk.Menu(menu_bar, tearoff=0, bg='#E8E8E8', fg='#505050')
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="8-bit Grid", command=lambda: self.set_grid_size(8))
        settings_menu.add_command(label="16-bit Grid", command=lambda: self.set_grid_size(16))
        settings_menu.add_command(label="32-bit Grid", command=lambda: self.set_grid_size(32))

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0, bg='#E8E8E8', fg='#505050')
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_help)

    # Display help information
    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.configure(bg='#E8E8E8')
        help_text = """Welcome to Pixel Sprite Maker!
        
Here's how to use the application:

- To select a color, click on one of the color buttons or choose a custom color.
- To draw on the canvas, click on the grid squares to fill them with the selected color.
- To change the grid size, go to the 'Settings' menu and select a grid size.
- To save your artwork, go to the 'File' menu and select 'Save' or 'Save As'.

FAQ:
- How do I change the grid size? Go to the 'Settings' menu and select the desired grid size.
- How do I use custom colors? Click on the 'Custom' button in the color palette and choose a color.
- How do I save my artwork? Go to the 'File' menu and select 'Save' or 'Save As'.

Enjoy, Washer.
"""
        tk.Label(help_window, text=help_text, bg='#E8E8E8', fg='#505050', justify=tk.LEFT, padx=10, pady=10).pack()

    # Create the color palette
    def create_palette(self):
        self.clear_palette()
        palettes = {
            8: ['#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'],
            16: ['#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
                 '#800000', '#808000', '#800080', '#008080', '#C0C0C0', '#808080', '#FF8080', '#80FF80'],
            32: ['#000000', '#FFFFFF', '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF',
                 '#800000', '#808000', '#800080', '#008080', '#C0C0C0', '#808080', '#FF8080', '#80FF80',
                 '#008000', '#000080', '#8080FF', '#800080', '#8080FF', '#800080', '#800000', '#00FF80',
                 '#FF8000', '#80FF00', '#FF0080', '#80FF80', '#FFFF80', '#80FFFF', '#FF80FF', '#FF8080']
        }

        row, col = 0, 0
        for color in palettes[self.grid_size]:
            if col >= 10:  # Stack vertically when reaching 10 colors per row
                col = 0
                row += 1
            tk.Button(self.palette_frame, bg=color, width=2, height=1, command=lambda col=color: self.select_color(col)).grid(row=row, column=col, padx=2, pady=2)
            col += 1

        tk.Button(self.palette_frame, text='Custom', command=self.choose_custom_color).grid(row=row, column=col, padx=2, pady=2)

    # Clear the color palette
    def clear_palette(self):
        for widget in self.palette_frame.winfo_children():
            widget.destroy()

    # Select a color from the palette
    def select_color(self, color):
        self.selected_color = color

    # Choose a custom color
    def choose_custom_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.selected_color = color_code

    # Create the pixel art grid
    def create_grid(self):
        self.canvas.delete("all")
        self.pixel_size = self.canvas_size // self.grid_size  # Recalculate pixel size based on grid size
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1, y1 = col * self.pixel_size, row * self.pixel_size
                x2, y2 = x1 + self.pixel_size, y1 + self.pixel_size  # Corrected line
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black', tags=f'pixel_{row}_{col}')
                self.canvas.tag_bind(f'pixel_{row}_{col}', '<Button-1>', self.color_pixel)

    # Color a specific pixel in the grid
    def color_pixel(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        self.canvas.itemconfig(item, fill=self.selected_color)

        row, col = event.y // self.pixel_size, event.x // self.pixel_size
        self.update_preview(row, col, self.selected_color)
        self.image_data[row][col] = self.selected_color

    # Update the preview canvas with the selected color
    def update_preview(self, row, col, color):
        x1, y1 = col * self.preview_scale, row * self.preview_scale
        x2, y2 = x1 + self.preview_scale, y1 + self.preview_scale
        self.preview_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

        # Save the pixel art as a PNG file
    def save_art(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.save_to_png(file_path)

    def save_as_art(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.save_to_png(file_path)

    def save_to_png(self, file_path):
        scale_factor = 20  # Adjust this factor to scale up the image size

        # Create an image with a transparent background
        image = Image.new('RGBA', (self.grid_size * scale_factor, self.grid_size * scale_factor), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw the image, ensuring white pixels are saved as white and the background remains transparent
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = self.image_data[row][col]
                if color:  # Draw pixels if color is not None
                    if color != '#FFFFFF':  # Draw non-white pixels normally
                        draw.rectangle([col * scale_factor, row * scale_factor, (col + 1) * scale_factor, (row + 1) * scale_factor], fill=color)
                    else:  # Explicitly handle white pixels
                        draw.rectangle([col * scale_factor, row * scale_factor, (col + 1) * scale_factor, (row + 1) * scale_factor], fill=(255, 255, 255, 255))

        # Save the image
        image.save(file_path)

    # Clear the canvas and reset the image data
    def clear_canvas(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.canvas.itemconfig(f'pixel_{row}_{col}', fill='white')
                self.update_preview(row, col, 'white')
        self.image_data = [[None] * self.grid_size for _ in range(self.grid_size)]

    # Set a new grid size and update the canvas accordingly
    def set_grid_size(self, new_size):
        self.grid_size = new_size
        self.pixel_size = self.canvas_size // new_size  # Update pixel size based on new grid size
        self.image_data = [[None] * self.grid_size for _ in range(self.grid_size)]
        self.canvas.config(width=self.canvas_size, height=self.canvas_size)
        self.preview_canvas.config(width=self.grid_size * self.preview_scale, height=self.grid_size * self.preview_scale)
        self.create_palette()
        self.create_grid()
        self.update_window_title()

    # Display information about the application
    def show_about(self):
        messagebox.showinfo("About", "Pixel Sprite Maker\nCreated by Washer.")

    # Save the current project as a .pix file
    def save_project(self, file_path):
        project_data = {
            'grid_size': self.grid_size,
            'image_data': self.image_data
        }
        with open(file_path, 'w') as file:
            json.dump(project_data, file)

    def save_project_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pix", filetypes=[("PIX files", "*.pix")])
        if file_path:
            self.save_project(file_path)

    # Load a project from a .pix file
    def load_project(self, file_path):
        with open(file_path, 'r') as file:
            project_data = json.load(file)
        self.grid_size = project_data['grid_size']
        self.image_data = project_data['image_data']
        self.pixel_size = self.canvas_size // self.grid_size

        # Update the canvas and preview canvas size
        self.canvas.config(width=self.canvas_size, height=self.canvas_size)
        self.preview_canvas.config(width=self.grid_size * self.preview_scale, height=self.grid_size * self.preview_scale)

        self.create_grid()
        self.update_window_title()

        # Restore the colors from image_data to the grid
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = self.image_data[row][col]
                if color is None:
                    color = 'white'  # Use white as the default color for transparent pixels in tkinter
                self.canvas.itemconfig(f'pixel_{row}_{col}', fill=color)
                self.update_preview(row, col, color)

    def load_project_as(self):
        file_path = filedialog.askopenfilename(defaultextension=".pix", filetypes=[("PIX files", "*.pix")])
        if file_path:
            self.load_project(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pixel Art Creator")
    app = PixelArtApp(root)
    root.mainloop()
