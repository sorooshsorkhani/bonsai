#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Name: metadata_info.py
Description: Stores metadata info constant variables.
"""

from langchain.chains.query_constructor.schema import AttributeInfo

TOOLS_BADGES = ['Reptiles', 'Observation design', 'Ecosystem services', 'Data collection', 
                'Data reporting', 'Data Management', 'Species populations', 'Macroinvertebrates', 
                'Invasive', 'Genetic composition', 'Ecosystem Structure', 'Other Invertebrates',
                'Plants', 'Butterflies', 'Species Populations', 'Birds', 'Migratory',
                'Community composition', 'Freshwater', 'Ecosystem function', 'Ecosystem structure',
                'Fishes', 'Terrestrial', 'Mammals', 'Species traits', 
                'Marine', 'Citizen Science', 'Data analysis', 'Amphibians']

METADATA_FIELD_INFO = [
    # General
    AttributeInfo(
        name="source_type",
        description="The type/category of the document/source. One of [\"GEO BON Publications\", \"BON in a Box Pipelines GitHub\", \"BON in a Box Tools\"]",
        type="string",
    ),
    AttributeInfo(
        name="source",
        description="The source of the document. It includes a link or a file name",
        type="string",
    ),
    # GEO BON Publications
    AttributeInfo(
        name="year",
        description="The year of publication. Used for GEO BON Publications",
        type="integer",
    ),
    AttributeInfo(
        name="page",
        description="The page number of the document. Used for GEO BON Publications",
        type="string",
    ),
    # Tools Catalogue
    AttributeInfo(
        name="tool_title",
        description="The title of the tool. Used for BON in a Box Tools",
        type="string",
    )
]

DOCUMENT_CONTENT_DESCRIPTION = "Extensive and detailed information on a wide range of topics."