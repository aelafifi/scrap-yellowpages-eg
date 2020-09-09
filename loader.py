from neo4j import GraphDatabase
from json import loads

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123"))

ignore_ids = []

def save_record(tx, record):
    global ignore_ids

    if record['id'] in ignore_ids:
        return

    ignore_ids.extend(record['branches'])

    tx.run("MERGE (company:Company {id: $id}) "
        "ON CREATE SET company.title = $title, company.address = $address",
        id=record['id'], title=record['title'], address=record['address'])

    for cat in record['categories']:
        tx.run("MERGE (cat:Category {title: $title})", title=cat)

        tx.run("MATCH (company:Company {id: $id}), (cat:Category {title: $title}) "
            "MERGE (cat)-[:CONTAINS]->(company)",
            id=record['id'], title=cat)


with driver.session() as session:
    for line in open("yp.json"):
        record = loads(line)
        session.write_transaction(save_record, record)
