import tkinter

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 10

def layout( text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x > WIDTH - HSTEP:
            cursor_x = HSTEP
            cursor_y += VSTEP
    return display_list


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.display_list = []
        self.scroll = 0

        # event binding
        self.window.bind("<Down>", self.scroll_down)

    def load(self, text):
        self.display_list = layout(text)
        self.draw()

        # 책에서는 main 에서 호출해주고 있다.
        tkinter.mainloop()

    def draw(self):
        self.canvas.delete("all")
        for x,y,c in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            # 원래 위치보다 SCROLL_STEP 만큼 위로 올려서 그린다.
            self.canvas.create_text(x, y - self.scroll, text=c)

    def scroll_down(self, e):
        self.scroll += SCROLL_STEP
        self.draw()


        


