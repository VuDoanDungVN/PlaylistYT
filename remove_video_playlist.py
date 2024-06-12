import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from create_playlist import remove_video_from_playlist
def remove_video_from_playlist_ui(service, playlist_id):
    video_id = askstring("Video ID", "Enter the ID of the video you want to remove:")
    if video_id:
        remove_video_from_playlist(service, playlist_id, video_id)
        messagebox.showinfo("Success", "Video removed from playlist")
    else:
        messagebox.showwarning("Warning", "Please enter a valid video ID.")
