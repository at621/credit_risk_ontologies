from rdflib import Graph, Namespace, RDF, Literal, SKOS
import os

# Define Namespaces
CRM = Namespace("http://example.org/crm#")
REG = Namespace("http://example.org/regulations#")
# You can add more namespaces if needed

# Initialize the RDF Graph
g = Graph()
g.bind("crm", CRM)
g.bind("reg", REG)
g.bind("skos", SKOS)

# ----------------------------
# 1. Define the Concept Scheme
# ----------------------------
g.add((CRM.CreditRiskModeling, RDF.type, SKOS.ConceptScheme))
g.add((CRM.CreditRiskModeling, SKOS.prefLabel, Literal("Credit Risk Modeling")))
g.add((CRM.CreditRiskModeling, SKOS.definition, Literal(
    "A domain dealing with the estimation, analysis, and quantification of the risk of loss due to a borrower’s default."
)))

# ----------------------------
# 2. Define Top-Level Concepts
# ----------------------------
# Top Concept: Credit Risk Model
g.add((CRM.CreditRiskModel, RDF.type, SKOS.Concept))
g.add((CRM.CreditRiskModel, SKOS.prefLabel, Literal("Credit Risk Model")))
g.add((CRM.CreditRiskModel, SKOS.definition, Literal(
    "A conceptual or mathematical framework to estimate the probability and severity of loss from a counterparty default."
)))
g.add((CRM.CreditRiskModel, SKOS.topConceptOf, CRM.CreditRiskModeling))
g.add((CRM.CreditRiskModel, SKOS.inScheme, CRM.CreditRiskModeling))

# ----------------------------
# 3. Define Narrower Concepts
# ----------------------------
# Probability of Default (PD)
g.add((CRM.ProbabilityOfDefault, RDF.type, SKOS.Concept))
g.add((CRM.ProbabilityOfDefault, SKOS.prefLabel, Literal("Probability of Default")))
g.add((CRM.ProbabilityOfDefault, SKOS.definition, Literal(
    "The likelihood that a borrower will fail to meet its debt obligations within a given time horizon."
)))
g.add((CRM.ProbabilityOfDefault, SKOS.broader, CRM.CreditRiskModel))
g.add((CRM.ProbabilityOfDefault, SKOS.inScheme, CRM.CreditRiskModeling))

# Loss Given Default (LGD)
g.add((CRM.LossGivenDefault, RDF.type, SKOS.Concept))
g.add((CRM.LossGivenDefault, SKOS.prefLabel, Literal("Loss Given Default")))
g.add((CRM.LossGivenDefault, SKOS.definition, Literal(
    "The fraction of an exposure that is lost if a default occurs."
)))
g.add((CRM.LossGivenDefault, SKOS.broader, CRM.CreditRiskModel))
g.add((CRM.LossGivenDefault, SKOS.inScheme, CRM.CreditRiskModeling))

# Exposure at Default (EAD)
g.add((CRM.ExposureAtDefault, RDF.type, SKOS.Concept))
g.add((CRM.ExposureAtDefault, SKOS.prefLabel, Literal("Exposure at Default")))
g.add((CRM.ExposureAtDefault, SKOS.definition, Literal(
    "The amount of exposure owed by a borrower at the moment of default."
)))
g.add((CRM.ExposureAtDefault, SKOS.broader, CRM.CreditRiskModel))
g.add((CRM.ExposureAtDefault, SKOS.inScheme, CRM.CreditRiskModeling))

# Risk Weight
g.add((CRM.RiskWeight, RDF.type, SKOS.Concept))
g.add((CRM.RiskWeight, SKOS.prefLabel, Literal("Risk Weight")))
g.add((CRM.RiskWeight, SKOS.definition, Literal(
    "A regulatory measure expressing the relative riskiness of a credit exposure, used to calculate capital requirements."
)))
g.add((CRM.RiskWeight, SKOS.broader, CRM.CreditRiskModel))
g.add((CRM.RiskWeight, SKOS.inScheme, CRM.CreditRiskModeling))

# ----------------------------
# 4. Define Subcategories for LGD
# ----------------------------
# LGD for Performing Exposures
g.add((CRM.LossGivenDefaultForPerforming, RDF.type, SKOS.Concept))
g.add((CRM.LossGivenDefaultForPerforming, SKOS.prefLabel, Literal("Loss Given Default for Performing Exposures")))
g.add((CRM.LossGivenDefaultForPerforming, SKOS.definition, Literal(
    "LGD applied specifically to exposures currently meeting obligations on time."
)))
g.add((CRM.LossGivenDefaultForPerforming, SKOS.broader, CRM.LossGivenDefault))
g.add((CRM.LossGivenDefaultForPerforming, SKOS.inScheme, CRM.CreditRiskModeling))

# LGD for Non-Performing Exposures
g.add((CRM.LossGivenDefaultForNonPerforming, RDF.type, SKOS.Concept))
g.add((CRM.LossGivenDefaultForNonPerforming, SKOS.prefLabel, Literal("Loss Given Default for Non-Performing Exposures")))
g.add((CRM.LossGivenDefaultForNonPerforming, SKOS.definition, Literal(
    "LGD applied specifically to exposures that are delinquent or in default."
)))
g.add((CRM.LossGivenDefaultForNonPerforming, SKOS.broader, CRM.LossGivenDefault))
g.add((CRM.LossGivenDefaultForNonPerforming, SKOS.inScheme, CRM.CreditRiskModeling))

# Associative Relationship between LGD Subcategories
g.add((CRM.LossGivenDefaultForPerforming, SKOS.related, CRM.LossGivenDefaultForNonPerforming))

# ----------------------------
# 5. Associate Regulatory Requirements
# ----------------------------
# Custom Property: hasRequirement
# Define it as a property if not already defined
g.add((CRM.hasRequirement, RDF.type, RDF.Property))
g.add((CRM.hasRequirement, SKOS.prefLabel, Literal("has requirement")))
g.add((CRM.hasRequirement, SKOS.definition, Literal(
    "Associates a regulatory requirement with a credit risk modeling concept."
)))

# Example: Link all requirements to Probability of Default (PD)
# You can change the association logic as per your needs
for i in range(1, 10001):
    req_uri = REG[f"Req{i}"]
    g.add((CRM.ProbabilityOfDefault, CRM.hasRequirement, req_uri))

# ----------------------------
# 6. Save the RDF Graph to a File
# ----------------------------
# Define the output directory and file name
output_dir = "output_rdf"
output_file = "credit_risk_modeling.ttl"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Full path to the output file
file_path = os.path.join(output_dir, output_file)

# Serialize the graph to Turtle format and save to the file
g.serialize(destination=file_path, format="turtle")

print(f"RDF graph has been successfully saved to {file_path}")
