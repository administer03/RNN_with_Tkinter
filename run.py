import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model

from datetime import datetime
from pythainlp.util import thai_strftime

# plot function is created for
# plotting the graph in
# tkinter window
def plot(day):
	# messagebox.showinfo('waiting', 'กรุณารอสักครู่ ระบบกำลังประมวลผล')
	# window.destroy()

	# Create new window after click
	# root = Tk()
	# root.geometry('700x500')
	root = Toplevel(window)
	root.title('Prediction Result')
	root.geometry("1200x600")

	# ----------------------------------------------------------

	# # load model to predicting values
	

	model = load_model('LSTM_Model.h5')
	# model.summary()

	# # load excel file
	excel_file = pd.read_excel('excel_data.xlsx')


	# # get value to create a predict list
	prediction_list = excel_file['Selling Volumn'].iloc[-60:].tolist()
	prediction_list = np.array(prediction_list)
	# # prediction_list.shape
	prediction_list = np.reshape(prediction_list, (1, -1, 1))

	predicted_value = model.predict(prediction_list)
	# print(predicted_value)

	df = pd.DataFrame([], index=pd.date_range(datetime.today(), periods=day, freq='D'))

	df.index = df.index.normalize()
	df["Predicted Values"] = predicted_value[0]

	# plt.rcParams["figure.figsize"] = (17,8)

	x = df.index
	y = df["Predicted Values"]

	# ----------------------------------------------------------

	# the figure that will contain the plot
	fig = Figure(figsize = (5, 5),
				dpi = 100)

	# list of squares

	# adding the subplot
	plot1 = fig.add_subplot(111)

	

	# plotting the graph
	plot1.plot(x, y)
	plot1.scatter(x, y, color='black')
	plot1.grid(color = 'green', linestyle = '--', linewidth = 0.5)
	plot1.set_title("Next {} days prediction results".format(day))

	# creating the Tkinter canvas
	# containing the Matplotlib figure
	canvas = FigureCanvasTkAgg(fig,
							master = root)
	canvas.draw()

	# placing the canvas on the Tkinter window
	canvas.get_tk_widget().pack()

	# creating the Matplotlib toolbar
	toolbar = NavigationToolbar2Tk(canvas,
								root)
	toolbar.update()
	# placing the toolbar on the Tkinter window
	canvas.get_tk_widget().pack(side = BOTTOM, fill= BOTH, expand=True)


def tick():
    now = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')
    fmt = "วันเวลา ณ ปัจจุบัน\n%Aที่ %-d %B พ.ศ. %Y \n เวลา %H:%M:%S น."
	
	
    clock.config(text=thai_strftime(now, fmt))
    clock.after(200, tick)

# the main Tkinter window
window = Tk()
# window.columnconfigure(0, minsize=250)
# window.rowconfigure([0, 1, 2], minsize=100)
window.grid_columnconfigure((0, 1, 2), weight=1)

# setting the title
window.title('AI dealing with stock program')

# dimensions of the main window
window.geometry("1200x600")


####################################### CLOCK ################################################
clock = Label(window, font=("none", 40, "bold"), bg="white", fg="black", bd=5, relief="ridge")
tick() # it sill work if not send clock parameter



####################################### BUTTON ################################################
plot_button = Button(master = window,
					command=lambda: [plot(clicked.get())],
					height = 2,
					width = 30,
					text = "click เพื่อทำนาย",
					font=("none", 30, "bold"),
					fg='white', bg='#03c04a')


####################################### DropDown ################################################
options = [
    30
    # 45,
    # 60,
]

clicked = IntVar()

clicked.set('Select')

drop = OptionMenu( window , clicked , *options )



####################################### TEXT ################################################
lb = Label(window, text='เลือกจำนวนวันที่ต้องการทำนาย', font=("none", 20, "bold"))


#  Grid
clock.grid(row=0, column=1, padx = 4, pady = 40)
lb.grid(row=1, column=1)

drop.config(width=15)
drop["menu"].config(bg="#B8B8B8")
drop.grid(row=2, column=1)

plot_button.grid(row=3, column=1, padx = 4, pady = 40)

# Pack
# clock.pack()
# lb.pack(side=tkinter.LEFT)
# drop.pack(side=tkinter.LEFT)
# plot_button.pack()

window.mainloop()
