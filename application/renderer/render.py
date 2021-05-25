from jinja2 import Environment, FileSystemLoader

class Renderer():

    TEMPLATE_FILE = "ui_template.html"
    OUT_FILE = "../../../results.html"
    SIMILARITIES = 'sim'
    REORDERINGS = 'reo'

    def __init__(self, data, mode=SIMILARITIES):
        self.data = data
        self.mode = mode

    def render(self):
        templateLoader = FileSystemLoader(searchpath="./")
        templateEnv = Environment(loader=templateLoader)

        template = templateEnv.get_template(self.TEMPLATE_FILE)
        outputHTML = template.render({'data': self.data, 'mode': self.mode})  # this is where to put args to the template renderer

        with open(self.OUT_FILE, 'w') as f:
            f.write(outputHTML)
