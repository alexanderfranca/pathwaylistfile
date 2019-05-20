import re
import pprint
import sys


class PathwayListFile:
    """
    Deals with KEGG pathway.list file. 

    Example
        pathway.list file has the following format until this momment:
            #Metabolism
            ##Global and overview maps
            01100   Metabolic pathways
            01120   Microbial metabolism in diverse environments
            ##Carbohydrate metabolism
            00010   Glycolysis / Gluconeogenesis
            00020   Citrate cycle (TCA cycle)
            00030   Pentose phosphate pathway

    Attributes:
        pathway_list_file(file): File handle that represents the pathway.list file.
        metabolic_pathways(dict): Metabolic pathways complete data (classes, subclasses, pathway names and its map numbers).
        maps_and_pathways(dict): Metabolic map numbers and its pathways names.
        metabolic_pathways_names(list): Metabolic pathway names.
        metabolic_pathways_map_numbers(list): Metabolic pathway map numbers.
        metabolic_pathways_super_classes(list): Metabolic pathways superclasses names.
        metabolic_pathways_classes(list): Metabolic pathways classes names.
    """

    def __init__(self, pathway_file=None):

        self.pathway_file = pathway_file

        self.metabolic_pathways={}
        self.maps_and_pathways={}
        self.metabolic_pathways_names=[]
        self.metabolic_pathways_map_numbers=[]
        self.metabolic_pathways_super_classes=[]
        self.metabolic_pathways_classes=[]

    def is_metabolic_super_class( self, string=None ):
        """
        Returns if the string means a super class of a metabolic pathway.

        That kind of string is something like: '#Organismal Systems'
        """

        re_super_class = re.compile('^#[A-Z]')

        if re_super_class.search( string ):
            return True
        else:
            return False

    def is_metabolic_class( self, string=None ):
        """
        Returns if the string means a class of a metabolic pathway.

        That kind of string is something like: '##Immune system'
        """

        re_class = re.compile('^##[A-Z]')

        if re_class.search( string ):
            return True
        else:
            return False

    def is_metabolic_map_record( self, string=None ):
        """
        Returns if the string means metabolic pathway map record. 

        That kind of string is something like: '07231   Sodium channel blocking drugs'
        """

        re_map = re.compile("^([0-9]{1,})\s.*")

        if re_map.search( string ):
            return True
        else:
            return False


    def metabolic_pathway_map_number( self, string=None ):
        """
        Returns the metabolic patwhay map number from a string.

        That kind of string is something like: '07231   Sodium channel blocking drugs'
        """

        re_map  = re.compile("^([0-9]{1,})\s.*")
        result = re_map.search( string )

        return result.group(1)


    def metabolic_pathway_map_name( self, string=None ):
        """
        Returns the metabolic patwhay map name from a string.

        That kind of string is something like: '07231   Sodium channel blocking drugs'
        """

        re_map  = re.compile("^[0-9]{1,}\s(.*)")
        result = re_map.search( string )
        result = result.group(1)
        result = re.sub('^\ {1,}', '', result )

        return result

    def generate_metabolic_pathway_data( self ):
        """
        Read metabolic pathways pathway.list and returns full filled dictionary.

        Returns:
            (dict): List of all metabolic pathways names and map names.
        """

        # Parse metabolic pathways names and classes/subclasses.
        with open(self.pathway_file) as f:
            for line in f:

                # Remove end of line special chars.
                line = line.rstrip('\r\n')

                if self.is_metabolic_super_class( line ):

                    # Superclass has '#' in its name. We're removing it
                    line = line.replace('#','')
                    self.metabolic_pathways[ line ] = {} 
                    current_super_class = line

                if self.is_metabolic_class( line ):

                    # Class has '#' in its name. We're removing it.
                    line = line.replace('#','')
                    self.metabolic_pathways[ current_super_class ][ line ] = {}
                    current_class = line

                if self.is_metabolic_map_record( line ):
                    map_number = self.metabolic_pathway_map_number( line )
                    map_name   = self.metabolic_pathway_map_name( line )

                    # types of data:
                    # 1. Hierachy based by super classes and classes.
                    self.metabolic_pathways[ current_super_class ][ current_class ][ map_number ] = map_name

                    # 2. Based in map number. That's a dump dictionary because of the superclass and class repetitions,
                    # but that's better to query data map number. 
                    self.maps_and_pathways[ map_number ] = { 'map_name': map_name, 'superclass': current_super_class, 'class': current_class }

                    # 3. Simple list of metabolic pathways names
                    self.metabolic_pathways_names.append( map_name )

                    # 4. Simple list of metabolic pathway maps number
                    self.metabolic_pathways_map_numbers.append( map_number )

                    # 5. Simple list of metabolic pathways super classes
                    self.metabolic_pathways_super_classes.append( current_super_class )

                    # 6. Simple list of metabolic pathways subclasses
                    self.metabolic_pathways_classes.append( current_class )


    def get_maps_and_pathways( self ):
        """
        Returns a dictionary containing all map numbers and its related data.

        Returns:
            (dict): All map numbers and its related data.
        """

        if len( self.maps_and_pathways ) == 0:
            self.generate_metabolic_pathway_data()

        return self.maps_and_pathways


    def pathways_and_maps( self ):
        """
        Returns a dictionary containing all pathways names, classes, superclasses and map numbers.

        Returns:
            (dict): All pathways and its related data.
        """

        if len( self.metabolic_pathways) == 0:
            self.generate_metabolic_pathway_data()

        return self.metabolic_pathways


    def map_pathway_data_by_map_number( self, map_number=None ):
        """
        Returns map pathway data by map number (superclass, class and metabolica pathway name)

        Args:
            map_number(str): Metabolic pathway map number.

        Returns:
            (dict): Data from the metabolic pathway map.
        """

        data = self.get_maps_and_pathways()

        return data[map_number]


    def pathways_names( self ):
        """
        Returns all the metabolic pathways names.

        Returns:
            (list): Pathways names.
        """

        if len( self.maps_and_pathways ) == 0:
            self.generate_metabolic_pathway_data()

        data = set(self.metabolic_pathways_names)
        data = list(data)

        return data


    def pathways_super_classes( self ):
        """
        Returns all the metabolic pathways super classes.

        Returns:
            (list): Pathways superclasses.
        """

        if len( self.maps_and_pathways ) == 0:
            self.generate_metabolic_pathway_data()

        data = set(self.metabolic_pathways_super_classes)
        data = list(data)

        return data


    def pathways_classes( self ):
        """
        Returns all metabolic pathways classes.

        Returns:
            (list): Pathways classes.
        """

        if len( self.maps_and_pathways ) == 0:
            self.generate_metabolic_pathway_data()

        data = set(self.metabolic_pathways_classes)
        data = list(data)

        return data


    def pathways_map_numbers( self ):
        """
        Returns all metabolic pathways map numbers.

        Returns:
            (list): Pathway maps numbers.
        """

        if len( self.maps_and_pathways ) == 0:
            self.generate_metabolic_pathway_data()

        data = set(self.metabolic_pathways_map_numbers)
        data = list(data)

        return data

    def all_pathways( self ):
        """
        Returns all metabolic pathways data.

        Returns:
            (list): Pathway data.
        """

        if len( self.maps_and_pathways ) == 0:
            self.generate_metabolic_pathway_data()

        return self.metabolic_pathways 



    

