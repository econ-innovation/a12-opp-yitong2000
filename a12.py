class Paper:
    def __init__(self, ut, year, journal, issn, doi, issue, volume):
        self.ut = ut
        self.year = year
        self.journal = journal
        self.issn = issn
        self.doi = doi
        self.issue = issue
        self.volume = volume

    def __str__(self):
        return f"{self.ut}, {self.year}, {self.journal}, {self.issn}, {self.doi}, {self.issue}, {self.volume}"

class Abstract:
    def __init__(self, ut, abstract):
        self.ut = ut
        self.abstract = abstract

    def __str__(self):
        return f"{self.ut}, {self.abstract}"

class Title:
    def __init__(self, ut, title):
        self.ut = ut
        self.title = title

    def __str__(self):
        return f"{self.ut}, {self.title}"

class Author:
    def __init__(self, ut, author_fullname, author_familyname, author_givenname, author_order):
        self.ut = ut
        self.author_fullname = author_fullname
        self.author_familyname = author_familyname
        self.author_givenname = author_givenname
        self.author_order = author_order

    def __str__(self):
        return f"{self.ut}, {self.author_fullname}, {self.author_familyname}, {self.author_givenname}, {self.author_order}"

class AuthorAffiliation:
    def __init__(self, ut, author_fullname, author_order, affiliation_address, affiliation_order):
        self.ut = ut
        self.author_fullname = author_fullname
        self.author_order = author_order
        self.affiliation_address = affiliation_address
        self.affiliation_order = affiliation_order

    def __str__(self):
        return f"{self.ut}, {self.author_fullname}, {self.author_order}, {self.affiliation_address}, {self.affiliation_order}"

class Reference:
    def __init__(self, ut, reference):
        self.ut = ut
        self.reference = reference

    def __str__(self):
        return f"{self.ut}, {self.reference}"

# 从文件中读取数据，创建对象
papers = []
abstracts = []
titles = []
authors = []
author_affiliations = []
references = []

with open("/Users/yitong/编程学习/bigdata/a12-opp-yitong2000/qje2014_2023.txt", "r") as file:
    paper_data = {}
    for line in file:
        tag, *data = line.strip().split(" ")
        if tag == "ER":
            if paper_data:
                paper = Paper(paper_data.get("UT", ""), paper_data.get("PY", ""), paper_data.get("SO", ""), paper_data.get("SN", ""), paper_data.get("DI", ""), paper_data.get("IS", ""), paper_data.get("VL", ""))
                papers.append(paper)
                if "AB" in paper_data:
                    abstract = Abstract(paper_data["UT"], " ".join(paper_data["AB"]))
                    abstracts.append(abstract)
                if "TI" in paper_data:
                    title = Title(paper_data["UT"], " ".join(paper_data["TI"]))
                    titles.append(title)
                if "AU" in paper_data:
                    for idx, author in enumerate(paper_data["AU"], start=1):
                        auth = Author(paper_data["UT"], author, "", "", idx)
                        authors.append(auth)
                if "AF" in paper_data:
                    for idx, aff in enumerate(paper_data["AF"], start=1):
                        aff_data = aff.split(";")
                        author, address = aff_data[0], aff_data[1]
                        auth_aff = AuthorAffiliation(paper_data["UT"], author, "", address, idx)
                        author_affiliations.append(auth_aff)
                if "CR" in paper_data:
                    for ref in paper_data["CR"]:
                        reference = Reference(paper_data["UT"], ref)
                        references.append(reference)
                paper_data = {}
        elif tag in paper_data:
            paper_data[tag].append(" ".join(data))
        else:
            paper_data[tag] = [" ".join(data)]

# 将信息输出至txt文件
def output_to_txt(objects, filename):
    with open(filename, "w") as file:
        for obj in objects:
            file.write(str(obj) + "\n")

output_to_txt(papers, "papers.txt")
output_to_txt(abstracts, "abstracts.txt")
output_to_txt(titles, "titles.txt")
output_to_txt(authors, "authors.txt")
output_to_txt(author_affiliations, "author_affiliations.txt")
output_to_txt(references, "references.txt")

