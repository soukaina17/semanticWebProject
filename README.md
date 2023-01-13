# semanticWebProject
Here is the code for ou semantic web project

This script processes an ICS file, named ADECal.ics, which contains calendar events, by using icalendar and rdflib libraries to convert it into an RDF graph. The resulting RDF graph is then transmitted to LDP using the requests library, along with a turtle format serialization. Finally, the script queries the RDF graph to list all events that are scheduled to occur after a certain date.
