import json
from typing import Any, Dict, List

import pip_audit.service as service

from .interface import VulnerabilityFormat


class JsonFormat(VulnerabilityFormat):
    def __init__(self, output_desc: bool):
        self.output_desc = output_desc

    def format(self, result: Dict[service.Dependency, List[service.VulnerabilityResult]]) -> str:
        output_json = []
        for dep, vulns in result.items():
            output_json.append(self._format_dep(dep, vulns))
        return json.dumps(output_json)

    def _format_dep(
        self, dep: service.Dependency, vulns: List[service.VulnerabilityResult]
    ) -> Dict[str, Any]:
        return {
            "package": dep.package,
            "version": str(dep.version),
            "vulns": [self._format_vuln(vuln) for vuln in vulns],
        }

    def _format_vuln(self, vuln: service.VulnerabilityResult) -> Dict[str, Any]:
        vuln_json = {
            "id": vuln.id,
            "fix_versions": [str(version) for version in vuln.fix_versions],
        }
        if self.output_desc:
            vuln_json["description"] = vuln.description
        return vuln_json