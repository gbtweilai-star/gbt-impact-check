# impact_check

**One capability bit from GBT V8, packaged standalone.** No. 266 of 341,
`system` domain (System).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> **影响面检查（多域监控的读数面）**（主人令 2026-10-19：「修改一个地方的时候要分出触手关注跟这个修复的地方相连的所有地方，确保你修改其他地方不会被连带故障」）：读 `state/model-pack/wiring.json` 邻接图（现读 **6301 节点 / 951536 有向边 / 单连通分量 100%**），给一个目标（能力位名 / 代码路径 / 页面路径）就算出它 1~2 跳的影响面。**不是 selfscan**（那是框架五维自检），本位只管刀口宽度。op=status（图的规模·连通性·构建时间，取不到如实报 missing 不编 0）· op=impact（必填 target 或 targets，depth≤3 ⇒ 影响面构成 + **1 跳必验清单**；目标不在图里**如实拒绝**，绝不把空集当"没影响"）· op=risky（n ⇒ 按 1 跳邻居数排最危险的件，并如实标注"本图不分强弱边"）· op=where。**全部纯读免门**：不写盘、不出网、不起进程。已知读数：`code:gbt_allinone/api.py` 1 跳 = 337 个能力位 · depth=2 = 4859 节点 · `cap:tentacle_arm` 2 跳 = 342 节点

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-impact-check.git
cd gbt-impact-check
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_impact_check info                  # capability card
python -m gbt_impact_check spec --json           # machine-readable contract
python -m gbt_impact_check check --payload '{"target": "<在此填写>"}'
python -m gbt_impact_check run   --payload '{"target": "<在此填写>"}'
```

Real `info` output from this machine:

```text
impact_check  (system)  v1.0.0
----------------------------------------
**影响面检查（多域监控的读数面）**（主人令 2026-10-19：「修改一个地方的时候要分出触手关注跟这个修复的地方相连的所有地方，确保你修改其他地方不会被连带故障」）：读 `state/model-pack/wiring.json` 邻接图（现读 **6301 节点 / 951536 有向边 / 单连通分量 100%**），给一个目标（能力位名 / 代码路径 / 页面路径）就算出它 1~2 跳的影响面。**不是 selfscan**（那是框架五维自检），本位只管刀口宽度。op=status（图的规模·连通性·构建时间，取不到如实报 missing 不编 0）· op=impact（必填 target 或 targets，depth≤3 ⇒ 影响面构成 + **1 跳必验清单**；目标不在图里**如实拒绝**，绝不把空集当"没影响"）· op=risky（n ⇒ 按 1 跳邻居数排最危险的件，并如实标注"本图不分强弱边"）· op=where。**全部纯读免门**：不写盘、不出网、不起进程。已知读数：`code:gbt_allinone/api.py` 1 跳 = 337 个能力位 · depth=2 = 4859 节点 · `cap:tentacle_arm` 2 跳 = 342 节点

gated      : False
external   : False
multi-op   : True
params     : target
             target=要查的目标，如 code:gbt_allinone/api.py / cap:tentacle_arm / holo_pet_w3/omni-arm/index.html；**op=status / risky / where 不用传**；也可用 targets=[…] 一次查多处；depth 默认 2（上限 3）
values     : (multi-op, but the registry does not enumerate them)
```

Wire a real implementation:

```python
from gbt_impact_check import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({"target": "<在此填写>"}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| `target` | yes | declared required by the registry |

Registry hint (`params_hint`): target=要查的目标，如 code:gbt_allinone/api.py / cap:tentacle_arm / holo_pet_w3/omni-arm/index.html；**op=status / risky / where 不用传**；也可用 targets=[…] 一次查多处；depth 默认 2（上限 3）

**注册表标注 `multi_op: true`，但没有枚举具体取值。**本包不替它编造取值清单——这种缺口应当在注册表源头补，而不是在文档里圆。

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Not gated: the registry marks this bit `safe: true`.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
22 passed, 1 skipped in 0.11s
```

## Provenance

| field | value |
|---|---|
| capability | `impact_check` |
| domain | `system` |
| handler | `impact_check` |
| safe | `True` (gated = `False`) |
| external | `False` |
| atlas page | [system/impact_check](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/system/impact_check.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
