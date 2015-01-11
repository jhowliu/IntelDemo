import sys
sys.path.append('./lib/')
import pygtk
import gobject
pygtk.require('2.0')
import gtk
import time
import threading
pictureSize = [400, 400]

class Base(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.maximize()
        self.window.connect("delete_event", gtk.main_quit)

        self.hbox_welcome = gtk.HBox()
        self.hbox_result = gtk.HBox()
        self.hbox_origin = gtk.HBox(spacing = 3)
        self.vbox_whole = gtk.VBox(spacing = 3)
        
        self.user1_hbox = gtk.HBox()
        self.user2_hbox = gtk.HBox()
        self.user3_hbox = gtk.HBox()
        self.user4_hbox = gtk.HBox()

        self.model_user1 = gtk.Label()
        self.model_user2 = gtk.Label()
        self.model_user3 = gtk.Label()
        self.model_user4 = gtk.Label()

        string = "Han\n\n 0 % \n\n 0 %"
        self.model_user1.set_label(string)
        result_picture = gtk.gdk.pixbuf_new_from_file("src/han.jpg")
        #Resize Image
        scaled_result_picture = result_picture.scale_simple(100, 100,gtk.gdk.INTERP_BILINEAR)
        #Set Image on Window
        user1_image = gtk.Image()
        user1_image.set_from_pixbuf(scaled_result_picture)
        self.user1_hbox.add(user1_image)
        self.user1_hbox.add(self.model_user1)
        self.hbox_origin.add(self.user1_hbox)


        string = "Jhow\n\n 0 % \n\n 0 %"
        self.model_user2.set_label(string)
        result_picture = gtk.gdk.pixbuf_new_from_file("src/jhow.jpg")
        #Resize Image
        scaled_result_picture = result_picture.scale_simple(100, 100,gtk.gdk.INTERP_BILINEAR)
        #Set Image on Window
        user2_image = gtk.Image()
        user2_image.set_from_pixbuf(scaled_result_picture)
        self.user2_hbox.add(user2_image)
        self.user2_hbox.add(self.model_user2)
        self.hbox_origin.add(self.user2_hbox)

        string = "Jing\n\n 0 % \n\n 0 %"
        self.model_user3.set_label(string)
        result_picture = gtk.gdk.pixbuf_new_from_file("src/jing.jpg")
        #Resize Image
        scaled_result_picture = result_picture.scale_simple(100, 100,gtk.gdk.INTERP_BILINEAR)
        #Set Image on Window
        user3_image = gtk.Image()
        user3_image.set_from_pixbuf(scaled_result_picture)
        self.user3_hbox.add(user3_image)
        self.user3_hbox.add(self.model_user3)
        self.hbox_origin.add(self.user3_hbox)

        string = "Rick\n\n 0 % \n\n 0 %"
        self.model_user4.set_label(string)
        result_picture = gtk.gdk.pixbuf_new_from_file("src/rick.jpg")
        #Resize Image
        scaled_result_picture = result_picture.scale_simple(100, 100,gtk.gdk.INTERP_BILINEAR)
        #Set Image on Window
        user4_image = gtk.Image()
        user4_image.set_from_pixbuf(scaled_result_picture)
        self.user4_hbox.add(user4_image)
        self.user4_hbox.add(self.model_user4)
        self.hbox_origin.add(self.user4_hbox)


        #Welcome String
        self.welcome_label = gtk.Label()
        self.welcome_label.set_use_markup(gtk.TRUE)
        self.welcome_label.set_markup('<span size="50000">Welcome to Intel Smart House!!</span>')
        self.hbox_welcome.add(self.welcome_label)

        #Result
        self.result_label = gtk.Label()
        self.result_label.set_use_markup(gtk.TRUE)
        self.result_label.set_markup('<span size="100000">Who are you?</span>')
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

    def predict(self, pVal, probs):
        print "pVal: ", pVal
        if pVal != -2:
            string = "Han\n\n" + str(probs[0][0]) + "\n\n" + str(probs[0][1])
            self.model_user1.set_label(string)

            string = "Jhow\n\n" + str(probs[1][0]) + "\n\n" + str(probs[1][1])
            self.model_user2.set_label(string)

            string = "Jing\n\n" + str(probs[2][0]) + "\n\n" + str(probs[2][1])
            self.model_user3.set_label(string)

            string = "Rick\n\n" + str(probs[3][0]) + "\n\n" + str(probs[3][1])
            self.model_user4.set_label(string)

        #Prediction result is Han.
        if pVal == 0:
            self.result_label.set_markup('<span size="100000">Hi, Han!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/Han.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(pictureSize[0], pictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Jhow.
        elif pVal == 1:
            self.result_label.set_markup('<span size="100000">Hi, Jhow!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/jhow.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(pictureSize[0], pictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Jing
        elif pVal == 2:
            self.result_label.set_markup('<span size="100000">Hi, Jing!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/jing.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(pictureSize[0], pictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Rick.
        elif pVal == 3:

            self.result_label.set_markup('<span size="100000">Hi, Rick!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/rick.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(pictureSize[0],pictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is intruder.
        elif pVal == -1:
            self.result_label.set_markup('<span size="100000">Intruder!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/intruder.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(pictureSize[0],pictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        if pVal == -1:
            self.welcome_label.set_markup('<span size="100000" color="red">Warning!!</span>')
        else:
            self.welcome_label.set_markup('<span size="100000" color="green">Welcom To Smart Home!!</span>')

        while gtk.events_pending():
            gtk.main_iteration(False)


    def main(self):
        gtk.main()
