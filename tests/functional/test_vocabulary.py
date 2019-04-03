#
# Test farm vocabulary method
#

def test_get_all_vocabularies(test_farm):
    vocabs = test_farm.vocabulary()

    assert len(vocabs) > 0
    assert 'vid' in vocabs[0]
    assert 'name' in vocabs[0]
