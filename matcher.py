from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "123"))


THRESHOLD = 95.0


with driver.session() as session:
    counts = {}

    result = session.run("MATCH (c1:Category)-[:CONTAINS]->(c:Company) "
                         "RETURN c1.title AS title, count(c) AS _count")
    for record in result:
        counts[record['title']] = record['_count']

    result = session.run("MATCH (c1:Category)-[:CONTAINS]->(c:Company)<-[:CONTAINS]-(c2:Category) "
                         "WHERE c1 < c2 "
                         "RETURN c1.title AS c1_title, c2.title AS c2_title, count(c) AS _count")
    records = []
    for record in result:
        rec = dict(record)
        rec['c1_count'] = counts[rec['c1_title']]
        rec['c2_count'] = counts[rec['c2_title']]
        rec['c1_perc'] = rec['_count'] * 100 / counts[rec['c1_title']]
        rec['c2_perc'] = rec['_count'] * 100 / counts[rec['c2_title']]
        records.append(rec)

    for rec in records:
        if rec['c1_perc'] >= THRESHOLD or rec['c2_perc'] >= THRESHOLD:
            print(f"{rec['c1_title']} ({rec['_count']}/{rec['c1_count']}) [{rec['c1_perc']}]")
            print(f"{rec['c2_title']} ({rec['_count']}/{rec['c2_count']}) [{rec['c2_perc']}]")
            print()
