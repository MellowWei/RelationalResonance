# Relational Resonance Engine (RRE)

一个可独立运行的「关系共振/意义动力学」小引擎：  
- 事件数据（JSONL）  
- 6个独立模型（SPW / Trigger / Phase / Witness / MDI / Temporal Compression）  
- 可视化（热力图、时间线、相位时间线）  
- 概率预测（P2_next_7d / SPW_next_7d / Stability_30d）

## 快速开始

```bash
python analysis/run_all.py
```

输出：
- `analysis/_scores.json`（每个事件的模型分数）
- `analysis/_out/*.png`（图表：timeline、phase、heatmap）
- `analysis/_prediction.json`（概率预测）

## 数据输入

编辑：`data/events.jsonl`  
每行一个事件 JSON（字段缺失会自动视为 0 或 null）

推荐字段：
- `event_id`, `time`, `actors`, `channel`
- `motifs`, `language_markers`
- `affect`: `{awe, safety, depth, arousal}`
- `context`: `{gap_days, substance, non_control, return_pattern, novelty, identity_shift}`

## 命名建议

这个系统更准确叫：
- **Relational Resonance Engine (RRE)** / **Relational Meaning Dynamics (RMDM)**  
而不是字面“前世今生”。
