import sys
import pygtk
pygtk.require('2.0')
import gtk
from Demo import *

class Base:
    def __init__(self, filename1,filename2,filename3,filename4,filename5):

        [modelPool, p_tabel, dataPool, trainingLabel, scaleRange, scaleMin] = Run([filename1,filename2,filename3,filename4], filename5)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(640, 480)
        self.window.connect("delete_event", gtk.main_quit)

        

        self.hbox_start = gtk.HBox()
        self.hbox_welcome = gtk.HBox()
        self.hbox_result = gtk.HBox()
        self.hbox_origin = gtk.HBox(spacing = 3)
        self.vbox_whole = gtk.VBox(spacing = 3)

        self.start_button = gtk.Button()
        #self.start_button.connect("clicked", self.detect(p_tabel), None)
        self.start_button.connect("clicked", self.receiving(modelPool, p_tabel, dataPool, trainingLabel, scaleRange, scaleMin), "start")
        self.hbox_start.add(self.start_button)

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

        string = "Jhow\n3.4%"
        self.model_user1.set_label(string)
        self.hbox_origin.add(self.model_user1)


        string = "Han\n98.7%"
        self.model_user2.set_label(string)  
        self.hbox_origin.add(self.model_user2)

        string = "Rick\n10.9%"
        self.model_user3.set_label(string)  
        self.hbox_origin.add(self.model_user3)

        string = "Yo\n9.7%"
        self.model_user4.set_label(string)  
        self.hbox_origin.add(self.model_user4)

   

        #Welcome String
        self.welcome_label = gtk.Label()
        self.welcome_label.set_use_markup(gtk.TRUE)
        self.welcome_label.set_markup('<span size="25000">Welcome to Intel Smart House!!</span>')
        self.hbox_welcome.add(self.welcome_label)
        
        #Result
        self.result_label = gtk.Label()
        self.result_label.set_use_markup(gtk.TRUE)
        self.result_label.set_markup('<span size="20000">Who are you?</span>')
        self.hbox_result.add(self.result_label)
        
        #Initial picture
    
        #Read Image
        result_picture = gtk.gdk.pixbuf_new_from_file("Demo/ques.jpg")
        #Resize Image
        scaled_result_picture = result_picture.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
        #Set Image on Window
        image_result_picture = gtk.Image()
        image_result_picture.set_from_pixbuf(scaled_result_picture)

        self.hbox_result.add(image_result_picture)
        #Add to hbox 

        

        self.vbox_whole.add(self.hbox_start)    
        self.vbox_whole.add(self.hbox_welcome)
        self.vbox_whole.add(self.hbox_result)
        self.vbox_whole.add(self.hbox_origin)
        self.window.add(self.vbox_whole)  
        self.window.show_all()
        #self.start_button.connect("clicked", gtk.Widget.destroy, "start")
        print "stop here"
    
    
    
    def receiving(self, modelPool, p_tabel, dataPool, trainingLabel, scaleRange, scaleMin):
        pVal = Ready(modelPool, p_tabel, dataPool, trainingLabel, scaleRange, scaleMin)
                #Prediction result is Han.
        if pVal == 0:
            self.result_label.set_markup('<span size="20000">Hi, Han!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("Demo/Han.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            image_result_picture.set_from_pixbuf(scaled_result_picture)
            #Add to hbox
            

        #Prediction result is Jhow.
        elif pVal == 1:
            self.result_label.set_markup('<span size="20000">Hi, Jhow!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("Demo/jhow.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            image_result_picture.set_from_pixbuf(scaled_result_picture)
            #Add to hbox
            

        #Prediction result is Rick.
        elif pVal == 2:
            self.result_label.set_markup('<span size="20000">Hi, Jing!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("Demo/jing.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            image_result_picture.set_from_pixbuf(scaled_result_picture)
            #Add to hbox
            

        #Prediction result is Yo.
        elif pVal == 3:
            self.result_label.set_markup('<span size="20000">Hi, Rick!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("Demo/rick.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            image_result_picture.set_from_pixbuf(scaled_result_picture)
            #Add to hbox
           

        #Prediction result is intruder.
        elif pVal == -1:
            self.result_label.set_markup('<span size="20000">Intruder!</span>')
            #Read Image
            result_picture = gtk.gdk.pixbuf_new_from_file("Demo/intruder.jpg")
            #Resize Image
            scaled_result_picture = result_picture.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
            #Set Image on Window
            image_result_picture.set_from_pixbuf(scaled_result_picture)
            #Add to hbox
      
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
    base.main()