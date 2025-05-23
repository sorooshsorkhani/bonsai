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

# few shot examples to use in SelfQueryRetriever
EXAMPLES = [
    {
        "query": "What file format can I use to input protected areas for the protconn pipeline?",
        "filter": "eq(\"document_category\",\"BON in a Box Pipelines GitHub\")",
    },
    {
        "query": "How can I choose the dispersal distance parameter for the protected connected index (protconn) BON in a Box pipeline?",
        "filter": "eq(\"document_category\",\"BON in a Box Pipelines GitHub\")",
    },
    {
        "query": "What is an EBV?",
        "filter": "NO_FILTER",
    },
    {
        "query": "What tools can I use to know where a species can be?",
        "filter": "or(eq(\"document_category\",\"BON in a Box Pipelines GitHub\"), eq(\"document_category\",\"BON in a Box Tools\"))",
    },
    {
        "query": "How are pipelines assembled in BON in a Box?",
        "filter": "eq(\"document_category\",\"BON in a Box Pipelines GitHub\")",
    },
    {
        "query": "If I want to contribute, how are pipelines assembled in BON in a Box?",
        "filter": "eq(\"document_category\",\"BON in a Box Pipelines GitHub\")",
    },
    {
        "query": "What is the link between Essential Biodiversity Variables and biodiversity indicators?",
        "filter": "NO_FILTER",
    },
    {
        "query": "What are some of the models that can be used to prioritize sampling in the context of establishing BONs?",
        "filter": "or(eq(\"document_category\",\"GEO BON Publications\"), eq(\"document_category\",\"BON in a Box Pipelines GitHub\"))",
    },
    {
        "query": "Show GEO BON Publications from 2019 onward",
        "filter": "and(eq(\"document_category\",\"GEO BON Publications\"), gte(\"year\",2019))",
    },
]
