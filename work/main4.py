from urllib import response
import requests
import icalendar
import rdflib
from rdflib import URIRef
from bs4 import BeautifulSoup
import json
from rdflib.namespace import XSD, RDF, RDFS

# fichier ICS 
with open("ADECal.ics", "rb") as f:
    ics_data = f.read()

# parseur
calendar = icalendar.Calendar.from_ical(ics_data)

# rdf graph
g = rdflib.Graph()

# triple + event -> graph
for event in calendar.walk("VEVENT"):
    tgraph = rdflib.Graph()
    id = event["uid"]
    eventName = event["SUMMARY"]
    eventStart = event["DTSTART"].dt
    eventEnd = event["DTEND"].dt
    eventLocation = event["LOCATION"]
    
    event = rdflib.URIRef(id)
    tgraph.bind("schema", "http://schema.org/")
    tgraph.add((event, rdflib.RDF.type, rdflib.URIRef("http://schema.org/Event")))

    tgraph.add((event, rdflib.URIRef("http://schema.org/name"), rdflib.Literal(eventName)))
    tgraph.add((event, rdflib.URIRef("http://schema.org/startDate"), rdflib.Literal(eventStart)))
    tgraph.add((event, rdflib.URIRef("http://schema.org/endDate"), rdflib.Literal(eventEnd)))
    tgraph.add((event, rdflib.URIRef("http://schema.org/location"), rdflib.Literal(eventLocation)))
    
    headers = {'Content-Type': 'text/turtle'}
    requests.post('https://territoire.emse.fr/ldp/bouzianeInouss/', headers=headers, data=tgraph.serialize(format='turtle').encode('utf8'), auth=('ldpuser', 'LinkedDataIsGreat'))

    g += tgraph
    
# deuxième contexte
# calendar = rdflib.URIRef("http://example.com/calendars/soukainaCalendar")
# g.add((calendar, rdflib.RDF.type, rdflib.URIRef("http://schema.org/Calendar")))

# g.add((calendar, rdflib.URIRef("http://schema.org/name"), rdflib.Literal("my calendar")))
# g.add((calendar, rdflib.URIRef("http://schema.org/description"), rdflib.Literal("Here is my personal calendar.")))

# Serialize the RDF data in Turtle format
# calendar_rdf = g.serialize(format="turtle")

#print("ics calendar ADECal\n")
# print(calendar_rdf)

print("------------------------------------------------")

def listUpcomingEvents(date,g):
    #    This function takes in a date and RDF graph as input and returns a list of upcoming events that are starting after the input date.

    query = """
    PREFIX schema: <http://schema.org/>
    SELECT ?event ?start
    WHERE {
        ?event a schema:Event ;
               schema:startDate ?start .
        FILTER (?start >= '""" + str(date) + """'^^xsd:dateTime)
    }

    """

    results = g.query(query)
    eventList = []
    for result in results:
        event = result[0]
        start = result[1]
        eventName = g.value(subject=event, predicate=URIRef("http://schema.org/name"))
        eventList.append({"Event":eventName,"Start Date":start})
    return eventList


event = listUpcomingEvents("2022-09-06T07:00:00", g)
print(event)
print("------------------------------------------------")


#add events on ldp territoire
events = [
    {
        "name": "Semantic Web Work Session",
        "rdf": """
        @prefix schema: <http://schema.org/> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <> a schema:Event ;
           schema:name "Semantic Web Work Session" ;
           schema:startDate "2022-12-16T09:00:00"^^xsd:dateTime ;
           schema:endDate "2022-12-16T17:00:00"^^xsd:dateTime ;
           schema:location <http://example.com/locations/classroom> .
        """
    },
    {
        "name": "Semantic Web Practice Session",
        "rdf": """
        @prefix schema: <http://schema.org/> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <> a schema:Event ;
           schema:name "Semantic Web Practice Session" ;
           schema:startDate "2023-01-06T09:00:00"^^xsd:dateTime ;
           schema:endDate "2023-01-06T17:00:00"^^xsd:dateTime ;
           schema:location <http://example.com/locations/classroom> .
        """
    }
]


burl = "https://territoire.emse.fr/ldp/"

# Set the headers for the request
headers = {
    "Content-Type": "text/turtle",  # The format of the RDF data
    "Slug": "my-calendar",  # The name of the calendar resource
    "Link": '<http://www.w3.org/ns/ldp#BasicContainer>; rel="type"',  # The type of the calendar resource
}


print("------------------------------------------------")


SCHEMA = rdflib.Namespace("http://schema.org/")

def alentoor():
    requete = requests.get("https://www.alentoor.fr/saint-etienne/agenda")
    page = BeautifulSoup(requete.content, "html.parser")
    data = [
        json.loads(jsonLd.string) for jsonLd in page.find_all("script", type="application/ld+json")
    ]
    graph = rdflib.Graph()
    for d in data:
        tgraph = rdflib.Graph()
        id = URIRef('alentoor-' + d['@id'].split('/')[-1])
        dstart = rdflib.Literal(d['startDate'], datatype=XSD.date)
        dend = rdflib.Literal(d['endDate'], datatype=XSD.date)
        summary = rdflib.Literal(d['name'], lang="fr")
        description = rdflib.Literal(d['description'], datatype=XSD.string)
        tgraph.add((id, RDF.type, SCHEMA.Calendar))
        tgraph.add((id, RDFS.label, summary))
        tgraph.add((id, SCHEMA.startDate, dstart))
        tgraph.add((id, SCHEMA.endDate, dend))
        tgraph.add((id, SCHEMA.description, description))
        graph += tgraph
        headers = {'Content-Type': 'text/turtle'}
        requests.post('https://territoire.emse.fr/ldp/bouzianeInouss/', headers=headers, data=tgraph.serialize(format='turtle').encode('utf8'), auth=('ldpuser', 'LinkedDataIsGreat'))
    return graph

graph_alentoor = alentoor()
print(graph_alentoor.serialize(format='turtle'))

g += graph_alentoor
print(g.serialize(format='turtle'))


#pour retrouver plus facilement notre fichier
#g.serialize(format='turtle', destination='fichier.ttl') 
#g = rdflib.Graph().parse('fichier.ttl')


#def mark_event_attendance(event_uri, attendee_uri):
 #   g.add((event_uri, schema.attendee, attendee_uri))

#Modify an existing event to indicate that someone has attended it
#def get_event_attendance(event_uri):
 #   query = """
  #  SELECT ?attendee
   # WHERE {
    #    <event_uri> <http://schema.org/attendee> ?attendee
    #}

#results = g.query(query.replace("event_uri", event_uri))
#attendees = [result[0] for result in results]
#return attendees


#author Inouss Bouziane