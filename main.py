import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

FONT = ('times', 18, 'bold')
FONT_BUTTON = ('times', 9, 'bold')

window = Tk()
window.geometry("1600x800")
window.title("IMAGE WATERMARKER")
window.config(padx=150, pady=80)


l1 = Label(text='Upload Image', width=30, font=FONT)
l1.grid(row=1, column=1)

b1 = Button(text='Select file', width=20, font=FONT_BUTTON, command=lambda: upload_image())
b1.grid(row=2, column=1)

l2 = Label(text='Upload Watermark', width=30, font=FONT)
l2.grid(row=1, column=3)

b3 = Button(text='Select file', width=20, font=FONT_BUTTON, command=lambda: upload_watermark())
b3.grid(row=2, column=3)


l3 = Label(text="Enter text for watermark", width=40, font=FONT)
l3.grid(row=1, column=2)

watermark_text = Entry(width=40)
watermark_text.grid(row=2, column=2)


def upload_image():
    global img
    global img_original
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    img_original = img
    width, height = img.size
    width_new = int(width / 10)
    height_new = int(height / 10)
    img_resized = img.resize((width_new, height_new))
    img = ImageTk.PhotoImage(img_resized)

    b2 = Button(image=img) # using Button
    b2.grid(row=3, column=1)

    b5 = Button(text='WATERMARK', width=40, height=4, font=FONT_BUTTON, bg='green', command=lambda: watermark())
    b5.grid(row=7, column=2)


def upload_watermark():
    global watermark_img
    global watermark_img_original

    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    watermark_img = Image.open(filename)
    watermark_img_original = watermark_img
    width, height = watermark_img.size
    width_new = int(width / 20)
    height_new = int(height / 20)
    watermark_img_resized = watermark_img.resize((width_new, height_new))
    watermark_img = ImageTk.PhotoImage(watermark_img_resized)
    # Show image
    b4 = Button(image=watermark_img) # using Button
    b4.grid(row=3, column=3)
    # Button for watermark


def watermark():
    # Get name of the picture file
    image_name = img_original.filename.split('/')[-1].split(".")[0]

    # Make copy to use it for text watermark
    img_original_copy_for_text = img_original.copy()

    # Get image size
    width, height = img_original_copy_for_text.size

    # Calculate the x,y coordinates of the text
    margin = 10
    x = width - (width / 5) - margin
    y = height - (height / 8) - margin

    # Lamp to determine if something is saved
    lamp = False
    # Save text watermark
    text = watermark_text.get()
    if text != "":
        draw = ImageDraw.Draw(img_original_copy_for_text)

        font_size = int(width / 25)
        curr_font = ImageFont.truetype('arial.ttf', font_size)
        # draw watermark in the bottom right corner
        draw.text((x, y), text, font=curr_font)
        img_original_copy_for_text.save(f'{image_name}_watermark_text.jpg')
        lamp = True

    # Save picture watermark
    try:
        width_watermark, height_watermark = watermark_img_original.size

        img_original.paste(watermark_img_original.resize((int(width_watermark / 10), int(height_watermark / 10))), (int(x), int(y)))
        img_original.save(f'{image_name}_watermark_picture.jpg')
        lamp = True
    except NameError:
        pass

    # Success message popup
    if lamp:
        tkinter.messagebox.showinfo(title="Successfully", message="Picture watermarked successfully.")
    else:
        tkinter.messagebox.showerror(title="Error", message="Nothing saved. Either select image or enter text for watermark!!!")


if __name__ == '__main__':
    window = mainloop()
