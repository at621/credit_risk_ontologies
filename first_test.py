from rdflib import Graph, Namespace, RDF, Literal, SKOS

# Define namespaces
crm = Namespace("http://example.org/crm#")
reg = Namespace("http://example.org/regulations#")

# Initialize the graph
g = Graph()
g.bind("crm", crm)
g.bind("reg", reg)
g.bind("skos", SKOS)

# Create a concept scheme for credit risk modeling
g.add((crm.CreditRiskModeling, RDF.type, SKOS.ConceptScheme))
g.add((crm.CreditRiskModeling, SKOS.prefLabel, Literal("Credit Risk Modeling")))
g.add((crm.CreditRiskModeling, SKOS.definition, Literal("A domain dealing with the estimation, analysis, and quantification of the risk of loss due to a borrower’s default.")))

# Create a top concept
g.add((crm.CreditRiskModel, RDF.type, SKOS.Concept))
g.add((crm.CreditRiskModel, SKOS.prefLabel, Literal("Credit Risk Model")))
g.add((crm.CreditRiskModel, SKOS.definition, Literal("A conceptual or mathematical framework to estimate the probability and severity of loss from a counterparty default.")))
g.add((crm.CreditRiskModel, SKOS.topConceptOf, crm.CreditRiskModeling))
g.add((crm.CreditRiskModel, SKOS.inScheme, crm.CreditRiskModeling))

# Define some narrower concepts under CreditRiskModel
g.add((crm.ProbabilityOfDefault, RDF.type, SKOS.Concept))
g.add((crm.ProbabilityOfDefault, SKOS.prefLabel, Literal("Probability of Default")))
g.add((crm.ProbabilityOfDefault, SKOS.definition, Literal("The likelihood that a borrower will fail to meet its debt obligations within a given time horizon.")))
g.add((crm.ProbabilityOfDefault, SKOS.broader, crm.CreditRiskModel))
g.add((crm.ProbabilityOfDefault, SKOS.inScheme, crm.CreditRiskModeling))

g.add((crm.LossGivenDefault, RDF.type, SKOS.Concept))
g.add((crm.LossGivenDefault, SKOS.prefLabel, Literal("Loss Given Default")))
g.add((crm.LossGivenDefault, SKOS.definition, Literal("The fraction of an exposure that is lost if a default occurs.")))
g.add((crm.LossGivenDefault, SKOS.broader, crm.CreditRiskModel))
g.add((crm.LossGivenDefault, SKOS.inScheme, crm.CreditRiskModeling))

# Create narrower concepts for LGD
g.add((crm.LossGivenDefaultForPerforming, RDF.type, SKOS.Concept))
g.add((crm.LossGivenDefaultForPerforming, SKOS.prefLabel, Literal("Loss Given Default for Performing Exposures")))
g.add((crm.LossGivenDefaultForPerforming, SKOS.definition, Literal("LGD applied specifically to exposures currently meeting obligations on time.")))
g.add((crm.LossGivenDefaultForPerforming, SKOS.broader, crm.LossGivenDefault))
g.add((crm.LossGivenDefaultForPerforming, SKOS.inScheme, crm.CreditRiskModeling))

g.add((crm.LossGivenDefaultForNonPerforming, RDF.type, SKOS.Concept))
g.add((crm.LossGivenDefaultForNonPerforming, SKOS.prefLabel, Literal("Loss Given Default for Non-Performing Exposures")))
g.add((crm.LossGivenDefaultForNonPerforming, SKOS.definition, Literal("LGD applied specifically to exposures that are delinquent or in default.")))
g.add((crm.LossGivenDefaultForNonPerforming, SKOS.broader, crm.LossGivenDefault))
g.add((crm.LossGivenDefaultForNonPerforming, SKOS.inScheme, crm.CreditRiskModeling))

# Add associative relationship between performing and non-performing variants
g.add((crm.LossGivenDefaultForPerforming, SKOS.related, crm.LossGivenDefaultForNonPerforming))

# Add a large number of requirements as URIs only, linked to ProbabilityOfDefault
for i in range(1, 10001):
    req_uri = reg[f"Req{i}"]
    # Just link the requirement ID to ProbabilityOfDefault
    g.add((crm.ProbabilityOfDefault, crm.hasRequirement, req_uri))

# Print the resulting graph in Turtle format
print(g.serialize(format="turtle").decode("utf-8"))
