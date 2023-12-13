from rdflib import Graph
from rdflib.namespace import RDF, RDFS, SKOS, NamespaceManager
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, \
                           PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, \
                           VOID, XSD
from uuid import uuid4

def create_address(g:Graph, namespace_url:str, label:str, lang:str, landmarks:dict, spatial_relations:list, target:int=None, datetime:str=None):
    namespace = Namespace(namespace_url)

    if None in (landmarks, spatial_relations):
        return None
    
    landmark_uris = {}
    for key, landmark in landmarks.items():
        landmark_uri = create_landmark(g, namespace, landmark, lang)
        landmark_uris[key] = landmark_uri

    if target is None:
        target_uri = create_landmark(g, namespace, {}, lang)
    else:
        target_uri = landmark_uris.get(target)

    next_addr_seg_uri = None
    for spat_rel in reversed(spatial_relations):
        spatial_rel_uri = create_spatial_relation(g, namespace, spat_rel[0], lang)
        addr_seg_uri = generate_uri(namespace, "AS")
        locatum = landmark_uris.get(spat_rel[1])
        if locatum is None:
            locatum = target_uri

        relatums = []
        for x in spat_rel[2]:
            relatum_lm = landmark_uris.get(x)
            if relatum_lm is None:
                relatum_lm = target_uri

            relatums.append(relatum_lm)

        create_addr_segment(g, namespace, spatial_rel_uri, addr_seg_uri, locatum, relatums, next_addr_seg_uri)
        next_addr_seg_uri = addr_seg_uri

    create_address_main_elem(g, namespace, label, target_uri, next_addr_seg_uri, lang, datetime)

def create_address_main_elem(g:Graph, namespace:Namespace, label, target_uri:URIRef, first_step_uri:URIRef, lang:str=None, datetime:str=None):
    addr_uri = generate_uri(namespace, "ADDR")
    g.add((addr_uri, RDF.type, namespace["Address"]))
    g.add((addr_uri, RDFS.label, Literal(label, lang=lang)))
    g.add((addr_uri, namespace["targets"], target_uri))
    g.add((addr_uri, namespace["firstStep"], first_step_uri))
    if datetime is not None:
        g.add((addr_uri, namespace["dateTime"], Literal(datetime, datatype=XSD.dateTime)))


def create_landmark(g:Graph, namespace:Namespace, landmark_dict:dict, lang:str=None):
    landmark_types = {"thoroughfare":"Thoroughfare", "undefined":"Undefined", None: "Undefined",
                      "city":"City", "housenumber":"HouseNumber", "district":"District", "structure":"Structure"}
    l_uri = generate_uri(namespace, "LM")
    l_label = landmark_dict.get("label")
    l_type = landmark_types.get(landmark_dict.get("type"))

    g.add((l_uri, RDF.type, namespace["Landmark"]))
    g.add((l_uri, namespace["isLandmarkType"], namespace[l_type]))

    if l_label is not None:
        g.add((l_uri, RDFS.label, Literal(l_label, lang=lang)))

    return l_uri

def create_addr_segment(g:Graph, namespace:Namespace, spatial_rel_uri:URIRef, addr_seg_uri:URIRef, locatum:URIRef, relatums:list[URIRef], next_addr_segment:URIRef=None):
    if next_addr_segment is not None:
        g.add((addr_seg_uri, RDF.type, namespace["AddressSegment"]))
        g.add((addr_seg_uri, namespace["nextStep"], next_addr_segment))
    else:
        g.add((addr_seg_uri, RDF.type, namespace["FinalAddressSegment"]))

    g.add((addr_seg_uri, namespace["locatum"], locatum))

    for relatum in relatums:
        g.add((addr_seg_uri, namespace["relatum"], relatum))

    g.add((addr_seg_uri, namespace["isSpatialRelationType"], spatial_rel_uri))
    
def create_spatial_relation(g:Graph, namespace:Namespace, label:str, lang:str=None):
    spatial_rel = generate_uri(namespace, "SR")
    label_lang = Literal(label, lang=lang)
    g.add((spatial_rel, RDF.type, OWL.NamedIndividual))
    g.add((spatial_rel, RDF.type, namespace["AddressSegmentType"]))
    g.add((spatial_rel, RDF.type, SKOS.Concept))
    g.add((spatial_rel, RDFS.label, label_lang))
    return spatial_rel

def generate_uri(namespace:Namespace=None, prefix:str=None):
    if prefix:
        return namespace[f"{prefix}_{uuid4().hex}"]
    else:
        return namespace[uuid4().hex]
    
def generate_uuid():
    return uuid4().hex
