# semanticWebProject
Here is the code for our semantic web project

This script processes an ICS file, named ADECal.ics, which contains calendar events, by using icalendar and rdflib libraries to convert it into an RDF graph. The resulting RDF graph is then transmitted to LDP using the requests library, along with a turtle format serialization. Finally, the script queries the RDF graph to list all events that are scheduled to occur after a certain date.

# Prerequisites
Python 3
icalendar library
rdflib library
requests library
bs4 library (BeautifulSoup)

# Run
Ensure that you have the ICS file "ADECal.ics" in the same directory as the main.
Run the main4.py script.

# View the results
In the resultat.txt, you will have all the data about the ics file printed in alphabetical order (is it to make sure that we have the good data) so we have the following fields : endDate, location, name and startDate .

In the file fichier.ttl we have all the event taking from the calendar with all the data related to each events. The id of each event begin with ADE so that we know that it is a course type event. 
In resultatSaintEtienne.txt we have all the event that are not courses but take place in saint-etienne from alentoor.

When we run the main4.py, we can open the link : https://territoire.emse.fr/ldp/ and see the line : <member xmlns="http://www.w3.org/ns/ldp#" rdf:resource="https://territoire.emse.fr/ldp/bouziane/"/> to validate that its work. 

We can see the result in the following link : https://territoire.emse.fr/ldp/bouziane/

If we open one of the link like this one : https://territoire.emse.fr/ldp/bouziane/ade60323032322d3230323353542d455449454e4e452d33363236322d302d30/ 
we can see the rdf graph result of the choosen event : ade60323032322d3230323353542d455449454e4e452d33363236322d302d30
with the fields : name, endDate, startDate, location

# note
we can find SPARQL query in the function listUpcomingEvents.
Note that this function take a date and a graph into parameters, to print a list of event with a start date after the date in parameter.

