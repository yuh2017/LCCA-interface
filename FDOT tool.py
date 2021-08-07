from tkinter import *
from numpy import *
import numpy.core._methods
import numpy.lib.format
import pandas
numpy.set_printoptions(precision=4,suppress=True)
import tkinter.scrolledtext as tkst
from tkinter.ttk import *
from tkinter import filedialog
from tabulate import tabulate
from dbfread import DBF
from pandas import DataFrame
from tkinter.messagebox import showinfo

LARGE_FONT = ("Arial", 12,"bold")
COOL_FOTN = ("Arial",15,"bold italic")
INSTRUCT_FONT =("Arial",8,"bold")
Med_font= ("Verdana",10)
small_font=("Verdana",10)
appversion='2.091117'
class FDOTTOOL(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.app_data   = {"ananame": StringVar(),"anadate": StringVar(),"projectdes":StringVar(),"convhtbase":DoubleVar(),"contvhtbui":DoubleVar(),
                         "flvhtbase":DoubleVar(),"flvhtbui":DoubleVar(),"forcastyears":DoubleVar(),"npvvalue":DoubleVar(),"vottvalue":DoubleVar(),"projectcost":DoubleVar()}
        Tk.wm_title(self, "Florida FEIM")
        self.LCAResults = {}
        container       = Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar         = Menu(container)
        filemenu        = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Exit", command=sys.exit)


        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=filemenu)
        filemenu.add_command(label="Manual", command=self.softwaremanual)
        filemenu.add_command(label="Version", command=self.aboutinformation)
        Tk.config(self, menu=menubar)
        self.frames = {}

        for F in (StartPage,PageZero, PageOne, PageTwo,PageTwoONE, 
                  PageThree, StartPage2, NewPage2, LCCAResults1, LCCAResults2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            page_name = F.__name__
            self.frames[page_name] = frame

        self.show_frame(StartPage)

    def show_frame(self, cont, arg=None):
        frame = self.frames[cont]
        frame.tkraise()
        if arg:
            frame.arg = arg
            frame.some_function(arg)
    
    def softwaremanual(self):
        toplevel = Toplevel()
        toplevel.title('Manual')
        toplevel.focus_set()
        manualsf = tkst.ScrolledText(toplevel, width=30, height=10)
        manuals ='this part is still underdevelpement'
        manualsf.insert(END, manuals)
        manualsf.pack()
    def aboutinformation(self):
        toplevel = Toplevel()
        toplevel.geometry('500x500')
        toplevel.title('Version Information')
        toplevel.focus_set()
        aboutinformatinon1 = Label(toplevel, text='\nSoftware Version',font=LARGE_FONT)
        aboutinformatinon1.pack(side=TOP,anchor=N)
        aboutinformatinon1 = Label(toplevel, text=appversion,font=small_font)
        aboutinformatinon1.pack(side=TOP,anchor=N)
        aboutinformatinon1=Label(toplevel,text='\nProject Manger(UF)',font=LARGE_FONT)
        aboutinformatinon1.pack(side=TOP,anchor=N)
        aboutinformatinon1=Label(toplevel,text='Zhong-Ren Peng',font=small_font)
        aboutinformatinon1.pack(side=TOP,anchor=N)
        aboutinformatinon1=Label(toplevel,text='\nProject Manger(FDOT)',font=LARGE_FONT)
        aboutinformatinon1.pack(side=TOP,anchor=N)
        aboutinformatinon1=Label(toplevel,text='Frank',font=small_font)
        aboutinformatinon1.pack(side=TOP,anchor=N)
        aboutinformatinon1=Label(toplevel,text='\nLead Researcher and Software Developer',font=LARGE_FONT)
        aboutinformatinon1.pack(side=TOP,anchor=N)
        aboutinformatinon1=Label(toplevel,text='Haitao YU\n',font=small_font)
        aboutinformatinon1.pack(side=TOP,anchor=N)


        manualsf = tkst.ScrolledText(toplevel, width=50, height=10,font=small_font)
        manuals ="© 2017 University of Florida\nFlorida Department of Transportation. \nAll rights reserved."
        manualsf.insert(END, manuals)
        manualsf.pack(side=TOP,anchor=N)

    def get_page(self, page_name):
        return self.frames[page_name]

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Florida Freight Economic Impact Model Tool", font=COOL_FOTN)
        label.pack(side=TOP,anchor=N,pady=10, padx=10)
        label2 = Label(self,
                      text='Florida FEIM'+'\n'+'V.'+appversion,
                      font=COOL_FOTN,justify=CENTER)
        label2.pack(side=TOP, anchor=N, pady=10, padx=10)
        button = Button(self, text="New Project",
                           command=lambda: controller.show_frame(PageZero))
        button.pack()

class PageZero(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        frameintro = Frame(self)
        frameintro.pack(side=TOP, anchor=N, padx=10, pady=10)
        label = Label(frameintro, text="Project Properties", font=LARGE_FONT)
        label.pack(side=TOP,anchor=N,padx=10)


        framereport = Frame(self)
        framereport.pack(side=TOP, anchor=CENTER)
        Labeldate = Label(framereport, text="ANALYSIS DATE",font=INSTRUCT_FONT)
        Labeldate.pack(side=TOP, expand=True, anchor=CENTER)
        self.some_entry2 = Entry(framereport, textvariable=self.controller.app_data["anadate"])
        self.some_entry2.pack(side=TOP)

        Labelname = Label(framereport, text="NAME",font=INSTRUCT_FONT)
        Labelname.pack(side=TOP, expand=True, anchor=CENTER)
        self.some_entry1 = Entry(framereport,textvariable=self.controller.app_data["ananame"])
        self.some_entry1.pack(side=TOP)

        Labelname = Label(framereport, text="Project Description",font=INSTRUCT_FONT)
        Labelname.pack(side=TOP, expand=True, anchor=CENTER)
        self.some_entry4 = Text(framereport, height=20, width=40)
        self.some_entry4.pack(side=TOP)
        button2 = Button(framereport, text="Back", command=lambda: controller.show_frame(StartPage))
        button2.pack(anchor=CENTER)
        button1 = Button(framereport, text="Next", command=lambda: controller.show_frame(PageOne))
        button1.pack(side=TOP, expand=True, anchor=N)



class PageOne(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        frameintro2 = Frame(self)
        frameintro2.pack(side=TOP, anchor=N, padx=10, pady=10)
        labe2 = Label(frameintro2, text="Project Information", font=LARGE_FONT)
        labe2.pack(side=TOP,anchor=N,padx=10)


        framestudyarea = Frame(self)
        framestudyarea.pack(side=TOP, fill=X, anchor=CENTER, pady=10)
        self.tkvar = StringVar()
        choices = {'','Florida','Alachua', 'Baker', 'Bay', 'Bradford', 'Brevard', 'Broward', 'Calhoun', 'Charlotte', 'Citrus',
                   'Clay', 'Collier', 'Columbia', 'DeSoto', 'Dixie', 'Duval', 'Escambia', 'Flagler', 'Franklin',
                   'Gadsden', 'Gilchrist', 'Glades', 'Gulf', 'Hamilton', 'Hardee', 'Hendry', 'Hernando', 'Highlands',
                   'Hillsborough', 'Holmes', 'Indian River', 'Jackson', 'Jefferson', 'Lafayette', 'Lake', 'Lee', 'Leon',
                   'Levy', 'Liberty', 'Madison', 'Manatee', 'Marion', 'Martin', 'Miami-Dade', 'Monroe', 'Nassau',
                   'Okaloosa', 'Okeechobee', 'Orange', 'Osceola', 'Palm Beach', 'Pasco', 'Pinellas', 'Polk', 'Putnam',
                   'Santa Rosa', 'Sarasota', 'Seminole', 'St.Johns', 'St.Lucie', 'Sumter', 'Suwannee', 'Taylor',
                   'Union', 'Volusia', 'Wakulla', 'Walton', 'Washington'}
        
        self.tkvar.set('Florida Counties')
        Label(framestudyarea, text="Choose Study County",font=INSTRUCT_FONT).pack(side=TOP, expand=True, anchor=CENTER, padx=15)

        self.studycounty= OptionMenu(framestudyarea, self.tkvar, *sorted(choices))# this creates sorted order
        self.studycounty.pack(side=TOP, expand=True,anchor=CENTER)



        self.tkvar2 = StringVar()
        choices2 = {'', '2020', '2025', '2030','2035','2040','2045', '2050'}
        self.tkvar2.set('Year')
        Label(framestudyarea, text="Choose forecasting year", font=INSTRUCT_FONT).pack(side=TOP, expand=True, anchor=CENTER,
                                                                                   padx=15)
        # 2010 +5 2040
        self.forecaseyears = OptionMenu(framestudyarea, self.tkvar2, *sorted(choices2))  # this creates sorted order
        self.forecaseyears.pack(side=TOP, expand=True, anchor=CENTER)



        LabelVOTT1 = Label(framestudyarea, text="Value of Travel Time", font=INSTRUCT_FONT)
        LabelVOTT1.pack(side=TOP, expand=TRUE, anchor=N)
        self.some_entry2 = Entry(framestudyarea, textvariable=self.controller.app_data["vottvalue"])
        self.some_entry2.pack(side=TOP)

        LabelVOTT2 = Label(framestudyarea, text="Net Present Value (NPV)", font=INSTRUCT_FONT)
        LabelVOTT2.pack(side=TOP, expand=TRUE, anchor=N)
        self.some_entry3 = Entry(framestudyarea, textvariable=self.controller.app_data["npvvalue"])
        self.some_entry3.pack(side=TOP)

##        LabelVOTT = Label(framestudyarea, text="Project Cost *Optional", font=INSTRUCT_FONT)
##        LabelVOTT.pack(side=TOP, expand=TRUE, anchor=N)
##        self.some_entry3 = Entry(framestudyarea, textvariable=self.controller.app_data["projectcost"])
##        self.some_entry3.pack(side=TOP)

##        self.tkvar3 = StringVar()
##        choices3 = {'','Yes', 'No'}
##        self.tkvar3.set('Consider Costs')
##        self.studycounty= OptionMenu(framestudyarea, self.tkvar3,*choices3)# this creates sorted order
##        self.studycounty.pack(side=TOP, expand=True,anchor=CENTER)


        button2 = Button(framestudyarea, text="Back",command=lambda: controller.show_frame(PageZero))
        button2.pack(anchor=CENTER)
        button1 = Button(framestudyarea, text="Next",command=lambda: controller.show_frame(PageTwo))
        button1.pack(anchor=CENTER)
        button3 = Button(framestudyarea, text="Help",command=self.myhelp)
        button3.pack(anchor=CENTER)

    def myhelp(self):

        showinfo('Help','Attention: Only recommended values. Value might be different by projects.\nProject net present value is usualy set as 0.04.\nValue of travel time is usually 40-60$/hour.\nForecasting year should be the same with the one used in FreightSIM for scenarios.')

class PageTwo(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        frameintro3 = Frame(self)
        frameintro3.pack(side=TOP, anchor=N, padx=10, pady=10)
        label3 = Label(frameintro3, text="Scenario Input", font=LARGE_FONT)
        label3.pack(side=TOP, anchor=N, padx=10)
        label1 = Label(frameintro3, text="Built VHT analysis", font=LARGE_FONT)
        label1.pack(pady=10, padx=10)

        self.button = Button(frameintro3, text="Browse for VHT link files", command=self.load_file)
        self.button.pack()
        label5 = Label(frameintro3, text="Built Scenario VHT", font=LARGE_FONT)
        label5.pack(side=TOP, anchor=N, pady=10, padx=10)
        self.texin1 = Text(frameintro3, width=20, height=2)
        self.texin1.pack(side=TOP)
        label4 = Label(frameintro3, text="Calculation status", font=LARGE_FONT)
        label4.pack(side=TOP, anchor=N, pady=10,padx=10)
        self.texin2 = Text(frameintro3, width=20, height=1)
        self.texin2.pack(side=TOP)
        
        button2 = Button(frameintro3, text="Back",command=lambda: controller.show_frame(PageOne))
        button2.pack(anchor=CENTER)
        button1 = Button(frameintro3, text="Next",command=lambda: controller.show_frame(PageTwoONE))
        button1.pack(anchor=CENTER)
        button3 = Button(frameintro3, text="Help", command=self.myhelp)
        button3.pack(anchor=CENTER)

    def myhelp(self):
        showinfo('Help',
                 'Please locate to link.dbf files from FreightSIM output.This file can be found from scenario output folder after running scenarios from FreightSIM.\nThe calculation process will be approximately 2-3 minutes.\nPlease wait for a pop-up window which confirms VHT analysis is finished.')

    def load_file(self):
        self.fname = filedialog.askopenfilename(filetypes=(("Link File", "*.dbf"), ("All files", "*.*")))
        showinfo('Progress', 'Please wait for VHT calculation...')
        if self.fname:
            dbf = DBF(self.fname, load=False, encoding='iso-8859-1')
            frame = DataFrame(iter(dbf))
            studyarea = self.controller.get_page("PageOne")
            studycounty2 = studyarea.tkvar.get()
            row = studycounty2
            
            self.builtLength = frame['LANEMILES'].astype(double).sum()
            
            frame['TOTAL_VEH'] = frame['TOTAL_VEH'].astype(int)
            frame['vehtr'] = frame['TRUCK_VOL'] * frame['CGTIME'] * .016667
            if studycounty2=='Florida':
                self.vhttr = frame['vehtr'].sum()
                self.vhtstudy = self.vhttr
                roundnumber = round(self.vhtstudy, 2)
            else:
                self.vhttr = frame.groupby('COUNTY')['vehtr'].sum()[row]
                self.vhtstudy = self.vhttr
                roundnumber=round(self.vhtstudy,2)
            self.texin1.delete("1.0", END)
            self.texin1.insert(END, roundnumber)
            self.texin1.see(END)
            instruction='Please proceed...'
            self.texin2.delete("1.0", END)
            self.texin2.insert(END, instruction)
            self.texin2.see(END)
            self.builtvht = self.vhtstudy
            showinfo("Status", "Please proceed.")
            print(self.builtvht)

class PageTwoONE(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        frameintro3 = Frame(self)
        frameintro3.pack(side=TOP, anchor=N, padx=10, pady=10)
        label3 = Label(frameintro3, text="Scenario Input", font=LARGE_FONT)
        label3.pack(side=TOP, anchor=N, padx=10)

        label2 = Label(frameintro3, text="No-Built VHT analysis", font=LARGE_FONT)
        label2.pack(pady=10, padx=10)

        self.button2 = Button(frameintro3, text="Browse for VHT link files", command=self.load_file)
        self.button2.pack()
        label5 = Label(frameintro3, text="No-Built Scenario VHT", font=LARGE_FONT)
        label5.pack(side=TOP, anchor=N, pady=10,padx=10)
        self.texin22 = Text(frameintro3, width=20, height=2)
        self.texin22.pack(side=TOP)
        label4 = Label(frameintro3, text="Calculation status", font=LARGE_FONT)
        label4.pack(side=TOP, anchor=N, pady=10,padx=10)
        self.texin2 = Text(frameintro3, width=20, height=1)
        self.texin2.pack(side=TOP)

        button2 = Button(frameintro3, text="Back",command=lambda: controller.show_frame( PageTwo ))
        button2.pack(anchor=CENTER)
        button1 = Button(frameintro3, text="Next",command=lambda: controller.show_frame( StartPage2 ))
        button1.pack(anchor=CENTER)
        button3 = Button(frameintro3, text="Help", command=self.myhelp)
        button3.pack(anchor=CENTER)

    def myhelp(self):
        showinfo('Help',
                 'Please locate to link.dbf files from FreightSIM output.This file can be found from scenario output folder after running scenarios from FreightSIM.\nThe calculation process will be approximately 2-3 minutes.\nPlease wait for a pop-up window which confirms VHT analysis is finished.')

    def load_file(self):
        self.fname2 = filedialog.askopenfilename(filetypes=(("Link File", "*.dbf"), ("All files", "*.*")))
        showinfo('Progress', 'Please wait for VHT calculation...')
        if self.fname2:
            dbf2 = DBF(self.fname2, load=False, encoding='iso-8859-1')
            frame2 = DataFrame(iter(dbf2))
            studyarea = self.controller.get_page("PageOne")
            studycounty2 = studyarea.tkvar.get()
            row = studycounty2
            
            self.nonbuiltLength = frame2['LANEMILES'].astype(double).sum()
            
            frame2['TOTAL_VEH'] = frame2['TOTAL_VEH'].astype(int)
            frame2['vehtr'] = frame2['TRUCK_VOL'] * frame2['CGTIME'] *0.016667
            if studycounty2=='Florida':
                self.vhttr2 = frame2['vehtr'].sum()
                self.vhtstudy2 = self.vhttr2
                roundnumber2 = round(self.vhtstudy2, 2)
            else:
                self.vhttr2 = frame2.groupby('COUNTY')['vehtr'].sum()[row]
                self.vhtstudy2 = self.vhttr2
                roundnumber2=round(self.vhtstudy2,2)

            self.texin22.delete("1.0", END)
            self.texin22.insert(END, roundnumber2)
            self.texin22.see(END)

            instruction='Please proceed...'
            self.texin2.delete("1.0", END)
            self.texin2.insert(END, instruction)
            self.texin2.see(END)
            showinfo("Status", "Please proceed.")
            self.nonbuiltvht = self.vhtstudy2
            print( self.nonbuiltvht )





class StartPage2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label  = Label(self, text="Florida Freight Transportation Project" + "\n" +"Life Cycle Analysis", 
                      font=COOL_FOTN, justify = CENTER )
        label.pack(side=TOP,anchor=N,pady=10, padx=10)
        label2 = Label(self,
                      text='Florida FEIM'+'\n'+'V.'+ appversion,
                      font=Med_font,justify = CENTER)
        label2.pack(side=TOP, anchor=N, pady=10, padx=10)
        button = Button(self, text="Start",
                           command= lambda: controller.show_frame(NewPage2) )
        button.pack(anchor=CENTER)
        
        BackButton =  Button(self, text="Back",
                            command= (lambda: controller.show_frame(PageTwoONE) ) )
        BackButton.pack(anchor=CENTER)

class NewPage2(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.results = {}
        frame1 = Frame(self)
        frame1.pack(side=TOP, anchor=N, padx=10, pady=10)
        label = Label(frame1, text="Life cycle cost and benefit analysis", 
                      font=LARGE_FONT, justify = CENTER)
        label.pack(side=TOP,anchor=N,padx=10)
        
        label = Label(frame1, text="Inputs", 
                      font= Med_font, justify = CENTER)
        label.pack(side=TOP,anchor=N,padx=10)
        
        fields = ( 'Construction Cost per mile',
                   'Maintence Cost per mile', 
                   'Rehabilitation Cost per mile', 
                   'Rehabilitation Year Length(0-35)',
                   'Maintenance Cost Growth Rate', 
                   'Annual VHT Growth Rate')
        self.entries = {}
        for field in fields:
            row = Frame(self)
            lab = Label(row, width= 35, text=field+": ", anchor='w')
            ent = Entry(row)
            ent.insert(0, "0.0")
            row.pack(side=TOP, 
                     fill= X, padx= 5, pady= 5)
            lab.pack(side = LEFT,  expand = YES) #
            ent.pack(side = RIGHT, expand = YES, fill= X) #
            self.entries[field] = ent
        
        
        BackButton = Button(self, text="Back",
                            command=(lambda: controller.show_frame(StartPage2)) )
        BackButton.pack(anchor=CENTER)   
        nextButton = Button(self, text="Next",command=(lambda: controller.show_frame( LCCAResults1 ) ))
        nextButton.pack(anchor=CENTER)
     
        
        # changing the title of our master widget 
        
class LCCAResults1(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        frame1 = Frame(self)
        frame1.pack(side=TOP, anchor=N, padx=10, pady=10)
        label = Label(frame1, text="LCCA Results" + "\n" +"Unit: thousand dollars($)", 
                      font=LARGE_FONT, justify = CENTER)
        label.pack(side=TOP,anchor=N,padx=10)
        
        
        ents_results = [ 'Construction Cost',  'Maintenance Cost' , 
                        'Rehabilitation Cost' , 'Salvage value' , 'User Benefit' ]
        self.entries2 = {}
        fid = 0
        for field in ents_results:
            row = Frame(self)
            lab = Label(row, width= 35, text=field+": ", anchor='w')
            ent = Entry(row)
            ent.insert(0, 0.0)
            row.pack(side=TOP, 
                     fill= X, padx= 5, pady= 5)
            lab.pack(side = LEFT,  expand = YES) #
            ent.pack(side = RIGHT, expand = YES, fill= X) #
            self.entries2[field] = ent
            fid = fid + 1
            
        BackButton =  Button(self, text="Back",
                            command= (lambda: controller.show_frame(NewPage2) ) )
        BackButton.pack(anchor=CENTER)
         
        CalButton =  Button(self, text="Calculate",
                            command= (lambda: self.GetPageData(NewPage2)) )
        CalButton.pack(anchor=CENTER)
        
        NextButton =  Button(self, text="Next",
                            command= (lambda: controller.show_frame(LCCAResults2)) )
        NextButton.pack(anchor=CENTER)
        
        
    def CalculateSA(self, entries, entries_now):
#        RdLength = float(str(entries['Road Length(miles*)'].get()).replace(",", "")) 
#        print(NLanes, RdLength)
        ##########################################################
        if float(str(entries['Construction Cost per mile'].get()).replace(",", "")) <= 0:
            CostPerMile  = 1053537
        else:
            CostPerMile  = float(str(entries['Construction Cost per mile'].get()).replace(",", "")) 
        
        if float(str(entries['Maintenance Cost Growth Rate'].get())) <= 0.0:
            MaintGR  = 0.02
        else:
            MaintGR  = float(str(entries['Maintenance Cost Growth Rate'].get()).replace(",", "")) 
        
        if float(str(entries['Annual VHT Growth Rate'].get())) <= 0.0:
            VHTGrowthR  = 0.02
        else:
            VHTGrowthR  = float(str(entries['Annual VHT Growth Rate'].get()).replace(",", "")) 
        
        if float(str(entries['Rehabilitation Year Length(0-35)'].get())) <= 0.0:
            RehabLength  = 9
        else:
            RehabLength = float(str(entries['Rehabilitation Year Length(0-35)'].get()).replace(",", ""))
            RehabLength = int( RehabLength )
        
        
        vhtresutls= self.controller.get_page("PageTwo")
        convhtbase2 = vhtresutls.builtvht
        vhtresutls2 = self.controller.get_page("PageTwoONE")
        contvhtbui2 = vhtresutls2.nonbuiltvht
        
        
        RdLength = numpy.abs( vhtresutls.builtLength - vhtresutls2.nonbuiltLength )
        
        VHT  = numpy.abs( convhtbase2 - contvhtbui2 )
        
        infR        = 0.02
        studyarea   = self.controller.get_page("PageOne")
        predictyear = studyarea.tkvar2.get()
        NLC         = int(predictyear) - 2015
        
        nYrs = NLC % RehabLength
        #################################################
        
        MOT              = 0.1 * CostPerMile 
        Mobilization     = 0.1 * ( CostPerMile + MOT)
        SubConstruct     = MOT + Mobilization + CostPerMile
        ScopeContingency = 0.25 * SubConstruct
        CEI              = 0.15 * ( SubConstruct + ScopeContingency)
        LRP              = 0.25 * SubConstruct
        TotConstruct     = SubConstruct + ScopeContingency + CEI + LRP
        Design           = 0.15 * TotConstruct 
        
        ####################################### 
        initialC = (TotConstruct + Design) * RdLength
        
        if float(str(entries['Maintence Cost per mile'].get())) <= 0.0:
            MaintenceCost  = 0.00004*initialC
        else:
            MaintenceCost  = float(str(entries['Maintence Cost per mile'].get()).replace(",", "")) 
            
        if float(str(entries['Rehabilitation Cost per mile'].get())) <= 0.0:
            RehabCost  = 0.0008*initialC
        else:
            RehabCost  = float(str(entries['Rehabilitation Cost per mile'].get()).replace(",", ""))    
        
        rehabC      = 0
        operateC    = 0
        disRi       = float(studyarea.some_entry3.get())
        
        RnYrs    =  nYrs
        salvage  =  initialC *nYrs/NLC * ( (1+infR) ** RnYrs ) / ( (1+disRi) ** RnYrs )
        for yi in range(NLC):
            if (yi+1) % RehabLength == 0:
                rehabC =  rehabC +  RehabCost *( (1+MaintGR) ** yi )* RdLength* ( (1+infR) ** yi ) / ( (1+disRi) ** yi )
            operateC   = operateC +  MaintenceCost * RdLength*( (1+MaintGR) ** yi )* ( (1+infR) ** yi ) / ( (1+disRi) ** yi )
        ##########################################################
        initialC1       =  ("%8.0f" % (initialC / 1000) ).strip()
        rehabC1         = ("%8.0f" % (rehabC/ 1000) ).strip()
        operateC1       = ("%8.0f" % (operateC/ 1000) ).strip()
        salvage1        = ("%8.0f" % (salvage/ 1000) ).strip()
        ##########################################################
        ################################################# 
        GasPrice = 2.49 
        DriverWage = 27.5
        hourCost   = float(studyarea.some_entry2.get())

        #GasPrice*0.156*70 + DriverWage
        #################################################
        CumBenefit = 0
        for yi in range(NLC):
            CumBenefit = CumBenefit +  VHT*hourCost * 365 * ((1+VHTGrowthR)**yi) * ( (1+infR) ** yi ) / ( (1+disRi) ** yi )
        Total_User_Cost    = CumBenefit
        Total_User_Cost1 = ("%8.0f" % ( Total_User_Cost/ 1000) ).strip()
#        print( initialC, rehabC, operateC, salvage, Total_User_Cost)
        
        entries_now['Construction Cost'].delete(0, END)
        entries_now['Construction Cost'].insert(0, initialC1 )
            
        entries_now['Rehabilitation Cost'].delete(0, END)
        entries_now['Rehabilitation Cost'].insert(0, rehabC1 )
        #################################################
        entries_now['Maintenance Cost'].delete(0, END)
        entries_now['Maintenance Cost'].insert(0, operateC1 )
        #################################################
        entries_now['Salvage value'].delete(0, END)
        entries_now['Salvage value'].insert(0, salvage1 )
        #################################################
        entries_now['User Benefit'].delete(0, END)
        entries_now['User Benefit'].insert(0, Total_User_Cost1 )
        
        
        
    def GetPageData(self, Pagei):
        NewPage2_data = self.controller.get_page(Pagei)
        entries  = NewPage2_data.entries 
#        results  = NewPage2_data.TotalCosts( entries )
        self.CalculateSA(entries, self.entries2)
        
class LCCAResults2(Frame):
    def __init__(self, parent, controller):
        discountFactors = [0.1, 0.2, 0.3, 0.4, 0.5]
        Frame.__init__(self, parent)
        self.controller = controller
        frame1 = Frame(self)
        frame1.pack(side=TOP, anchor=N, padx=10, pady=10)
        label = Label(frame1, text="Life-Cycle Cost Sensitivity Analysis" + "\n" +"Unit: thousand dollars($)", 
                      font=LARGE_FONT, justify = CENTER)
        label.pack(side=TOP,anchor=N,padx=10)
        
        
        self.tv= Treeview(frame1)
        self.tv.pack(pady=10, padx=10)
        
#        self.vsb = Scrollbar(frame1, orient="vertical",
#                            command=self.tv.yview)
#        self.vsb.pack(side= RIGHT, fill= Y)
#        
#        self.hsb = Scrollbar(frame1, orient="horizontal",
#                            command=self.tv.xview)
#        self.hsb.pack(side='bottom', fill='x')
#
#        self.tv.configure(yscrollcommand= self.vsb.set, xscrollcommand= self.hsb.set)
        
        
        
        self.tv['columns'] = ('Column0', 'Column1', 'Column2','Column3', 'Column4', 'Column5')
        self.tv.heading('#0', text='Activity')
        self.tv.column('#0', anchor='center', width= 150)
        
        self.tv.heading('Column0', text='Year')
        self.tv.column('Column0', anchor='center', width= 100)               
        
        self.tv.heading('Column1', text='DF 1%')
        self.tv.column('Column1', anchor='center', width= 100)
        
        self.tv.heading('Column2', text='DF 2%')
        self.tv.column('Column2', anchor='center', width= 100)               
        self.tv.heading('Column3', text='DF 3%')
        self.tv.column('Column3', anchor='center', width= 100)
        self.tv.heading('Column4', text='DF 4%')
        self.tv.column('Column4', anchor='center', width= 100)
        self.tv.heading('Column5', text='DF 5%')
        self.tv.column('Column5', anchor='center', width= 100)
        self.treeview = self.tv
        
        ents_results = [ 'Construction Cost',  'Maintenance Cost' , 
                        'Rehabilitation Cost' , 'Salvage value' , 'User Benefit' ]
        self.entries2 = {}
            
        BackButton =  Button(self, text="Back",
                            command= (lambda: controller.show_frame(LCCAResults1) ) )
        BackButton.pack(anchor=CENTER)
         
        CalButton =  Button(self, text="Calculate",
                            command= (lambda: self.calculation(discountFactors)) )
        CalButton.pack(anchor=CENTER)

        NextButton =  Button(self, text="Next",
                            command= (  lambda: controller.show_frame( PageThree ))  ) 
        NextButton.pack(anchor=CENTER)
        
    def ShowSA(self, entries, discountFactors):
        discountFactors = [0.01, 0.02, 0.03, 0.04, 0.05]
#        print(NLanes, RdLength)
        ##########################################################
        if float(str(entries['Construction Cost per mile'].get()).replace(",", "")) <= 0:
            CostPerMile  = 1053537
        else:
            CostPerMile  = float(str(entries['Construction Cost per mile'].get()).replace(",", "")) 
        
        if float(str(entries['Maintenance Cost Growth Rate'].get())) <= 0.0:
            MaintGR  = 0.02
        else:
            MaintGR  = float(str(entries['Maintenance Cost Growth Rate'].get()).replace(",", "")) 
        
        
        if float(str(entries['Annual VHT Growth Rate'].get())) <= 0.0:
            VHTGrowthR  = 0.02
        else:
            VHTGrowthR  = float(str(entries['Annual VHT Growth Rate'].get()).replace(",", "")) 
        
        if float(str(entries['Rehabilitation Year Length(0-35)'].get())) <= 0.0:
            RehabLength  = 9
        else:
            RehabLength = float(str(entries['Rehabilitation Year Length(0-35)'].get()).replace(",", ""))
            RehabLength = int( RehabLength )
        
        vhtresutls= self.controller.get_page("PageTwo")
        convhtbase2 = vhtresutls.builtvht
        vhtresutls2 = self.controller.get_page("PageTwoONE")
        contvhtbui2 = vhtresutls2.nonbuiltvht
        
        RdLength = numpy.abs( vhtresutls.builtLength - vhtresutls2.nonbuiltLength )
        
        VHT  = numpy.abs( convhtbase2 - contvhtbui2 )
        
        infR        = 0.02
        studyarea   = self.controller.get_page("PageOne")
        predictyear = studyarea.tkvar2.get()
        NLC         = int(predictyear) - 2015
        nYrs = NLC % RehabLength
        print( "##############################" )
        print(RdLength, "#### ",VHT, "#### ", NLC, "### ", nYrs)
        
        MOT              = 0.1 * CostPerMile 
        Mobilization     = 0.1 * ( CostPerMile + MOT)
        SubConstruct     = MOT + Mobilization + CostPerMile
        ScopeContingency = 0.25 * SubConstruct
        CEI              = 0.15 * ( SubConstruct + ScopeContingency)
        LRP              = 0.25 * SubConstruct
        TotConstruct     = SubConstruct + ScopeContingency + CEI + LRP
        Design           = 0.15 * TotConstruct 
        
        ####################################### 
        initialC = (TotConstruct + Design) * RdLength
        
        if float(str(entries['Maintence Cost per mile'].get())) <= 0.0:
            MaintenceCost  = 0.00004*initialC
        else:
            MaintenceCost  = float(str(entries['Maintence Cost per mile'].get()).replace(",", "")) 
            
        if float(str(entries['Rehabilitation Cost per mile'].get())) <= 0.0:
            RehabCost  = 0.0008*initialC
        else:
            RehabCost  = float(str(entries['Rehabilitation Cost per mile'].get()).replace(",", ""))     
        
        rehabC   = 0
        operateC = 0

#        disRi       = float(studyarea.LabelVOTT.get() )
        RnYrs       =  nYrs   
        SlavageCost = [ 0.0 ] * ( len(discountFactors) )
        for Ri in range( len(discountFactors) ):
            disRi = discountFactors[Ri]
            SlavageCost[Ri] = initialC *nYrs/NLC * ( (1+infR) ** RnYrs ) / ( (1+disRi) ** RnYrs )   
        
        ##########################################################     =  
        GasPrice    = 2.49 
        DriverWage  = 27.5
        
        hourCost    = float(studyarea.some_entry2.get())
        ##########################################################
        ##########################################################
        ConstCmu = [ 0 ]
        
        for k in range(len(discountFactors)):
            ConstCmu.append( ("%8.0f" % (initialC/1000)).strip() )
        self.tv.insert('', 'end', text="Construction", values= ConstCmu)
        
        NameList = []
        head_strs = ["User Benefit #", "Maintenance Cost #", "Rehab #"]
        UserCostCmu     = [0] * (len(discountFactors ) + 1)
        RehabCosts      = [0] * (len(discountFactors ) + 1)
        MaintenanceCost = [0] * (len(discountFactors ) + 1)
        Salvagescosts   = [0] * (len(discountFactors ) + 1)
        kth_activity = 1
        for yi in range( NLC ):
            for Ri in range( len(discountFactors) ):
                idx = Ri + 1
                disRi = discountFactors[Ri]
                data_m =   MaintenceCost * RdLength*( (1+MaintGR) ** yi )* ( (1+infR) ** yi ) / ( (1+disRi) ** yi )
                MaintenanceCost[idx] = MaintenanceCost[idx] + (data_m/1000)
                
                data_u = VHT*hourCost * 365 * ((1+VHTGrowthR)**yi) * ( (1+infR) ** yi ) / ( (1+disRi) ** yi )
                UserCostCmu[idx] = UserCostCmu[idx] + (data_u/1000) 
                
                if (yi+1) % RehabLength == 0:
                    data_r = RehabCost *( (1+MaintGR) ** yi )* RdLength* ( (1+infR) ** yi ) / ( (1+disRi) ** yi )
                    RehabCosts[idx] =  (data_r/1000) 
                    NameList = [ head_stri +str(kth_activity) for head_stri in head_strs ]  
                    
            if (yi+1) % RehabLength == 0:
                data_item = [("%8.0f" % (uci)).strip() for uci in UserCostCmu ]
                data_item[0] = ("%8.0f" % (yi+1)).strip()
                self.tv.insert('', 'end', text= NameList[0], values= data_item)
                data_item = [("%8.0f" % (mci)).strip() for mci in MaintenanceCost ]
                data_item[0] = ("%8.0f" % (yi+1)).strip()
                self.tv.insert('', 'end', text= NameList[1], values= data_item)
                data_item = [("%8.0f" % (rci)).strip() for rci in RehabCosts ]
                data_item[0] = ("%8.0f" % (yi+1)).strip()
                self.tv.insert('', 'end', text= NameList[2], values= data_item)
                kth_activity = kth_activity + 1
                print(UserCostCmu)
                MaintenanceCost = [0] * ( len(discountFactors) + 1)
                UserCostCmu     = [0] * ( len(discountFactors) + 1)
                NameList        = []
        atYrs = NLC - nYrs
        Salvagescosts.append(atYrs)
        for Ri in range( len(discountFactors) ):
            idx = Ri + 1
            disRi = discountFactors[Ri]
            salvage = 0
            for ri in RnYrs:
                salvage  = initialC *nYrs/NLC * ( (1+infR) ** (atYrs+ri) ) / ( (1+disRi) ** (atYrs+ri) )
                Salvagescosts[idx] = salvage
        data_item = [("%8.0f" % (sali)).strip() for sali in Salvagescosts ]
        data_item[0] = ("%8.0f" % (atYrs)).strip()
        self.tv.insert('', 'end', text= 'Salvage value', values= data_item)
        
        
    def calculation(self, discountFactors):
        NewPage2_data = self.controller.get_page(NewPage2)
        entries  = NewPage2_data.entries 
        self.ShowSA(entries, discountFactors)  

########################################################


class PageThree(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        frame1 = Frame(self)
        frame1.pack(side=TOP, anchor=N, padx=10, pady=10)
        label = Label(frame1, text="Project Input", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        frame2 = Frame(self,width=50, height=10)
        frame2.pack(side=TOP,anchor=CENTER)
        self.texin1 = tkst.ScrolledText(frame2, width=35, height=5)
        self.texin1.pack(side=TOP)
        label2 = Label(frame2, text="Industry Impact Details", font=LARGE_FONT)
        label2.pack(pady=10, padx=10)
        self.tv=Treeview(frame2)
        self.tv.pack(pady=10, padx=10)
        self.tv['columns'] = ('economicoutput', 'economicemployment','economicincome')
        self.tv.heading('#0', text='Sector')
        self.tv.column('#0', anchor='center', width=50)
        self.tv.heading('economicoutput', text='Total Output')
        self.tv.column('economicoutput', anchor='center', width=80)
        self.tv.heading('economicemployment', text='Employment')
        self.tv.column('economicemployment', anchor='center', width=80)
        self.tv.heading('economicincome', text='Income')
        self.tv.column('economicincome', anchor='center', width=80)
        self.treeview = self.tv

#main calculation

        frame3 = Frame(self)
        frame3.pack(side=LEFT, fill=BOTH, expand=YES)
        label = Label(frame3, text="Results", font=LARGE_FONT)
        label.pack(pady=5, padx=10)
        button2 = Button(frame3, text='Analyze Input', command=self.print_it,width=15)
        button2.pack(side=TOP)
        button4 = Button(frame3, text='Industry Results', command=self.LoadTable,width=15)
        button4.pack(side=TOP)
        button3 = Button(frame3, text='Clear Results', command=self.clear_it,width=15)
        button3.pack(side=TOP)

        frame4 = Frame(self)
        frame4.pack(side=LEFT, fill=X, expand=YES)
        button5 = Button(frame4, text='Back', command=lambda: controller.show_frame(LCCAResults2))
        button5.pack(side=TOP)
        button6 = Button(frame4, text='Save Output', command=self.savefile)
        button6.pack(side=TOP)
        button7 = Button(frame4, text='Exit', command=lambda: controller.destroy())
        button7.pack(side=TOP)
        
        
    def print_it(self):
        # get values from the self.controller
        analystname = self.controller.app_data["ananame"].get()
        analystdate = self.controller.app_data["anadate"].get()
        vottvalue2 = self.controller.app_data["vottvalue"].get()
        vhtresutls= self.controller.get_page("PageTwo")
        convhtbase2 = vhtresutls.builtvht
        vhtresutls2 = self.controller.get_page("PageTwoONE")
        contvhtbui2 = vhtresutls2.nonbuiltvht

        npvv = self.controller.app_data["npvvalue"].get()
        # forecastyears2=self.controller.app_data["forcastyears"].get()
        projectcosts = self.controller.app_data["projectcost"].get()
        #get pages
        prodes = self.controller.get_page("PageZero")
        prodes2 = prodes.some_entry4.get("1.0", "end-1c")

        studyarea = self.controller.get_page("PageOne")
        studycounty2 = studyarea.tkvar.get()
                
        costornot= "NO" #studyarea.tkvar3.get()
        predictyear=studyarea.tkvar2.get()
        predictyear2=int(predictyear)
        # preidctyear2=predictyear3.get()

        #main calculation
        def my_range(startyear, endyear, stepyear):
            while startyear <= endyear:
                yield startyear
                startyear += stepyear

        #for the economic output
        IOop = "IO/" + studycounty2 + '.xlsx'
        IOop = pandas.read_excel(IOop)
        trIOop = "truckIO/" + studycounty2 + '.xlsx'
        trIOop = pandas.read_excel(trIOop)
        trIOop = trIOop.drop('rowcode', axis=1)
        empIO= "empIO/" + studycounty2 + '.xlsx'
        empIO = pandas.read_excel(empIO)
        incIO= "incIO/" + studycounty2 + '.xlsx'
        incIO = pandas.read_excel(incIO)

        vhtdiffcon = absolute(convhtbase2 - contvhtbui2)
        savemoneycon = vhtdiffcon * vottvalue2
        finalyearcon = savemoneycon
        zeroyearcon = 0
        steps = finalyearcon / (predictyear2 - 2015 - 1)
        totalsavingcon = 0
        inforecast = predictyear2 - 2015
        for savemoneycon in my_range(zeroyearcon, finalyearcon, steps):
            npvvalue = savemoneycon / ((1 + npvv) ** (predictyear2 - 2015 - (inforecast)))
            inforecast = inforecast - 1
            totalsavingcon = totalsavingcon + npvvalue
        ident = numpy.identity(20)
        IOop2 = IOop.as_matrix()
        IOop2 = IOop2[:,1:]
        print(ident)
        print("################################################################")
        print(IOop2.shape )
#        print(trIOop["411"].values )
        print(empIO.shape)
        print(incIO.shape)
        
#        trIOop = trIOop["411"].values
        empIO =  empIO.empcoeff 
        incIO =  incIO.inccoeff
        
        LeoIOop = numpy.subtract(ident, IOop2)
        
        Leoinvop = numpy.linalg.inv(LeoIOop)

        trIOop2 = trIOop * totalsavingcon * 365
        finalIOop = numpy.matmul(Leoinvop, trIOop2)
        
        print("##################################################################")
        print(finalIOop.shape)
        print("##################################################################")
        print(finalIOop)
        print("##################################################################")
        print(empIO)
        print("##################################################################")
        print(incIO)
        empIO=empIO.as_matrix()
        empIO=numpy.diagflat(empIO)
        incIO=incIO.as_matrix()
        incIO=numpy.diagflat(incIO)
        finalEMP=numpy.matmul( empIO, finalIOop)
        finalinc=numpy.matmul( incIO, finalIOop)

        # output
        self.zerozero = finalIOop.at[1, 411]
        self.zero = finalIOop.at[1, 411]
        self.one = finalIOop.at[2, 411]
        self.two = finalIOop.at[3, 411]
        self.three = finalIOop.at[4, 411]
        self.four = finalIOop.at[5, 411]
        self.five = finalIOop.at[6, 411]
        self.six = finalIOop.at[7, 411]
        self.seven = finalIOop.at[8, 411]
        self.eightt = finalIOop.at[9, 411]
        self.nine = finalIOop.at[10, 411]
        self.ten = finalIOop.at[11, 411]
        self.eleven = finalIOop.at[12, 411]
        self.twleve = finalIOop.at[13, 411]
        self.thirteen = finalIOop.at[14, 411]
        self.fourteen = finalIOop.at[15, 411]
        self.fifteen = finalIOop.at[16, 411]
        self.sixteen = finalIOop.at[17, 411]
        self.seventeen = finalIOop.at[18, 411]
        self.eighteen = finalIOop.at[19, 411]
        self.outputbenecon = finalIOop.sum().values[0]

        # output
        # round output
        self.zerozero = round(self.zerozero, 2)
        self.zero = round(self.zero, 2)
        self.one = round(self.one, 2)
        self.two = round(self.two, 2)
        self.three = round(self.three, 2)
        self.four = round(self.four, 2)
        self.five = round(self.five, 2)
        self.six = round(self.six, 2)
        self.seven = round(self.seven, 2)
        self.eightt = round(self.eightt, 2)
        self.nine = round(self.nine, 2)
        self.ten = round(self.ten, 2)
        self.eleven = round(self.eleven, 2)
        self.twleve = round(self.twleve, 2)
        self.thirteen = round(self.thirteen, 2)
        self.fourteen = round(self.fourteen, 2)
        self.fifteen = round(self.fifteen, 2)
        self.sixteen = round(self.sixteen, 2)
        self.seventeen = round(self.seventeen, 2)
        self.eighteen = round(self.eighteen, 2)
        self.outputbenecon = round(self.outputbenecon, 2)

        # employment
        self.zerozeroemp = finalEMP.at[0, 411]
        self.zeroemp = finalEMP.at[1, 411]
        self.oneemp = finalEMP.at[2, 411]
        self.twoemp = finalEMP.at[3, 411]
        self.threeemp = finalEMP.at[4, 411]
        self.fouremp = finalEMP.at[5, 411]
        self.fiveemp = finalEMP.at[6, 411]
        self.sixemp = finalEMP.at[7, 411]
        self.sevenemp = finalEMP.at[8, 411]
        self.eighttemp = finalEMP.at[9, 411]
        self.nineemp = finalEMP.at[10, 411]
        self.tenemp = finalEMP.at[11, 411]
        self.elevenemp = finalEMP.at[12, 411]
        self.twleveemp = finalEMP.at[13, 411]
        self.thirteenemp = finalEMP.at[14, 411]
        self.fourteenemp = finalEMP.at[15, 411]
        self.fifteenemp = finalEMP.at[16, 411]
        self.sixteenemp = finalEMP.at[17, 411]
        self.seventeenemp = finalEMP.at[18, 411]
        self.eighteenemp = finalEMP.at[19, 411]
        self.emptotal = finalEMP.sum().values[0]
        
        
        # round emp
        self.zerozeroemp = round(self.zerozeroemp, 0)
        self.zeroemp = round(self.zeroemp, 0)
        self.oneemp = round(self.oneemp, 0)
        self.twoemp = round(self.twoemp, 0)
        self.threeemp = round(self.threeemp, 0)
        self.fouremp = round(self.fouremp, 0)
        self.fiveemp = round(self.fiveemp, 0)
        self.sixemp = round(self.sixemp, 0)
        self.sevenemp = round(self.sevenemp, 0)
        self.eighttemp = round(self.eighttemp, 0)
        self.nineemp = round(self.nineemp, 0)
        self.tenemp = round(self.tenemp, 0)
        self.elevenemp = round(self.elevenemp, 0)
        self.twleveemp = round(self.twleveemp, 0)
        self.thirteenemp = round(self.thirteenemp, 0)
        self.fourteenemp = round(self.fourteenemp, 0)
        self.fifteenemp = round(self.fifteenemp, 0)
        self.sixteenemp = round(self.sixteenemp, 0)
        self.seventeenemp = round(self.seventeenemp, 0)
        self.eighteenemp = round(self.eighteenemp, 0)
        self.emptotal = round(self.emptotal, 0)

        # income
        
        self.zerozeroinc = finalinc.at[0, 411]
        self.zeroinc = finalinc.at[1, 411]
        self.oneinc = finalinc.at[2, 411]
        self.twoinc = finalinc.at[3, 411]
        self.threeinc = finalinc.at[4, 411]
        self.fourinc = finalinc.at[5, 411]
        self.fiveinc = finalinc.at[6, 411]
        self.sixinc = finalinc.at[7, 411]
        self.seveninc = finalinc.at[8, 411]
        self.eighttinc = finalinc.at[9, 411]
        self.nineinc = finalinc.at[10, 411]
        self.teninc = finalinc.at[11, 411]
        self.eleveninc = finalinc.at[12, 411]
        self.twleveinc = finalinc.at[13, 411]
        self.thirteeninc = finalinc.at[14, 411]
        self.fourteeninc = finalinc.at[15, 411]
        self.fifteeninc = finalinc.at[16, 411]
        self.sixteeninc = finalinc.at[17, 411]
        self.seventeeninc = finalinc.at[18, 411]
        self.eighteeninc = finalinc.at[19, 411]
        self.inctotal = finalinc.sum().values[0]
        

        # round income
        self.zerozeroinc = round(self.zerozeroinc, 2)
        self.zeroinc = round(self.zeroinc, 2)
        self.oneinc = round(self.oneinc, 2)
        self.twoinc = round(self.twoinc, 2)
        self.threeinc = round(self.threeinc, 2)
        self.fourinc = round(self.fourinc, 2)
        self.fiveinc = round(self.fiveinc, 2)
        self.sixinc = round(self.sixinc, 2)
        self.seveninc = round(self.seveninc, 2)
        self.eighttinc = round(self.eighttinc, 2)
        self.nineinc = round(self.nineinc, 2)
        self.teninc = round(self.teninc, 2)
        self.eleveninc = round(self.eleveninc, 2)
        self.twleveinc = round(self.twleveinc, 2)
        self.thirteeninc = round(self.thirteeninc, 2)
        self.fourteeninc = round(self.fourteeninc, 2)
        self.fifteeninc = round(self.fifteeninc, 2)
        self.sixteeninc = round(self.sixteeninc, 2)
        self.seventeeninc = round(self.seventeeninc, 2)
        self.eighteeninc = round(self.eighteeninc, 2)
        self.inctotal = round(self.inctotal, 2)

        if costornot=="Yes":
            flbenefit=self.outputbenecon-projectcosts
            self.netbenefit=flbenefit
        else:
            self.netbenefit = "Project costs not considered."

        #print basic information in the text box
        self.textinput ="Analyst Name: " + '\n' + analystname + '\n' + "Analysis Date: " + '\n' + analystdate + '\n' + "Project Description:" + '\n' + prodes2 + '\n' + "Study Area" + '\n' + studycounty2+'\n\n'+ "User Input"+'\n\n'+ "Value of Travel Time"+ '\n'+'%d' %(vottvalue2)+'\n'+"Project cost"+'\n'+'%d' %(projectcosts)+'\n'+"Net Present Value (%)"+'\n'+'%d' %(100*npvv)+'\n'+"Forecast Years"+ '\n'+'%d' %(predictyear2)+'\n'+"County Base Scenario VHT"+ '\n'+'%d' %(convhtbase2)+'\n'+"County Built Scenario VHT"+ '\n'+'%d' %(contvhtbui2)
        textinput2=self.textinput
        self.texin1.delete("1.0", END)
        self.texin1.insert(END, textinput2)
        self.texin1.see(END)

    def LoadTable(self):
        # output
        conoutzerozero = self.zerozero
        conoutzero = self.zero
        conoutone = self.one
        conouttwo = self.two
        conoutthree = self.three
        conoutfour = self.four
        conoutfive = self.five
        conoutsix = self.six
        conoutseven = self.seven
        conouteightt = self.eightt
        conoutnine = self.nine
        conoutten = self.ten
        conouteleven = self.eleven
        conouttwleve = self.twleve
        conoutthirteen = self.thirteen
        conoutfourteen = self.fourteen
        conoutfifteen = self.fifteen
        conoutsixteen = self.sixteen
        conoutseventeen = self.seventeen
        conouteighteen = self.eighteen
        outputbenecon=self.outputbenecon
        netbenefits     =self.netbenefit

        # employment
        empzerozero = self.zerozeroemp
        empzero = self.zeroemp
        empone = self.oneemp
        emptwo = self.twoemp
        empthree = self.threeemp
        empfour = self.fouremp
        empfive = self.fiveemp
        empsix = self.sixemp
        empseven = self.sevenemp
        empeightt = self.eighttemp
        empnine = self.nineemp
        empten = self.tenemp
        empeleven = self.elevenemp
        emptwleve = self.twleveemp
        empthirteen = self.thirteenemp
        empfourteen = self.fourteenemp
        empfifteen = self.fifteenemp
        empsixteen = self.sixteenemp
        empseventeen = self.seventeenemp
        empeighteen = self.eighteenemp
        emptotaltable = self.emptotal

        # inc
        inczerozero = self.zerozeroinc
        inczero = self.zeroinc
        incone = self.oneinc
        inctwo = self.twoinc
        incthree = self.threeinc
        incfour = self.fourinc
        incfive = self.fiveinc
        incsix = self.sixinc
        incseven = self.seveninc
        inceightt = self.eighttinc
        incnine = self.nineinc
        incten = self.teninc
        inceleven = self.eleveninc
        inctwleve = self.twleveinc
        incthirteen = self.thirteeninc
        incfourteen = self.fourteeninc
        incfifteen = self.fifteeninc
        incsixteen = self.sixteeninc
        incseventeen = self.seventeeninc
        inceighteen = self.eighteeninc
        inctotaltable = self.inctotal

        self.lb_list = [
            (conoutzerozero, empzerozero, inczerozero),
            (conoutzero, empzero, inczero),
            (conoutone, empone, incone),
            (conouttwo, emptwo, inctwo),
            (conoutthree, empthree, incthree),
            (conoutfour, empfour, incfour),
            (conoutfive, empfive, incfive),
            (conoutsix, empsix, incsix),
            (conoutseven, empseven, incseven),
            (conouteightt, empeightt, inceightt),
            (conoutnine, empnine, incnine),
            (conoutten, empten, incten),
            (conouteleven, empeleven, inceleven),
            (conouttwleve, emptwleve, inctwleve),
            (conoutthirteen, empthirteen, incthirteen),
            (conoutfourteen, empfourteen, incfourteen),
            (conoutfifteen, empfifteen, incfifteen),
            (conoutsixteen, empsixteen, incsixteen),
            (conoutseventeen, empseventeen, incseventeen),
            (conouteighteen, empeighteen, inceighteen),
            (outputbenecon, emptotaltable, inctotaltable)
        ]

        lb_listx=self.lb_list
        lb_list2=['11 Ag, Forestry, Fish & Hunting', '21 Mining', '22 Utilities', '23 Construction', '31-33 Manufacturing', '42 Wholesale Trade', '44-45 Retail trade', '48-49 Transportation & Warehousing', '51 Information', '52 Finance & insurance', '53 Real estate & rental', '54 Professional- scientific & tech svcs', '55 Management of companies', '56 Administrative & waste services', '61 Educational svcs', '62 Health & social services', '71 Arts- entertainment & recreation', '72 Accommodation & food services', '81 Other services', '92 Government & non NAICs', 'Total','Net Benefit']
        self.lb_listnaics=lb_list2
        mycount = 0
        for item in lb_listx:
            item2=lb_list2[mycount]
            mycount=mycount+1
            self.treeview.insert('', 'end', text=item2, values=item)


    def savefile(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")

        lb_listcon=self.lb_list
        lb_listnaics=self.lb_listnaics
        outputlist = [row[0] for row in lb_listcon]
        employmentlist = [row[1] for row in lb_listcon]
        incomelist=[row[2] for row in lb_listcon]


        saveoutput=list(zip(lb_listnaics,outputlist,employmentlist,incomelist))
        tableoutput=tabulate(saveoutput,headers=['Sector','Sector Output Impact ($)','Sector Employment Impact','Sector Income Impact ($)'],floatfmt=".2f")
        print(tableoutput)
        information=self.textinput
        textinput3=str(information)+'\n'+str(tableoutput)

        if file:
            file.write(textinput3)
            file.close()

    def clear_it(self):
        self.texin1.delete("1.0",END)
        for row in self.treeview.get_children():
            self.treeview.delete(row)

              

app = FDOTTOOL()
app.geometry("800x600")
app.mainloop()
