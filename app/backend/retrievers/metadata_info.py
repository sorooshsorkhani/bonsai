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
        name="document_category",
        description="Category of the document. One of [\"GEO BON Publications\", \"BON in a Box Pipelines GitHub\", \"BON in a Box Tools\"]",
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
        description="Publication year (applies to GEO BON Publications)",
        type="integer",
    )
]

DOCUMENT_CONTENT_DESCRIPTION = "Content extracted from scientific publications, BON in a Box repositories, or BON in a Box tools catalogue."