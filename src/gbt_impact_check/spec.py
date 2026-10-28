"""The capability contract, copied verbatim from the GBT V8 registry.

Do not hand-edit: ``tests/test_spec.py`` pins every field against the
registry snapshot so drift fails the build instead of shipping quietly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

_RAW = r"""{
 "name": "impact_check",
 "domain": "system",
 "desc": "**影响面检查（多域监控的读数面）**（主人令 2026-10-19：「修改一个地方的时候要分出触手关注跟这个修复的地方相连的所有地方，确保你修改其他地方不会被连带故障」）：读 `state/model-pack/wiring.json` 邻接图（现读 **6301 节点 / 951536 有向边 / 单连通分量 100%**），给一个目标（能力位名 / 代码路径 / 页面路径）就算出它 1~2 跳的影响面。**不是 selfscan**（那是框架五维自检），本位只管刀口宽度。op=status（图的规模·连通性·构建时间，取不到如实报 missing 不编 0）· op=impact（必填 target 或 targets，depth≤3 ⇒ 影响面构成 + **1 跳必验清单**；目标不在图里**如实拒绝**，绝不把空集当\"没影响\"）· op=risky（n ⇒ 按 1 跳邻居数排最危险的件，并如实标注\"本图不分强弱边\"）· op=where。**全部纯读免门**：不写盘、不出网、不起进程。已知读数：`code:gbt_allinone/api.py` 1 跳 = 337 个能力位 · depth=2 = 4859 节点 · `cap:tentacle_arm` 2 跳 = 342 节点",
 "handler": "impact_check",
 "safe": true,
 "external": false,
 "requires_params": true,
 "params": [
  "target"
 ],
 "params_hint": "target=要查的目标，如 code:gbt_allinone/api.py / cap:tentacle_arm / holo_pet_w3/omni-arm/index.html；**op=status / risky / where 不用传**；也可用 targets=[…] 一次查多处；depth 默认 2（上限 3）",
 "multi_op": true,
 "ops": [],
 "ops_hint": "target=要查的目标，如 code:gbt_allinone/api.py / cap:tentacle_arm / holo_pet_w3/omni-arm/index.html；**op=status / risky / where 不用传**；也可用 targets=[…] 一次查多处；depth 默认 2（上限 3）"
}"""


@dataclass(frozen=True)
class CapSpec:
    """Immutable description of one capability bit."""

    name: str
    domain: str
    desc: str
    handler: str
    safe: bool
    external: bool
    requires_params: bool
    params: Tuple[str, ...] = ()
    params_hint: str = ""
    multi_op: bool = False
    ops: Tuple[str, ...] = ()
    ops_hint: str = ""

    @property
    def gated(self) -> bool:
        """True when the registry marks this bit ``safe: false``.

        Gated does not mean "dangerous"; it means the action can change state
        that cannot be restored by running the inverse action.
        """
        return not self.safe

    @property
    def summary(self) -> str:
        """First clause of the description, for one-line listings."""
        for sep in ("\uff08", "\uff1b", "\u3002", ";"):
            if sep in self.desc:
                head = self.desc.split(sep, 1)[0].strip()
                if head:
                    return head
        return self.desc.strip()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "desc": self.desc,
            "handler": self.handler,
            "safe": self.safe,
            "gated": self.gated,
            "external": self.external,
            "requires_params": self.requires_params,
            "params": list(self.params),
            "params_hint": self.params_hint,
            "multi_op": self.multi_op,
            "ops": list(self.ops),
            "ops_hint": self.ops_hint,
        }


_data = json.loads(_RAW)

SPEC = CapSpec(
    name=_data["name"],
    domain=_data["domain"],
    desc=_data["desc"],
    handler=_data["handler"],
    safe=_data["safe"],
    external=_data["external"],
    requires_params=_data["requires_params"],
    params=tuple(_data["params"]),
    params_hint=_data["params_hint"],
    multi_op=_data["multi_op"],
    ops=tuple(_data["ops"]),
    ops_hint=_data["ops_hint"],
)
