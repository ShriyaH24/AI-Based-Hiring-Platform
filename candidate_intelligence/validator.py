from jsonschema import validate


class CandidateValidator:

    def __init__(self, schema):
        self.schema = schema

    def validate_candidate(self, candidate):

        validate(
            instance=candidate,
            schema=self.schema
        )

        return True