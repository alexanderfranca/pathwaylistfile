import sys
import os
import unittest
from pathwaylistfile.pathwaylistfile import *
import re


class TestPathwayListFile( unittest.TestCase ):

    def setUp( self ):
        self.pathway = PathwayListFile('./tests/fixtures/pathway.list')

    def test_is_metabolic_super_class( self ):

        self.assertTrue( self.pathway.is_metabolic_super_class('#Organismal Systems') )

    def test_is_metabolic_class( self ):

        self.assertTrue( self.pathway.is_metabolic_class('##Immune system') )

    def test_is_metabolic_map_record( self ):

        self.assertTrue( self.pathway.is_metabolic_map_record('07231   Sodium channel blocking drugs') )

    def test_metabolic_pathway_pathway_map_number( self ):

        result =  self.pathway.metabolic_pathway_map_number('07231   Sodium channel blocking drugs')
        self.assertEqual( result, '07231' )

    def test_metabolic_pathway_pathway_map_name( self ):

        result =  self.pathway.metabolic_pathway_map_name('07231   Sodium channel blocking drugs')
        self.assertEqual( result, 'Sodium channel blocking drugs' )

    def test_generate_metabolic_pathway_data( self ):

        self.pathway.generate_metabolic_pathway_data()

        self.assertTrue( type( self.pathway.metabolic_pathways ) is dict )

    def test_maps_and_pathways( self ):

        data = self.pathway.get_maps_and_pathways()

        self.assertEqual( data['07233']['superclass'], 'Drug Development' )

    def test_pathways_and_maps( self ):

        data = self.pathway.pathways_and_maps()

        self.assertEqual( data['Organismal Systems']['Circulatory system']['04260'], 'Cardiac muscle contraction' )


    def test_map_pathway_data_by_map_number( self ):

        data = self.pathway.get_maps_and_pathways()

        map_data = self.pathway.map_pathway_data_by_map_number( '07233' )

        self.assertEqual( map_data['superclass'], 'Drug Development' )


    def test_pathways_names( self ):

        data = self.pathway.pathways_names()

        self.assertTrue( 'Cyclooxygenase inhibitors' in data )

    def test_pathways_super_classes( self ):

        data = self.pathway.pathways_super_classes()

        self.assertTrue( 'Environmental Information Processing' in data )

    def test_pathways_classes( self ):

        data = self.pathway.pathways_classes()

        self.assertTrue( 'Neurodegenerative diseases' in data )

    def test_pathways_map_numbers( self ):

        data = self.pathway.pathways_map_numbers()

        self.assertTrue( '00010' in data )


if __name__ == "__main__":
    unittest.main()
