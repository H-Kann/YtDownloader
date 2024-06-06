import customtkinter as ctk

class ContextMenu(ctk.CTkToplevel):
    
    def __init__(self,
                 master= None,
                 corner_radius=15,
                 border_width=1,
                 **kwargs):
        
        super().__init__(takefocus=1)
        
        self.focus()
        self.master_window = master
        self.corner = corner_radius
        self.border = border_width
        self.hidden = True

        # add transparency
        self.after(100, lambda: self.overrideredirect(True))
        self.transparent_color = self._apply_appearance_mode(self._fg_color)
        self.attributes("-transparentcolor", self.transparent_color)
        self.frameMenu = ctk.CTkFrame(self, bg_color=self.transparent_color, corner_radius=self.corner,
                              border_width=self.border, **kwargs)
        self.frameMenu.pack(expand=True, fill="both")
        
        self.master.bind("<Button-1>", lambda event: self._withdraw_off(), add="+") # hide menu when clicked outside
        self.bind("<Button-1>", lambda event: self._withdraw()) # hide menu when clicked inside
        self.master.bind("<Configure>", lambda event: self._withdraw()) # hide menu when master window is changed
        
        self.resizable(width=False, height=False)
        self.transient(self.master_window)
         
        self.update_idletasks()
        
        self.withdraw()
        
    def _withdraw(self):
        self.withdraw()
        self.hidden = True

    def _withdraw_off(self):
        if not self.hidden:
            self.withdraw()
        self.hidden = True
        
    def popup(self, x=None, y=None):
        self.x = x
        self.y = y
        self.deiconify()
        self.geometry('+{}+{}'.format(self.x, self.y))
        self.hidden = False
        
