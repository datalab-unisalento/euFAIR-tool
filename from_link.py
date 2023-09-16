import metadata_evaluator
from data_retriever import retriever
from utility.utility import myprint as mprint
from utility.bcolors import bcolors as bc


methods = ['DCAT_AP', 'DCAT_AP-IT', 'merged']

def try_ckan(url):
    try:
        payloads_generics = retriever.retrieve_payload_generic(url)

        metadata_result_generic = {}

        for method in methods:

            mprint("METADATA EVALUATOR", bc.GREEN)
            metadata_result_generic[method] = metadata_evaluator.metadata_evaluator_generic('', method, payloads_generics, url)
        print(metadata_result_generic)

        return metadata_result_generic
    except Exception as e:
        print(e)