import os

class OutputFormatComplianceOracle:
    """
    Oracle for Output Format Compliance.
    Provides the list of JSON reports that should be evaluated.
    """

    def __init__(self, contract):
        self.contract = contract

    def list_all_json_reports(self, root: str):
        """
        Recursively lists all JSON reports under the output directory.
        """
        json_files = []
        for dirpath, _, filenames in os.walk(root):
            for f in filenames:
                if f.endswith(".json"):
                    json_files.append(os.path.join(dirpath, f))
        return json_files
