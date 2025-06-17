import customtkinter
from tkinter import filedialog
import threading
import subprocess
import os
import time

available_threads = len(os.sched_getaffinity(0))
lowest_threads = 1
highest_threads = available_threads

stop_event = threading.Event()
process = None
start_time = None
timer_job = None

tk = customtkinter

directoryPath = ""
onionsToGenerate = ""
intValue = lowest_threads

def select_output_folder():
    global directoryPath
    directoryPath = filedialog.askdirectory(mustexist=True)
    if directoryPath:
        dir_label.configure(text=f"Selected: {directoryPath}")

def onions_to_generate():
    global onionsToGenerate
    onionsToGenerate = entry.get().strip()

def update_label(value):
    global intValue
    intValue = int(float(value))
    label.configure(text=f"Threads to use: {intValue}")

def run_command():
    global stop_event, start_time
    onions_to_generate()
    if not directoryPath or not onionsToGenerate:
        textbox.insert(tk.END, "Select output folder and enter vanity onions to generate\n", "error")
        textbox.tag_config("error", foreground="red")
        return

    start_button.configure(state="disabled")
    stop_button.configure(state="normal")
    stop_event.clear()
    start_time = time.time()
    update_timer()
    textbox.delete("1.0", tk.END)
    threading.Thread(target=execute_command, daemon=True).start()

def execute_command():
    global process
    try:
        filters = onionsToGenerate.strip().split()
        args = ["./mkp224o"] + filters + ["-d", directoryPath, "-t", str(intValue)]
        if verbose.get() == "on":
            args.append("-s")

        print("Running:", " ".join(args))

        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in iter(process.stdout.readline, ''):
            if stop_event.is_set():
                break
            textbox.insert(tk.END, line)
            textbox.see(tk.END)

        process.stdout.close()
        if process.poll() is None:
            process.terminate()
            process.wait()

    except Exception as e:
        textbox.insert(tk.END, f"\n[Error] {str(e)}", "error")
        textbox.tag_config("error", foreground="red")
    finally:
        start_button.configure(state="normal")
        stop_button.configure(state="disabled")
        stop_timer()
        print("Terminated")

def stop_command():
    global process
    stop_event.set()
    if process and process.poll() is None:
        process.terminate()

def update_timer():
    global timer_job, start_time
    if start_time is None:
        return
    elapsed = int(time.time() - start_time)
    hrs = elapsed // 3600
    mins = (elapsed % 3600) // 60
    secs = elapsed % 60
    elapsed_time_label.configure(text=f"Time running: {hrs:02d}:{mins:02d}:{secs:02d}")
    timer_job = app.after(1000, update_timer)

def stop_timer():
    global timer_job, start_time
    if timer_job is not None:
        app.after_cancel(timer_job)
        timer_job = None
    start_time = None
    elapsed_time_label.configure(text="Time running: 00:00:00")

app = tk.CTk()
app.geometry("550x750")
app.title("mkp224o GUI")

input_frame = tk.CTkFrame(app)
input_frame.pack(padx=20, pady=10, fill="both", expand=False)

instruction_label = tk.CTkLabel(input_frame, text="Enter vanity onions (space separated):")
instruction_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

entry = tk.CTkEntry(input_frame, width=500)
entry.grid(row=1, column=0, padx=10, pady=(5, 10))

dir_frame = tk.CTkFrame(app)
dir_frame.pack(padx=20, pady=10, fill="both", expand=False)

select_dir_button = tk.CTkButton(dir_frame, text="Choose output folder", command=select_output_folder)
select_dir_button.grid(row=0, column=0, padx=10, pady=10)

dir_label = tk.CTkLabel(dir_frame, text="No folder selected")
dir_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

options_frame = tk.CTkFrame(app)
options_frame.pack(padx=20, pady=10, fill="both", expand=False)

label = tk.CTkLabel(options_frame, text=f"Threads to use: {intValue}")
label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

slider = tk.CTkSlider(options_frame, from_=lowest_threads, to=highest_threads, number_of_steps=max(1, highest_threads - lowest_threads), command=update_label)
slider.set(intValue)
slider.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="we")

verbose = tk.StringVar(value="on")
checkbox = tk.CTkCheckBox(options_frame, text="Verbose output", variable=verbose, onvalue="on", offvalue="off")
checkbox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")

control_frame = tk.CTkFrame(app)
control_frame.pack(padx=20, pady=10, fill="both", expand=False)

start_button = tk.CTkButton(control_frame, text="Start", command=run_command)
start_button.grid(row=0, column=0, padx=10, pady=10)

stop_button = tk.CTkButton(control_frame, text="Stop", command=stop_command)
stop_button.grid(row=0, column=1, padx=10, pady=10)
stop_button.configure(state="disabled")

output_frame = tk.CTkFrame(app)
output_frame.pack(padx=20, pady=10, fill="both", expand=True)

textbox = tk.CTkTextbox(output_frame, height=240, width=500)
textbox.pack(padx=10, pady=10, fill="both", expand=True)

elapsed_time_label = tk.CTkLabel(app, text="Time running: 00:00:00")
elapsed_time_label.pack(padx=10, pady=10)

app.mainloop()
