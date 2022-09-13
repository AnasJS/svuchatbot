from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

# First, we need to load a morphological database.
# Here, we load the default database which is used for analyzing
# Modern Standard Arabic.


def camel_based_morphology_analysing(sent):
    db = MorphologyDB.builtin_db()

    analyzer = Analyzer(db)

    analyses = analyzer.analyze('موظف')
    return analyses