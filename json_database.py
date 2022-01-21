#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 11:41:38 2021

@author: charliesowerby


Going to use pandas to load in the spells all in memory in a pandas dataframe
"""

#%% Imports 

import pandas as pd 
import os 



#%% Notes

""" 

For Spell Memory:
    -Have a Memory class to hold a pandas DataFrame that contains a total list of all the spells 

For Profile Memory: 
    -Create a dictionary where keys are profile names and values are lists of spells that each player has in their spellbook 
    
    -Could consider a situation in which prepared/spellbook spells are stored differently 
    
    
Frontend: 
    - Potentially the SAME GUI? 
    
    - New GUI with raw tkinter? 
    
    - Web Tool? (This is such a pain)

"""






#%% Spells 

class SpellList:
    def __init__(self):
        
        self.spell_filepath = '/Users/charliesowerby/Desktop/Projects/dnd_ui/spells.csv'
    
        # Load filepath 
        try:
            self.df = pd.read_csv(self.spell_filepath)
        
        except:
            print("Error Occured when loading spells")
        
        
        
        
        
       
        
            
        
        
            
        
        
    def query(self, query_dict):
        """ Query the datafarme according to conditions in query_dict
        
        Parameters 
        ----------
        query_dict : dict 
            dictionary formatted to specify parameters, i.e. {'classes':['Wizard', 'Cleric'], level:3}
        
        Returns
        -------
        DataFrame 
            Spells in the df that match the query parameters 
        
        """ 
        
        # TODO: write a translation from dictionary to list of query conditions 
        
 
        
        df = self.spells
        
        
        query_list = [df[category] == query_dict[category] for category in query_dict.keys()]
        
        df = df[query_list]
        
        
        return df 
    
#%% Profiles 

class ProfileList:
    def __init__(self):
        # Want to initialize a list of profiles by checking for saved profiles in the correct location, if none, then 
        
        
        # Profile List 
        self.filepath = '/Users/charliesowerby/Desktop/Projects/dnd_ui/profiles.csv'
        
        
        pass 
    def save_profiles(self):
        self.profiles.to_csv(self.profile_filepath)

        
    
#%% Save Profiles 




#%% Main 

if __name__ == "__main__":
    mem = Memory()
    
    