import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from PIL import Image, ImageTk  

import cal
from typhoonClient import get_explanation

global output_df

def BuildMateApp():
    
    # Initialize main window
    window = ttk.Window()
    window.title("Build Mate")
    window.config(bg='#DC143C')
    window.geometry("1350x850")
    
    window.grid_rowconfigure(2, weight = 1)
    window.grid_columnconfigure(0, weight = 1)
    
    s = ttk.Style()
    s.configure('Red.TFrame', background='#DC143C')
    s.configure('White.TFrame', background='#FFFFFF', highlightcolor='#DC143C',highlightthickness=50)
    
    icon_frame = ttk.Frame(window, style='White.TFrame')
    icon_frame.grid(row=0, column=0,ipady=0,ipadx=1400, columnspan=5)
    # Company Icon
    # get Directory
    Dir = os.getcwd()
    path = 'buildmate_name.png'
    path = os.path.join(Dir, path)
    # open Img
    original_icon = Image.open(path)  # Replace 'buildmate_name.png' with the path to your icon file
    scale_up = 1
    resized_icon = original_icon.resize((int(202*scale_up), int(52*scale_up)))  # Resize the icon
    icon = ImageTk.PhotoImage(resized_icon)
    icon_label = ttk.Label(icon_frame, image=icon)
    icon_label.grid(row=0, column=0, padx=25, pady=25 , sticky='W')

    # L Content Area Frame (White Background Layer)
    content_layer = ttk.Frame(window, style='White.TFrame', padding=10, width=600)
    content_layer.grid(row=2, column=0, columnspan=4, sticky='nsew', padx=25, pady=25)
    # R Content Area Frame (White Background Layer)
    Rcontent_layer = ttk.Frame(window, style='White.TFrame', padding=10, width=600)
    Rcontent_layer.grid(row=2, column=1, columnspan=4, sticky='nsew', padx=25, pady=25)

    # Variable Used in Calculation Label
    calc_label = ttk.Label(content_layer, text="ตัวแปรที่ใช้ในการคำนวณ", font=('Kanit', 20, 'bold'), foreground='blue', anchor='w')
    calc_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    # Entry Labels
    quantity_label = "จำนวนสินค้า"
    cost_label = "ต้นทุนสินค้า"
    sale_price_label = "ราคาขายหลังส่วนลดป้ายเหลือง"
    min_discount_label = "ส่วนลด ราคาป้ายเหลือง ขั้นต่ำ"
    max_discount_label = "ส่วนลด ราคาป้ายเหลือง ขั้นสุด"
    min_coupon_label = "ส่วนลด คูปอง ขั้นต่ำ"
    max_coupon_label = "ส่วนลด คูปอง ขั้นสุด"
    
    labels = [
        quantity_label, cost_label, sale_price_label, min_discount_label,
        max_discount_label, min_coupon_label, max_coupon_label
    ]

    entries = {}
    for i, label_text in enumerate(labels):
        label = ttk.Label(content_layer, text=label_text, font=('Kanit', 13, 'bold'))
        label.grid(row=i + 1, column=0, padx=10, pady=5, sticky='w')
        entry = ttk.Entry(content_layer, width=14)
        entry.grid(row=i + 1, column=1, padx=10, pady=5)
        entries[label_text] = entry

    # Function Label
    Func_label = ttk.Label(content_layer, text="การประมวลผล", font=('Kanit', 20, 'bold'), foreground='blue', anchor='w')
    Func_label.grid(row=8, column=0, padx=10, pady=10, sticky='w')

    # Flag to check if calculate button has been clicked
    calculate_clicked = {'status': False}
    selected_directory = {'path': None}
    output_df = {'data': None}
    ams_check = {'state': False}

    # ams_check Button
    def toggle_ams_chec():
        if true_false_button.config('text')[-1] == 'False':
            true_false_button.config(text='True')
            ams_check['state'] = True
        else:
            true_false_button.config(text='False')
            ams_check['state'] = False

    true_false_label = ttk.Label(content_layer, text="คำนวณค่า Affiliate", font=('Kanit', 13, 'bold'))
    true_false_label.grid(row=9, column=0, padx=10, pady=5, sticky='w')
    true_false_button = ttk.Button(content_layer, text='False', command=toggle_ams_chec, bootstyle=PRIMARY)
    true_false_button.grid(row=9, column=1, padx=0, pady=5, sticky='w')


    # Calculate Button
    calculate_label = ttk.Label(content_layer, text="คำนวณผลลัพธ์", font=('Kanit', 13, 'bold'))
    calculate_label.grid(row=10, column=0, padx=10, pady=5, sticky='w')
    def calculate():
        file_name = file_name_entry.get().strip()
        selected_directory['path']
        if not file_name or not selected_directory['path']:
            Cstatus_label.config(text="Error", foreground='red')
            calculate_clicked['status'] = False
            return
        
        # Retrieve values from entries   
        unit = entries[quantity_label].get()
        cogs_unit = entries[cost_label].get()
        gross_revenue = entries[sale_price_label].get()
        discount_sign_min = entries[min_discount_label].get()
        discount_sign_max = entries[max_discount_label].get()
        discount_promotion_min = entries[min_coupon_label].get()
        discount_promotion_max = entries[max_coupon_label].get()
        
        if selected_directory['path']:
            file_name = file_name_entry.get().strip()
            if file_name is not None:
                full_path = os.path.join(selected_directory['path'], file_name + '.csv')
                ams_state = ams_check['state']
                output_df['data'] = cal.calculation(unit, cogs_unit, gross_revenue, discount_sign_min, discount_sign_max, discount_promotion_min, discount_promotion_max, ams_state)
                csv_data = cal.export_csv(output_df['data'], full_path)
               
                # print("Calculation output:", output_csv)
                typhoon_write_content = get_explanation(csv_data)
                insert_typhoon_text(typhoon_write_content)
                Cstatus_label.config(text="Pass", foreground='green')
                calculate_clicked['status'] = True
       
        
    calculate_button = ttk.Button(content_layer, text="Calculate", command=calculate, bootstyle=SUCCESS)
    calculate_button.grid(row=10, column=1, padx=0, pady=10, sticky='w')

    # Calculate Status Label
    Cstatus_label = ttk.Label(content_layer, font=('Kanit', 13, 'bold'))
    Cstatus_label.grid(row=10, column=2, padx=00, pady=10, sticky='w')

    # Reset Button
    reset_label = ttk.Label(content_layer, text="ตั้งใหม่", font=('Kanit', 13, 'bold'))
    reset_label.grid(row=11, column=0, padx=10, pady=5, sticky='w')
    def reset():
        for label, entry in entries.items():
            if label != "กำหนด File path":
                entry.delete(0, ttk.END)
            file_name_entry.delete(0, ttk.END)
            typhoon_text.delete('1.0', ttk.END)
            calculate_clicked['status'] = False
            status_label.config(text="", font=('Kanit', 13, 'bold')) 
            Cstatus_label.config(text="", font=('Kanit', 13, 'bold')) 
    reset_button = ttk.Button(content_layer, text="Reset", command=reset, bootstyle=DANGER)
    reset_button.grid(row=11, column=1, padx=0, pady=10, sticky='w')

    # Output preparation Label
    calc_label = ttk.Label(Rcontent_layer, text="เตรียมผลลัพธ์", font=('Kanit', 20, 'bold'), foreground='blue')
    calc_label.grid(row=0, column=2,padx=0, pady=10, sticky='NESW')

    # File Name and File Path
    file_name_label = ttk.Label(Rcontent_layer, text="กำหนดชื่อไฟล์", font=('Kanit', 13, 'bold'))
    file_name_label.grid(row=1, column=2, padx=0, pady=5, sticky='w')
    file_name_entry = ttk.Entry(Rcontent_layer)
    file_name_entry.grid(row=1, column=3, padx=0, pady=5, sticky='w')

    file_path_label = ttk.Label(Rcontent_layer, text="กำหนด File path", font=('Kanit', 13, 'bold'))
    file_path_label.grid(row=2, column=2, padx=0, pady=5, sticky='w')
    file_path_entry = ttk.Entry(Rcontent_layer)
    file_path_entry.grid(row=2, column=3, padx=0, pady=5)
    
    def select_file_path():
        file_path = filedialog.askdirectory()
        if file_path:
            file_path_entry.delete(0, ttk.END)
            file_path_entry.insert(0, file_path)
            selected_directory['path'] = file_path

    file_path_button = ttk.Button(Rcontent_layer, text="Select Path", command=select_file_path, bootstyle=PRIMARY)
    file_path_button.grid(row=2, column=4, padx=10, pady=5)

    download_label = ttk.Label(Rcontent_layer, text="ดาวน์โหลดตาราง", font=('Kanit', 13, 'bold'))
    download_label.grid(row=3, column=2, padx=0, pady=5, sticky='w')
    # Download Button
    def download_action():
        if calculate_clicked['status'] and selected_directory['path']:
            file_name = file_name_entry.get().strip()
            if file_name and output_df['data'] is not None:
                full_path = os.path.join(selected_directory['path'], file_name + '.csv')
                cal.export_csv(output_df['data'], full_path)
                print(f"File will be saved at: {full_path}")
                # Update status LED to green and show "Download Pass"
                status_label.config(text="Pass", foreground='green')
            else:
                # Update status LED to indicate error
                status_label.config(text="Error", foreground='red')
        else:
            # Update status LED to indicate error
            status_label.config(text="Error", foreground='red')

    download_button = ttk.Button(Rcontent_layer, text="Download", command=download_action, bootstyle=SUCCESS)
    download_button.grid(row=3, column=3, padx=0, pady=10, sticky='w')

    # Download Status Label
    status_label = ttk.Label(Rcontent_layer, font=('Kanit', 13, 'bold'))
    status_label.grid(row=3, column=4, padx=10, pady=10, sticky='w')

    # Typhoon Suggestions Label
    typhoon_label = ttk.Label(Rcontent_layer, text="แนะนำโปรโมชั่นใน Shopee", font=('Kanit', 20, 'bold'), foreground='blue')
    typhoon_label.grid(row=4, column=2, padx=0, pady=10)
    typhoon_text_frame = ttk.Frame(Rcontent_layer)
    typhoon_text_frame.grid(row=5, column=2, columnspan=5, padx=0, pady=10,sticky='w')

    typhoon_scrollbar = ttk.Scrollbar(typhoon_text_frame)
    typhoon_scrollbar.pack(side='right', fill='y')

    typhoon_text = ttk.Text(typhoon_text_frame, height=11, width=50, yscrollcommand=typhoon_scrollbar.set, font=('Kanit', 11))
    typhoon_text.pack(side='left', fill='both', expand=True)

    typhoon_scrollbar.config(command=typhoon_text.yview)
    
    # Add function to insert text into typhoon_text
    def insert_typhoon_text(text):
        typhoon_text.delete("1.0", "end")  # Delete all existing content
        typhoon_text.insert("1.0", text + "\n")  # Insert new text at the beginning

    # Start main loop
    window.mainloop()

if __name__ == "__main__":
    BuildMateApp()