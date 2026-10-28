# impact_check · 系统域能力位

> **用途一句话**：**影响面检查

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
<img alt="capability" src="https://img.shields.io/badge/capability-266%20%2F%20341-orange">
</p>

这是 **GBT V8 的 341 个原生能力位中的第 266 个**（系统域 · `system`），
单独抽出来做成的独立仓库：可安装、可测试、零运行时依赖。

---

## 一、这一位是什么

> **影响面检查（多域监控的读数面）**（主人令 2026-10-19：「修改一个地方的时候要分出触手关注跟这个修复的地方相连的所有地方，确保你修改其他地方不会被连带故障」）：读 `state/model-pack/wiring.json` 邻接图（现读 **6301 节点 / 951536 有向边 / 单连通分量 100%**），给一个目标（能力位名 / 代码路径 / 页面路径）就算出它 1~2 跳的影响面。**不是 selfscan**（那是框架五维自检），本位只管刀口宽度。op=status（图的规模·连通性·构建时间，取不到如实报 missing 不编 0）· op=impact（必填 target 或 targets，depth≤3 ⇒ 影响面构成 + **1 跳必验清单**；目标不在图里**如实拒绝**，绝不把空集当"没影响"）· op=risky（n ⇒ 按 1 跳邻居数排最危险的件，并如实标注"本图不分强弱边"）· op=where。**全部纯读免门**：不写盘、不出网、不起进程。已知读数：`code:gbt_allinone/api.py` 1 跳 = 337 个能力位 · depth=2 = 4859 节点 · `cap:tentacle_arm` 2 跳 = 342 节点

上面这句是**注册表原文**，逐字复制，没有改写。`tests/test_spec.py` 会把它钉死——
描述漂移会让测试失败，而不是悄悄发版。

---

## 二、用途：它解决什么问题

### 2.1 这一域在管什么

agent 自身的运行面：谁在跑、跑过什么、花了多少、有没有偏。包含权限闸（action_gate / delivery_gate / figure_gate）、状态盘点（health / inventory / asset_index / caps_called_audit）、审计与漂移检测（coverage_auditor / project_drift / truth_scan / cross_scan）、以及调度与交接（orchestration_kernel / handoff / task_manager）。

### 2.2 为什么这么设计

系统域的价值不在「多一个监控面板」，而在于**让沉默的失败变成响亮的失败**。一个能力位如果不汇报自己没被调用过，它就等于不存在；所以这里大量能力位的产物是「差异报告」而不是「状态页」。

### 2.3 具体到 `impact_check`

**该用它的时候**：

- 你的任务可以概括为「**影响面检查」，并且
- 你手上已经有 `target` 这些参数，并且
- 你确认它是**可逆**动作（注册表 `safe: true`，不需要逐次授权）。

**不该用它的时候**：

- 你只是想要一个「大概能做这件事」的模糊入口 —— 这一位有明确契约，不是万能入口。
- 你需要它**替你做决定**。它执行，不做价值判断；要不要执行是调用方的事。
- 你希望它自带模型/密钥/机器。它不自带，见 4.5 节接后端。

---

## 三、安装

```bash
git clone https://github.com/gbtweilai-star/gbt-impact-check.git
cd gbt-impact-check
python -m pip install -e ".[dev]"
```

零运行时依赖，只有 `pytest` 是开发期依赖。

---

## 四、使用方式

### 4.1 看它是什么（人类可读）

```bash
python -m gbt_impact_check info
```

真实输出（本机捕获，非示意）：

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

### 4.2 看它的契约（机器可读）

```bash
python -m gbt_impact_check spec --json
```

输出是一个 JSON 对象，字段与注册表一一对应：`name` / `domain` / `desc` / `handler` /
`safe` / `gated` / `external` / `requires_params` / `params` / `params_hint` /
`multi_op` / `ops` / `ops_hint`。下游可以直接拿它做能力发现，不需要读文档。

### 4.3 只校验、不执行

```bash
python -m gbt_impact_check check --payload '{"target": "<在此填写>"}'
```

`check` 永远不会抛异常，只返回「哪里不满足契约」。适合在花掉一次模型调用之前，
先把缺的参数摆给用户看。退出码：`0` 通过、`1` 契约不满足、`2` JSON 本身不合法。

### 4.4 执行

```bash
python -m gbt_impact_check run --payload '{"target": "<在此填写>"}'
```

默认后端是 **stub**，所以你会拿到这样的信封：

```json
{
  "cap": "impact_check",
  "status": "validated",
  "backend": "stub",
  "data": { "executed": false, "reason": "no backend wired" },
  "note": "payload checked against the contract; nothing was executed."
}
```

注意 `status` 是 `"validated"` 而**不是** `"ok"`。这是刻意的：一个把 stub 报成成功的库，
会让调用方停止寻找真正的实现。`bool(result)` 对 stub 结果是 `False`。

### 4.5 接上你自己的后端

```python
from gbt_impact_check import SPEC, run

class MyBackend:
    name = "my-backend"

    def invoke(self, cap, payload):
        # 这里才是真实实现：调模型、调浏览器、调你的服务
        return {"cap": cap, "handled": sorted(payload)}

result = run({"target": "<在此填写>"}, backend=MyBackend())
assert result.status == "ok"      # 真实后端才会是 ok
print(result.as_dict())
```

也可以进程级注册一次，之后所有 `run()` 都走它：

```python
from gbt_impact_check.backend import register_backend
register_backend(MyBackend())
```

`Backend` 是一个 `Protocol`，只需要 `name` 属性和 `invoke(cap, payload) -> dict`。
不继承任何基类，你的实现不需要依赖本包。

### 4.6 作为库用

```python
from gbt_impact_check import SPEC, run
from gbt_impact_check.core import check

print(SPEC.name, SPEC.domain, SPEC.gated)

problems = check({"target": "<在此填写>"})
if problems:
    for p in problems:
        print("缺:", p)
else:
    print(run({"target": "<在此填写>"}).as_dict())
```

---

## 五、参数

| 参数 | 必填 | 说明 |
|---|---|---|
| `target` | 是 | 必填（注册表标注） |

> 注册表原话（`params_hint`）：target=要查的目标，如 code:gbt_allinone/api.py / cap:tentacle_arm / holo_pet_w3/omni-arm/index.html；**op=status / risky / where 不用传**；也可用 targets=[…] 一次查多处；depth 默认 2（上限 3）

**注册表标注 `multi_op: true`，但没有枚举具体取值。**本包不替它编造取值清单——这种缺口应当在注册表源头补，而不是在文档里圆。


**为什么表里只有「必填/否」两档**：注册表只标注了哪些参数是必填的，没有标注类型与取值范围。
本包没有替它编造类型 —— 编造出来的类型比没有类型更危险，因为调用方会相信它。

---

## 六、返回值

`run()` 返回一个不可变的 `Result`：

| 字段 | 类型 | 含义 |
|---|---|---|
| `cap` | `str` | 能力位名，恒等于 `impact_check` |
| `status` | `str` | `validated`（stub 校验通过）/ `ok`（真实后端执行）/ `error` |
| `backend` | `str` | 实际执行后端的 `name` |
| `data` | `dict` | 后端返回的原始字典 |
| `note` | `str` | 人类可读的补充说明（stub 会在这里说明自己没执行） |
| `elapsed_ms` | `float` | 后端耗时 |

`Result.as_dict()` 可直接 `json.dumps`。

---

## 七、边界与注意

- **多位一体**（注册表 `multi_op: true`）。同一个能力名下挂着多个子动作，调用前必须读清楚 `op` 的含义，否则「调对了能力、用错了动作」是最常见的误用。
- **缺参数直接拒绝**。`run()` 在严格模式下抛 `PayloadError`，而不是带着空参数去执行——空参数执行往往比报错更贵。
- **本包不含真实实现**。这是刻意设计：真实实现依附于原运行时（模型、密钥、机器）。本包发布的是契约、校验、CLI 与类型接缝；接上你自己的 `Backend` 就能跑。

---

## 八、它不会做什么

- **不会假装执行成功**。默认 stub 的 `status` 是 `validated`，`executed` 是 `false`。
- **不会替你决定要不要执行**。授权是人的动作，不是库的动作。
- **不会编造参数类型**。注册表没写的，本包也不写。
- **不会静默吞掉错误**。后端抛异常就往上抛，返回非 dict 就报 `CapError`。
- **不会联网**。零运行时依赖，`run()` 只调用你给的后端。

---

## 九、测试

```bash
python -m pytest
```

真实输出：

```text
22 passed, 1 skipped in 0.11s
```

测试里有一条**漂移守卫**：`test_description_is_verbatim` 把 `SPEC.desc` 与注册表快照逐字比对。
描述被改了一个字，构建立刻失败。

---

## 十、出处与核对

| 项 | 值 |
|---|---|
| 能力位名 | `impact_check` |
| 域 | `system`（系统域，共 341 位 / 30 域中的一位） |
| 注册表 handler | `impact_check` |
| `safe` | `True` → gated = `False` |
| `external` | `False` |
| `multi_op` | `True` |
| 索引页 | [system/impact_check](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/system/impact_check.md) |
| 全量图谱 | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

**关于 341 这个数**：父仓 README 写的是 348，但按 AST 解析注册表实际可枚举的是
`341 个能力位 + 0 个未实现 + 0 个已禁用 = 341`。差出来的 7 个是历史重名/已合并条目。
本仓库按 341 编号，编号与 `gbt-caps` 的索引一致，可逐条核对。

---

## License

MIT。见 [LICENSE](LICENSE)。
