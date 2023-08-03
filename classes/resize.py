from PIL import Image
import os
import argparse
import sys


class ResizeImage:

    """Classe pour redimentionner une image"""

    def __init__(self, path, new_path=None, height=None, width=None):

        """
        Constructeur de la classe
        :param path: str, le path de l'image
        :param height: int, la hauteur souhaitée
        :param width: int, la largeur souhaitée
        """

        self.path = path
        self.height = height
        self.width = width
        self.new_path = new_path
        self.image = None
        self.ratio = None
        self.hsize = None
        self.wsize = None
        self.new_size = (None, None)

    def open_image(self):

        """Ouvre l'image"""

        try:
            self.image = Image.open(self.path)
        except FileNotFoundError:
            print(f"FileNotFoundError: No such file or directory:\n '{self.path}'")
            sys.exit(1)

    def calculate_ratio(self):

        """Calcule le ratio"""

        if self.width is not None:
            self.ratio = self.width / float(self.image.size[0])
        else:
            self.ratio = self.height / float(self.image.size[1])

    def height_size(self):

        """Calcule la hauteur si on a donner la largeur"""

        self.hsize = int((float(self.image.size[1]) * float(self.ratio)))

    def width_size(self):

        """Calcule la largeur si on a donner la hauteur"""

        self.wsize = int((float(self.image.size[0]) * float(self.ratio)))

    def img_resize(self):

        """Redimentionne l'image"""

        if self.width:
            self.height_size()
            self.image = self.image.resize((self.width, self.hsize), Image.ANTIALIAS)
        else:
            self.width_size()
            self.image = self.image.resize((self.wsize, self.height), Image.ANTIALIAS)

    def save(self):

        """Enregistre l'image redimmentionée en rajoutant 'resized' au nom
        de l'image
        Si self.new_path n'est pas définie enregistre l'image au même endroit
        que l'image originale
        Sinon enregistre l'image dans le nouveau path"""

        head, tail = os.path.split(self.path)
        name = 'resized_' + tail
        if self.new_path:
            try:
                os.chdir(self.new_path)
            except FileNotFoundError:
                os.makedirs(self.new_path)
            head = self.new_path
        path = os.path.join(head, name)
        self.image.save(path)

    def auto_resizing(self):

        """Auto redimentionnage"""

        self.open_image()
        if self.width and self.height:
            self.image = self.image.resize((self.width, self.height), Image.ANTIALIAS)
        else:
            self.calculate_ratio()
            self.img_resize()
        self.new_size = (self.image.size[0], self.image.size[1])
        self.save()
        print("Resized image created")


if __name__ == '__main__':

    def main():

        """Programe pricipal lors de l'execution du script"""

        args = parse_argument()
        try:
            path = args.path
            width = args.width
            height = args.height
            new_path = args.newpath
            if not (path and (width or height)):
                raise AttributeError
        except AttributeError:
            print('you must define a path with -p <path> and at least one of the\n'
                  'following attribute : width with -w <width> or height with -ht <height>')
        else:
            if width:
                width = int(width)
            if height:
                height = int(height)
            resize = ResizeImage(path, new_path=new_path, width=width, height=height)
            resize.auto_resizing()
            if args.verbose:
                new_size = resize.new_size
                verbosity(args, new_size)

    def verbosity(args, new_size):

        """Affiche les informations du redimentionnage"""

        if args.verbose:
            path = os.path.realpath(args.path)
            head, tail = os.path.split(args.path)
            width, height = new_size[0], new_size[1]
            new_name = 'resized_' + tail
            if args.newpath:
                head = args.newpath
            new_path = os.path.join(head, new_name)
            new_path = os.path.realpath(new_path)
            text = f"""    Image : {tail}
    Located at : {path}
    To : {new_name}
    Located at : {new_path}
    With new size : 
        width   {width} px
        height  {height} px"""
            print(text)

    def parse_argument():

        """
        Créer les arguments
        :return: les arguments parser
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--path", help="path to the file")
        parser.add_argument("-np", "--newpath", help="new path to the file")
        parser.add_argument("-w", "--width", help="desired image width")
        parser.add_argument("-ht", "--height", help="desired image height")
        parser.add_argument("-v", "--verbose", action="store_true",
                            help="increase output verbosity")

        return parser.parse_args()

    main()
