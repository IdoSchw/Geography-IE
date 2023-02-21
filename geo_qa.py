import rdflib

def geo_qa(question):
  g = rdflib.Graph()
  g.parse("graph.nt", format = "nt")
  g.serialize("graph.nt", format="nt")   # Saving the Ontology to file. Is that needed?

  # need to parse the question?
  # Queries
  question_arr = question.split()
  
  country_inx = question_arr.index("of") + 1
  country = "".join(question_arr[country_inx:])[:-1] # taking the last word(the country) without the "?"
                                    # for questions 1-4, 6
  # 1. Who is the president of <country>?
  if ("Who is the president of" in question):
    q = "select ?president WHERE" \
          "{ ?president <president_of> <" + country + "> }"

  
  # 2. Who is the prime minister of <country>?
  if ("Who is the prime minister of" in question):
    q = "SELECT ?prime WHERE" \
          "{ ?prime <prime_minister_of> <" + country + "> }"

  # 3. What is the population of <country>?
  if ("population" in question):
    q = "SELECT ? p WHERE" \
          "{ ?p <population of> <" + country + "> }"

  # 4. What is the area of <country>?
  if ("area" in question):
    q = "SELECT ?a WHERE" \
          "{ ?a <area of> <" + country + "> }"

  # 5. What is the form of government in <country>?
  if ("government" in question):
    country_inx = question_arr.index("in") + 1
    country = "".join(question_arr[country_inx:])[:-1]
    q = "SELECT ?form WHERE" \
          "{ ?form <government_form_of> <" + country + "> }"

  # 6. What is the capital of <country>?
  if ("capital" in question):
    q = "SELECT ?capital WHERE" \
          "{ ?capital <capital_of> <" + country + "> }"

  
  country = "".join(question_arr[country_inx:]) # storing the country str in a variable, for questions 7-10
                                                    #check it doesn't include the last word ("born")
  # 7. When was the president of <country> born?
  if ("When was the president" in question):
    q = "SELECT ?date WHERE" \
          "{ ?president <president_of> <" + country + "> ." \
            " ?president <birth_date> ?date }"

  # 8. Where was the president of <country> born?
  if ("Where was the president" in question):
    q = "SELECT ?place WHERE" \
        "{ ?president <president_of> <" + country + "> ." \
          " ?president <birth_place> ?place }"

  # 9. When was the prime minister of <country> born?
  if ("When was the prime minister" in question):
    q = "SELECT ?date WHERE" \
          "{ ?prime <prime_minister_of> <" + country + "> ." \
            " ?prime <birth_date> ?date }"

  # 10. Where was the prime minister of <country> born?
  if ("Where was the president" in question):
    q = "SELECT ?place WHERE" \
        "{ ?prime <prime_minister_of> <" + country + "> ." \
          " ?prime <birth_place> ?place }"

  # 11. Who is <entity>?
  if ("Who" in question):
    entity_inx = question_arr.index("is") + 1
    entity = "".join(question_arr[entity_inx:])[:-1]
    q = "SELECT ?title WHERE" \
          "{ ?title <title_of> <" + entity + "> }"

  # 12. How many <government_form1> are also <government_form2>?
  if ("How many" in question and "are also" in question):
    many_inx = question_arr.index("many")
    are_inx = question_arr.index("are")
    government_form1 = "".join(question_arr[many_inx + 1: are_inx])
    government_form2 = "".join(question_arr[are_inx + 2: ])[:-1]
    # q = "SELECT COUNT(DISTINCT ?country) WHERE" \
    #       "{ ?country <government_form> <" + government_form1 + "> . " \
    #         " ?country <government_form> <" + government_form2 + "> }"
    q = "SELECT COUNT(DISTINCT ?country) WHERE" \
          "{ <" + government_form1 + "> <government_form_of> ?country . " \
            " <" + government_form2 + "> <government_form_of> ?country }" \
              "ORDER BY ?country"

  # 13. List all countries whose capital name contains the string <str>
  if ("List" in question):
    sub_str = question_arr[-1]
    q = "SELECT DISTINCT ?country WHERE" \
          "{ ?capital <capital_of> ?country ." \
            "FILTER regex(str(?capital), " + sub_str +") }"

  country_inx = question_arr.index("in") + 1
  country = "".join(question_arr[country_inx:])[:-1] # taking the last word(the country) without the "?"
  # 14. How many presidents were born in <country>?
  if ("How many" in question and "were" in question):
    q = "SELECT COUNT(DISTINCT ?president) WHERE" \
          "?president <birth_place> <" + country + "> }"

  #15. What is the driving side of <country>?
  if ("side" in question):
    q = "SELECT ?side WHERE" \
          "{ ?side <driving_side_of> <" + country + "> }"

  x = g.query(q)
  for result in x:
      print(result)

question = "What is the capital of Vietnam?"
# question_arr = question.split()
# country_inx = question_arr.index("of") + 1
# country = "".join(question_arr[country_inx:])[:-1]
# print(country)
geo_qa(question)