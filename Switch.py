# Project 2 for OMS6250
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015
			    												

from Message import *
from StpSwitch import *

class Switch(StpSwitch):
    

    class Switch_Meta_Data():
        
        def __init__(self):
            self.root = 0;
            self.distance = 0;
            self.active_links = list();
            self.pathThrough = False;


    def __init__(self, idNum, topolink, neighbors):    
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)
        self.data = self.Switch_Meta_Data()
        self.data.root = self.switchID
        self.data.pathThrough = self.switchID


        
        #TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.

    def send_initial_messages(self):
        #TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
	#      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for  neighbor in self.links:
            msg = Message(self.switchID, self.data.distance, self.switchID, neighbor, False)
            self.send_message(msg)
        return
        
    def process_message(self, message):
        #TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.
        #print("***********************************************************************")        
        #print("Interogatting Message\n Claimed Root:" + str(message.root) + " \nDISTANCE FROM ROOT: " + str(message.distance) + "\nOrigin:" + str(message.origin) + "\nDestination:" + str(message.destination) + "\nPassthrough:" + str(message.pathThrough) )
        #print("***********************************************************************")
        #print("Get data info at start\n ROOT:" + str(self.data.root) + " \nDISTANCE FROM ROOT: " + str(self.data.distance) + "\nACTIVE LINKS:" + str(self.data.active_links) + "\nPaththrough " + str(self.data.pathThrough) )

        rootUpdated = False
        linkRemoved = -1
        #print("\tTesting switch " + str(self.switchID) + "'s root of " + str(self.data.root) + " against message's " + str(message.origin) + " root of " + str(message.root))
        if(message.root < self.data.root):
            #print("\tMessages root is lower than we go into this body")
            self.data.root = message.root
            #print("\tIncrement Distance")
            #Wehn the root changes it needs to remove any active links and build over again
            if(self.data.distance == 0):
                self.data.active_links = list()
            self.data.distance = message.distance + 1
            rootUpdated = True
            if message.origin not in self.data.active_links:
                #print("\tadding link of " + str(message.origin) +" to switches active links of switch " + str(self.switchID))
                self.data.active_links.append(message.origin)
            if(self.data.pathThrough != message.origin and self.data.pathThrough != self.switchID):
                if  self.data.pathThrough in self.data.active_links:
                        #print("\t remove the link " + str(self.data.pathThrough) + ", no longer needed  from " + str(self.switchID))
                        self.data.active_links.remove(self.data.pathThrough) #remove prev lin
                        #self.data.active_links = list()
                        linkRemoved = self.data.pathThrough
            self.data.pathThrough = message.origin

        
        if(message.root == self.data.root):
            if(message.distance + 1  < self.data.distance):
               if message.origin in self.data.active_links:
                   self.data.active_links.remove(message.origin) #remove prev lin
              #  if message.origin not in self.data.active_links:                   
              #      self.data.active_links.append(message.origin)
       #         self.data.passThough = message.origin


        #if the distance or the root has not been updated 
        #We must check to see if the passthrough is true
        #on message, we must do this in order to see if 
        #previous link add its to 
        if(message.pathThrough == True ):
            if message.origin not in self.data.active_links:
                self.data.active_links.append(message.origin)

        #if(message.pathThrough == False)

       # if(message.pathThrough == False):
       #     if message.origin  in self.data.active_links:
       #        self.data.active_links.remove(message.origin)

        if(rootUpdated):
            for neighbor in self.links:
                bool_pass = False
               # / #print("TEST SWITCH " + str(self.switchID))

                if(neighbor == message.origin and neighbor != linkRemoved):
                    #print("\t\tPassthrough is true on this")
                    bool_pass = True
                    #print("\t\t bool is now " + str(bool_pass))

                #print("\t\t+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                #print("\t\tSending out message\n\t\tClaimed Root:" + str(message.root) + " \n\t\tDISTANCE FROM ROOT: " + str(self.data.distance) + "\n\t\tOrigin:" + str(self.switchID) 
                 #   + "\n\t\tDestination:" + str(neighbor) + "\n\t\tPassthrough:" + str(bool_pass) )    
                #print("\t\t+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                msg = Message(self.data.root, self.data.distance, self.switchID, neighbor, bool_pass)
                self.send_message(msg)
        #Implement a way to update!!!

        #print("Get data info at end for switch " + str(self.switchID) + "\nROOT:" + str(self.data.root) + " \nDISTANCE FROM ROOT: " + str(self.data.distance) + "\nACTIVE LINKS:" 
        #    + str(self.data.active_links) + "\nPaththrough " + str(self.data.pathThrough) )

        return
        
    def generate_logstring(self):
        #TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      #print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        switch_longstring = ""
        self.data.active_links.sort()
        for link in self.data.active_links:
            switch_longstring = switch_longstring + (str(self.switchID) + " - " + str(link) + ", ")

        switch_longstring = switch_longstring[:-2]
        return switch_longstring
