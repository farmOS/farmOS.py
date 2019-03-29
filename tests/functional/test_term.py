#
# Test farm taxonomy term methods
#

def test_get_all_taxonomy_terms(test_farm):
    terms = test_farm.term.get()

    assert len(terms) > 0

def test_get_farm_terms_filtered_by_single_vocabulary_name(test_farm):
    vocabulary_name = 'farm_crops'

    terms = test_farm.term.get(vocabulary_name)

    assert len(terms) > 0
    # Assert all terms retrieved are from the same vocabulary
    # (cannot check vocabulary name in response)
    assert terms[0]['vocabulary']['id'] == terms[1]['vocabulary']['id']

def test_get_farm_terms_filtered_by_single_vocabulary_tid(test_farm):
    vocabulary_tid = 7

    term = test_farm.term.get(vocabulary_tid)

    assert 'vocabulary' in term
    assert int(term['tid']) == vocabulary_tid

def test_get_farm_term_filtered_by_multiple_vocabulary(test_farm):
    vocabulary_name = 'farm_crops'
    term_name = 'Spinach'

    term = test_farm.term.get({
        'bundle':vocabulary_name,
        'name':term_name
    })

    assert 'name' in term[0]
    assert term[0]['name'] == term_name
