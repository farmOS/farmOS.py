from farmOS.subrequests_model import Subrequest, SubrequestsBlueprint


def test_blueprint_root_validates_items_to_subrequests():
    blueprint = SubrequestsBlueprint(
        [
            {"action": "view", "endpoint": "api/log/observation", "requestId": "r1"},
            {"action": "create", "endpoint": "api/asset/animal", "body": {"a": 1}},
        ]
    )
    assert all(isinstance(item, Subrequest) for item in blueprint)
    assert blueprint[0].requestId == "r1"
