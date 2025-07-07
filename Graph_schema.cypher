
// --- Create Courses ---
CREATE (:Course {code: 'CS101', name: 'Intro to CS'}),
       (:Course {code: 'CS102', name: 'Data Structures'}),
       (:Course {code: 'CS103', name: 'Discrete Math'}),
       (:Course {code: 'CS201', name: 'Algorithms'}),
       (:Course {code: 'CS202', name: 'Computer Architecture'}),
       (:Course {code: 'CS203', name: 'Databases'}),
       (:Course {code: 'CS204', name: 'Operating Systems'}),
       (:Course {code: 'CS301', name: 'AI'}),
       (:Course {code: 'CS302', name: 'Machine Learning'}),
       (:Course {code: 'CS303', name: 'Security Fundamentals'}),
       (:Course {code: 'CS304', name: 'Data Science'}),
       (:Course {code: 'CS305', name: 'Web Development'}),
       (:Course {code: 'CS306', name: 'Cloud Computing'}),
       (:Course {code: 'CS307', name: 'Cybersecurity'});

// --- Add Prerequisites ---
MATCH (a:Course {code: 'CS101'}), (b:Course {code: 'CS102'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS102'}), (b:Course {code: 'CS201'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS102'}), (b:Course {code: 'CS202'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS102'}), (b:Course {code: 'CS203'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS202'}), (b:Course {code: 'CS204'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS201'}), (b:Course {code: 'CS301'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS201'}), (b:Course {code: 'CS302'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS203'}), (b:Course {code: 'CS302'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS102'}), (b:Course {code: 'CS303'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS302'}), (b:Course {code: 'CS304'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS102'}), (b:Course {code: 'CS305'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS204'}), (b:Course {code: 'CS306'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS305'}), (b:Course {code: 'CS306'}) CREATE (a)-[:PREREQUISITE]->(b);
MATCH (a:Course {code: 'CS303'}), (b:Course {code: 'CS307'}) CREATE (a)-[:PREREQUISITE]->(b);

// --- Create Topics ---
CREATE (:Topic {name: 'AI'}),
       (:Topic {name: 'Security'}),
       (:Topic {name: 'Data Science'}),
       (:Topic {name: 'Software'}),
       (:Topic {name: 'Systems'});

// --- Link Courses to Topics ---
MATCH (c:Course {code: 'CS301'}), (t:Topic {name: 'AI'}) CREATE (c)-[:RELATED_TO]->(t);
MATCH (c:Course {code: 'CS302'}), (t:Topic {name: 'AI'}) CREATE (c)-[:RELATED_TO]->(t);
MATCH (c:Course {code: 'CS303'}), (t:Topic {name: 'Security'}) CREATE (c)-[:RELATED_TO]->(t);
MATCH (c:Course {code: 'CS304'}), (t:Topic {name: 'Data Science'}) CREATE (c)-[:RELATED_TO]->(t);
MATCH (c:Course {code: 'CS305'}), (t:Topic {name: 'Software'}) CREATE (c)-[:RELATED_TO]->(t);
MATCH (c:Course {code: 'CS204'}), (t:Topic {name: 'Systems'}) CREATE (c)-[:RELATED_TO]->(t);
