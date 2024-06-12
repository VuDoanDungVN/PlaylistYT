import tkinter as tk
from tkinter import messagebox
from create_playlist import add_video_to_playlist

def add_video_to_playlist_ui(service):
    def add_video():
        playlist_id = playlist_id_entry.get()
        video_id = video_entry.get()
        add_video_to_playlist(service, playlist_id, video_id)
        messagebox.showinfo("Success", "Video added to playlist")

    root = tk.Tk()
    root.title("Add Video to Playlist")
    root.geometry("300x200")
    
    tk.Label(root, text="Add Video", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(root, text="Playlist ID:").pack()
    playlist_id_entry = tk.Entry(root, width=30)
    playlist_id_entry.pack()

    tk.Label(root, text="Video ID:").pack()
    video_entry = tk.Entry(root, width=30)
    video_entry.pack()

    add_button = tk.Button(root, text="Add Video", command=add_video)
    add_button.pack(pady=10)

    root.mainloop()
