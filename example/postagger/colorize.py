import os
enable_color = 1

def col(text, fg, bg=None):
    """Return colorized text using terminal color codes; set util.enable_color
    = 0 to quickly make col() return plain un-colored text."""
    xterm = 0
    if os.environ["TERM"] == "xterm": 
        xterm = 1
    if enable_color:
        col_dict = {
            "black"     :   "30m",
            "red"       :   "31m",
            "green"     :   "32m",
            "brown"     :   "33m",
            "blue"      :   "34m",
            "purple"    :   "35m",
            "cyan"      :   "36m",
            "lgray"     :   "37m",
            "gray"      :   "1;30m",
            "lred"      :   "1;31m",
            "lgreen"    :   "1;32m",
            "yellow"    :   "1;33m",
            "lblue"     :   "1;34m",
            "pink"      :   "1;35m",
            "lcyan"     :   "1;36m",
            "white"     :   "1;37m",
        }
        b = "0m"
        s = "\033["
        clear = "0m"
        # In xterm, brown comes out as yellow..
        if xterm and fg == "yellow": color = "brown"
        f = col_dict[fg]
        if bg:
            if bg == "yellow" and xterm: 
                bg = "brown"
            try: 
                b = col_dict[bg].replace('3', '4', 1)
            except KeyError: 
                pass
        return "%s%s%s%s%s%s%s" % (s, b, s, f, text, s, clear)
    else:
        return text

