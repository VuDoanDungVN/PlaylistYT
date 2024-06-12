import tkinter as tk
from tkinter import messagebox, filedialog
from create_playlist import get_authenticated_service, create_playlist

def create_playlist_ui():
    service = get_authenticated_service()
    playlist_id = None

    def create():
        nonlocal playlist_id
        title = title_entry.get()
        description = description_entry.get()
        playlist_id = create_playlist(service, title, description)
        messagebox.showinfo("Success", f"Playlist created with ID: {playlist_id}")

    def open_add_video_ui():
        from add_video_playlist import add_video_to_playlist_ui
        add_video_to_playlist_ui(service)

    def open_remove_video_ui():
        from remove_video_playlist import remove_video_from_playlist_ui
        remove_video_from_playlist_ui(service)

    def upload_video_ids():
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if filename:
            # TODO: Add your code here to handle the uploaded file
            print(f'File uploaded: {filename}')

    root = tk.Tk()
    root.title("Playlist Manager")

    # Create Playlist section
    create_playlist_frame = tk.Frame(root)
    create_playlist_frame.pack(pady=10)

    tk.Label(create_playlist_frame, text="Create Playlist", font=("Arial", 14, "bold"), anchor="w").grid(row=0, column=0, columnspan=2, sticky="w", pady=10)

    tk.Label(create_playlist_frame, text="Title:", anchor="w").grid(row=1, column=0, sticky="w")
    title_entry = tk.Entry(create_playlist_frame, width=50)
    title_entry.grid(row=1, column=1)

    tk.Label(create_playlist_frame, text="Description:", anchor="w").grid(row=2, column=0, sticky="w")
    description_entry = tk.Entry(create_playlist_frame, width=50)
    description_entry.grid(row=2, column=1)

    create_button = tk.Button(create_playlist_frame, text="Create Playlist", command=create ,width=20, height=2)
    create_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Buttons section
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=10)

    button_width = 20  # Adjust this value to change the width of the buttons
    button_height = 2  # Adjust this value to change the height of the buttons

    add_video_button = tk.Button(buttons_frame, text="Add Video to Playlist", command=open_add_video_ui, width=button_width, height=button_height)
    add_video_button.grid(row=0, column=0, padx=5)

    remove_video_button = tk.Button(buttons_frame, text="Remove Video from Playlist", command=open_remove_video_ui, width=button_width, height=button_height)
    remove_video_button.grid(row=0, column=1, padx=5)
    
    upload_button = tk.Button(buttons_frame, text="Upload Video IDs", command=upload_video_ids, width=button_width, height=button_height)
    upload_button.grid(row=0, column=3, padx=5)

    root.mainloop()

if __name__ == "__main__":
    create_playlist_ui()