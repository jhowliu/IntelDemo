import sys
import pygtk
pygtk.require('2.0')
import gtk
PictureSize = (500, 500)
class Base:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(1920, 1080)
        self.window.connect("delete_event", gtk.main_quit)

        self.hbox_welcome = gtk.HBox()
        self.hbox_result = gtk.HBox()
        self.hbox_origin = gtk.HBox(spacing = 3)
        self.vbox_whole = gtk.VBox(spacing = 3)

        self.model_user1 = gtk.Label()
        self.model_user2 = gtk.Label()
        self.model_user3 = gtk.Label()
        self.model_user4 = gtk.Label()
        '''
        #Read Image
        origin_acc_y = gtk.gdk.pixbuf_new_from_file("test.png")
        #Resize Image
        scaled_acc_y = origin_acc_y.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
        #Set Image on Window
        image_acc_y = gtk.Image()
        image_acc_y.set_from_pixbuf(scaled_acc_y)
        #Add to hbox
        self.hbox_origin.add(image_acc_y)
        '''
        # got the result from prediction
        ###
        ###

        self.model_user1.set_label("")
        self.hbox_origin.add(self.model_user1)

        self.model_user2.set_label("")
        self.hbox_origin.add(self.model_user2)

        self.model_user3.set_label("")
        self.hbox_origin.add(self.model_user3)

        self.model_user4.set_label("")
        self.hbox_origin.add(self.model_user4)


        #Welcome String
        self.welcome_label = gtk.Label()
        self.welcome_label.set_use_markup(gtk.TRUE)
        self.welcome_label.set_markup('<span size="125000">Welcome to Intel Smart House!!</span>')
        self.hbox_welcome.add(self.welcome_label)

        #Result
        self.result_label = gtk.Label()
        self.result_label.set_use_markup(gtk.TRUE)
        self.result_label.set_markup('<span size="200000">Who are you?</span>')
        self.hbox_result.add(self.result_label)

        #Initial picture
        #Read Image
        result_picture = gtk.gdk.pixbuf_new_from_file("src/ques.jpg")
        #Resize Image
        scaled_result_picture = result_picture.scale_simple(PictureSize[0], PictureSize[1],gtk.gdk.INTERP_BILINEAR)
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
        print "In UI pval:" + str(pVal)
        #Prediction result is Han.
        if pVal == 0:
            string = "Han\n\n" + probs[0][0] + '\n\n' + probs[0][1]
            self.model_user1.set_label(string)
            result_label.set_markup('<span size="100000">Hi, Han!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/Han.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0], PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Jhow.
        elif pVal == 1:
            string = "Jhow\n\n" + probs[0][0] + '\n\n' + probs[0][1]
            self.model_user2.set_label(string)
            self.result_label.set_markup('<span size="100000">Hi, Jhow!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/jhow.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0], PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Rick.
        elif pVal == 2:
            self.result_label.set_markup('<span size="100000">Hi, Jing!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/jing.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0], PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is Yo.
        elif pVal == 3:
            self.result_label.set_markup('<span size="100000">Hi, Rick!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/rick.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0],PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)

        #Prediction result is intruder.
        elif pVal == -1:
            self.result_label.set_markup('<span size="100000" color="red">Intruder!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("src/intruder.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(PictureSize[0],PictureSize[1],gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            self.image_result_picture.set_from_pixbuf(scaled_result_picture)
        self.window.show_all()
        return True

    def main(self):
        gtk.main()



def Setup(pVal, probs):
    base = Base(pVal, probs)
    base.main()
