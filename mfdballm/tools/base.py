class Tool:

    name = ""
    description = ""
    schema = {}

    def run(self, **kwargs):
        raise NotImplementedError
