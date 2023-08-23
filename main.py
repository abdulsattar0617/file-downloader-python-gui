import tkinter as tk 
from tkinter import filedialog , ttk 
from tkinter import *
import requests 
import os 

class Downloader:
    
    def __init__(self):
        self.saveto = "" 
        self.cancel_request = False  
        self.cancelled = False 
        self.entry_placeholder_text = "  Paste file url" 
        self.font = "Helvetica" 
        self.frame_color = "white" 
        self.window_color = "#dbeb34" 
        self.window = tk.Tk() 
        self.window.geometry("500x420") 
        self.window.configure(bg=self.window_color)

        self.frame = tk.Frame(height = 350, width = 400, bg = self.frame_color, borderwidth=5, highlightbackground="white", highlightthickness=2)
        self.frame.place(x=50, y=40) 
        self.window.title("File Downloader")   

        self.windowHead = tk.Label(text="Sofftech", bg=self.window_color, fg="black", font=(self.font, '18'))
        # self.windowHead.place(x=50, y=5)

        self.url_label = tk.Label(text="File Downloader", bg=self.frame_color, font=(self.font, '20', 'bold'))
        self.url_label.place(x=70, y=60)

        self.tagline = tk.Label(text="Paste any url of Image, Video or PDF to download.", bg=self.frame_color, font=('bahnschrift 12'))  
        self.tagline.place(x=70, y=100) 

        self.url_entry = tk.Entry(width=22, font=(self.font,'22'), bg=self.frame_color)
        self.url_entry.insert(0,self.entry_placeholder_text) 
        self.url_entry.place(x=72, y=140) 
        self.url_entry.configure(fg="gray") 
        

        self.browse_button = tk.Button(text="Save as/Edit File Name",bg="#6ca0dc",fg="white", command=self.browse_file, width=29,font=(self.font, '16'))  
        self.browse_button.place(x=72, y=190) 
        self.browse_button["border"] = "0" 

        self.cancel_button = tk.Button(text="Cancel Download",fg="white",bg="#FF5A5F", command=self.cancel_download, width=20,font=(self.font, '12'))
        self.cancel_button.place(x=72, y=320+10)
        self.cancel_button["border"] = "0"

        self.download_button = tk.Button(text="Download File", fg="white", bg="#6ca0dc", command=self.download, width=29,font=(self.font, '16'))
        self.download_button.place(x=72, y=235)  
        self.download_button["border"] = "0"

        style = ttk.Style()
        style.theme_use('alt')
        style.configure("orange.Horizontal.TProgressbar", foreground='orange', background='orange')
        
        
        self.progress_bar = ttk.Progressbar(self.window, style="orange.Horizontal.TProgressbar",orient="horizontal",maximum=100, length=300, mode="determinate")  
        self.progress_bar.place(x=72, y=290+10)  
        

        self.progress_percent = tk.Label(text=f" {0} % ", bg=self.frame_color, width=5,font=(self.font,'10')) 
        self.progress_percent.place(x=390, y=280+10) 

        self.progress_patch = tk.Label(text=f"    ", bg=self.frame_color, width=40,font=(self.font, '10')) 
        self.progress_patch.place(x=72, y=296+10)  

        self.window.mainloop() 

    def browse_file(self):
        saveto = filedialog.asksaveasfilename(initialfile=self.url_entry.get().split("/")[-1].split("?")[0] )  
        self.saveto = saveto   

    def init_components(self):
        self.cancel_request = False  
        self.cancelled = False 
        self.progress_percent.config(text=f" {0} % ") 
        self.progress_bar["value"] = 0
        self.url_entry.delete(0, END) 
        self.url_entry.configure(fg="gray") 
        self.url_entry.insert(0,self.entry_placeholder_text)

    def cancel_download(self):
        self.cancel_request = True 
        if self.cancelled: 
            os.remove(self.saveto)  
            self.init_components() 

        
       
    def validate(self):
        if self.url_entry.get() == self.entry_placeholder_text or self.url_entry.get() == "": 
            self.url_entry.config(highlightbackground="red", highlightthickness=1) 
            self.url_entry.configure(fg="#ff6347") 
            return False 
             
        else:
            return True  
           

    def download(self): 
        # print(self.url_entry.get())

        if self.validate() and (not self.cancel_request): 
            url = self.url_entry.get() 
            response = requests.get(url, stream=True)  
            total_size_in_bytes = int(response.headers.get("Content-Length"))    
            block_size = 10000 # bytes 
            self.progress_bar["value"] = 0 

            fileName = self.url_entry.get().split("/")[-1].split("?")[0] 
            if self.saveto == "":
                self.saveto = fileName 


            # print(self.saveto) 
            
            with open(self.saveto, "wb") as f:  
                for data in response.iter_content(block_size):
                    if self.cancel_request: 
                        f.close() 
                        self.cancelled = True 
                        self.cancel_download() 
                        break 
                    self.progress_bar["value"] += (100*block_size)/total_size_in_bytes 
                    
                    percent = int(self.progress_bar["value"])  
                    self.progress_percent.config(text=f" {percent} % ") 
                    # print(self.progress_bar["value"]) # prints progress percent on console

                    self.window.update() 
                    f.write(data) 
        else:
            self.validate() 


if __name__ == "__main__":
    
    Downloader() 
    