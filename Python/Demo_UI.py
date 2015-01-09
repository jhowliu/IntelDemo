import sys
import pygtk
import gobject
pygtk.require('2.0')
import gtk
from Demo import *
pictureSize = [500, 500]

class Base:
    def __init__(self, filename1,filename2,filename3,filename4,filename5):

        [self.modelPool, self.p_tabel, self.dataPool, self.trainingLabel, self.scaleRange, self.scaleMin, self.LogRegPool] = Run([filename1,filename2,filename3,filename4], filename5)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.fullscreen()
        self.window.connect("delete_event", gtk.main_quit)

        self.hbox_welcome = gtk.HBox()
        self.hbox_result = gtk.HBox()
        self.hbox_origin = gtk.HBox(spacing = 3)
        self.vbox_whole = gtk.VBox(spacing = 3)

        self.model_user1 = gtk.Label()
        self.model_user2 = gtk.Label()
        self.model_user3 = gtk.Label()
        self.model_user4 = gtk.Label()

        string = "Han\n\n 0 % \n\n 0 %"
        self.model_user1.set_label(string)
        self.hbox_origin.add(self.model_user1)


        string = "Jhow\n\n 0 % \n\n 0 %"
        self.model_user2.set_label(string)
        self.hbox_origin.add(self.model_user2)

        string = "Jing\n\n 0 % \n\n 0 %"
        self.model_user3.set_label(string)
        self.hbox_origin.add(self.model_user3)

        string = "Rick\n\n 0 % \n\n 0 %"
        self.model_user4.set_label(string)
        self.hbox_origin.add(self.model_user4)



        #Welcome String
        self.welcome_label = gtk.Label()
        self.welcome_label.set_use_markup(gtk.TRUE)
        self.welcome_label.set_markup('<span size="200000">Welcome to Intel Smart House!!</span>')
        self.hbox_welcome.add(self.welcome_label)

        #Result
        self.result_label = gtk.Label()
        self.result_label.set_use_markup(gtk.TRUE)
        self.result_label.set_markup('<span size="200000">Who are you?</span>')
        self.hbox_result.add(self.result_label)

        result_picture = gtk.gdk.pixbuf_new_from_file("src/ques.jpg")
        #Resize Image
        scaled_result_picture = result_picture.scale_simple(pictureSize[0], pictureSize[1],gtk.gdk.INTERP_BILINEAR)
        #Set Image on Window
        self.image_result_picture = gtk.Image()
        self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        self.hbox_result.add(self.image_result_picture)
        #Add to hbox 

        self.vbox_whole.add(self.hbox_welcome)
        self.vbox_whole.add(self.hbox_result)
        self.vbox_whole.add(self.hbox_origin)
        self.window.add(self.vbox_whole)
        self.window.show_all()

        while (1):
            self.scanning()
        print "stop here"

    def scanning(self):
        while gtk.events_pending():
            gtk.main_iteration(False)

        self.welcome_label.set_markup('<span size="200000">Detecting!!</span>')
        self.receiving()

        return True

    def receiving(self):
        pVal = Ready(self.modelPool, self.p_tabel, self.dataPool, self.trainingLabel, self.scaleRange, self.scaleMin, self.LogRegPool)
        #Prediction result is Han.
        if pVal == 0:
            self.result_label.set_markup('<span size="200000">Hi, Han!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/Han.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0], PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Jhow.
        elif pVal == 1:
            self.result_label.set_markup('<span size="200000">Hi, Jhow!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/jhow.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0], PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Rick.
        elif pVal == 2:
            self.result_label.set_markup('<span size="200000">Hi, Jing!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/jing.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0], PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Yo.
        elif pVal == 3:
            self.result_label.set_markup('<span size="200000">Hi, Rick!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/rick.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0],PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is intruder.
        elif pVal == -1:
            self.result_label.set_markup('<span size="200000">Intruder!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/intruder.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0],PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        while gtk.events_pending():
            gtk.main_iteration(False)

    def main(self):
        gtk.main()


if __name__=='__main__':
    if len(sys.argv) < 6:
        print "Usage: <Data>"
        exit(-1)
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    filename3 = sys.argv[3]
    filename4 = sys.argv[4]
    filename5 = sys.argv[5]
    base = Base(filename1,filename2,filename3,filename4,filename5)
