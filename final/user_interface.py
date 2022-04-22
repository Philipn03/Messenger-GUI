# Philip Nguyen
# philipbn@uci.edu
# 57277528

import tkinter as tk
from tkinter import ttk, filedialog
from Profile import Post
from NaClProfile import NaClProfile
import ds_client


class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self._posts = [Post]
        self._draw()
    
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._posts[index].entry
        self.set_text_entry(entry)
    
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        # TODO: Write code to that deletes all current text in the self.entry_editor widget
        # and inserts the value contained within the text parameter.
        try:
            self.entry_editor.delete(0.0,'end')          
            self.entry_editor.insert(0.0, text)
            # self.entry_editor.delete(1.0, tk.END)          
            # self.entry_editor.insert(0.0, text)
        except:
            print('Error')
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_posts(self, posts:list):
        # TODO: Write code to populate self._posts with the post data passed
        # in the posts parameter and repopulate the UI with the new post entries.
        # HINT: You will have to write the delete code yourself, but you can take 
        # advantage of the self.insert_posttree method for updating the posts_tree
        # widget.
        try:
            self._posts = posts
            for i in range(len(self._posts)):
                self._insert_post_tree(i, self._posts[i])
        except:
            print('Error')

    def insert_post(self, post: Post):
        self._posts.append(post)
        id = len(self._posts) - 1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, post)

    def reset_ui(self):
        self.set_text_entry("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    # show text on left hand side
    def _insert_post_tree(self, id, post: Post):
        entry = post.entry
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."
        
        self.posts_tree.insert('', id, id, text='pp')
    
    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, online_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        self.is_online = tk.IntVar()
        self._draw()
    
    def online_click(self):
        # TODO: Add code that implements a callback to the chk_button click event.
        # The callback should support a single parameter that contains the value
        # of the self.is_online widget variable.
        if self._online_callback is not None:
            self._online_callback(self.is_online.get())

    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()

    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        # self.chk_button.configure(command=self.online_click) 
        # self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

# class for main portion of root frame
# manages all method calls for the NaClProfile class
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._is_online = False
        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = NaClProfile()
        self._profile_filename = None
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    # new dsu file when 'New' clicked
    def new_profile(self):
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name

        # TODO Write code to perform whatever operations are necessary to prepare the UI for
        # a new DSU file.
        try:
            self._current_profile = NaClProfile()
            self._current_profile.generate_keypair()
            # self._current_profile.save_profile(self._profile_filename)
            self.body.reset_ui()
        except:
            print('Error')
        # print(self._current_profile.keypair)

    
    # open existing dsu file when 'Open' clicked
    # loads all data to ui
    def open_profile(self):
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        # TODO: Write code to perform whatever operations are necessary to prepare the UI for
        # an existing DSU file.
        try:
            self._profile_filename = filename.name
            self._current_profile = NaClProfile()
            self._current_profile.load_profile(self._profile_filename)
            self._current_profile.import_keypair(self._current_profile.keypair)
            self.body.reset_ui()
            self.body.set_posts(self._current_profile.get_posts())
        except:
            print('Error')

    # close program when 'Close' clicked
    def close(self):
        self.root.destroy()

    def save_profile(self):
        # TODO: Write code to perform whatever operations are necessary to save a 
        # post entry when the user clicks the save_button widget.
        # HINT: You will probably need to do things like create a new Post object,
        # fill it with text, add it to the active profile, save the profile, and
        # clear the editor_entry UI for a new post.
        try:
            post = Post(self.body.get_text_entry())
            self.body.insert_post(post)
            # self._current_profile.add_post(post)
            self._current_profile.save_profile(self._profile_filename)
            self.body.set_text_entry("")

            if self._is_online is True:
                self.publish(post)        
        except:
            print('Error')
    
    def publish(self, post:Post):
        # token = ds_client.connect('168.235.86.101', 3021, self._current_profile.username, self._current_profile.password, self._current_profile.public_key)
        token = ds_client.connect('168.235.86.101', 3021, 'dino321', 'rose', self._current_profile.public_key)
        post = self._current_profile.encrypt_entry(post['entry'], token)
        ds_client.send_message(post, self._current_profile.public_key)

 
    def online_changed(self, value:bool):
        try:
            if value == 1:
                self.footer.set_status("Online")
                self._is_online = True
            else:
                self.footer.set_status("Offline")
                self._is_online = False
            #print(self._is_online)
        except:
            print('Error')

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 
        menu_file.add_command(label='Add User', command=self.add_user)
        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback=self.online_changed)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
    
    def add_user():
        pass

if __name__ == "__main__":
    main = tk.Tk()

    main.title("ICS 32 Distributed Social Demo")

    main.geometry("720x480")

    main.option_add('*tearOff', False)

    MainApp(main)

    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())

    main.mainloop()
    