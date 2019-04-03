#
# Test farm vocabulary method
#

def test_get_all_vocabularies(test_farm):
    vocabs = test_farm.vocabulary()

    assert len(vocabs) > 0
    assert 'vid' in vocabs[0]
    assert 'name' in vocabs[0]

def test_get_single_vocabulary_by_machine_name(test_farm):
    vocabs = test_farm.vocabulary('farm_crops')

    assert 'vid' in vocabs[0]
    assert 'name' in vocabs[0]
