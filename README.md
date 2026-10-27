# StarRocks Skills

45 Claude skills for operating, tuning and troubleshooting StarRocks (3.0–3.5, some notes for 2.5 and 4.0), plus shared guides, references and scripts.

The folder combines two skill families:

| Family | Skills | Style | Supporting files |
| --- | --- | --- | --- |
| Troubleshooting (debug) | 13 | Symptom-driven runbooks: confirm → locate bottleneck → act by cause | `references/` with 30 real incident cases, `scripts/analyze_logs.py` |
| Admin, design, optimization | 32 | Topic reference guides: DDL, config, SQL, Python helpers | Single `SKILL.md` each |

Skills assume shell access to FE/BE hosts (logs, `curl` on BE HTTP ports, `jstack`) and a MySQL-protocol SQL client.

## Where to start

| Symptom or task | First skill | Then / also |
| --- | --- | --- |
| Host CPU near 100% | `starrocks_cpu_saturation` (triage) | `query`, `import`, `compaction`, `node` |
| Slow, hanging or wrong query | `starrocks_query` | `explain_plan`, `query_optimizer`, `join_optimization`, `cbo` |
| Load slow, timing out, RPC failed | `starrocks_import` | `stream_load`, `broker_load`, `routine_load_kafka` |
| "too many versions", compaction score > 100 | `starrocks_compaction` | `tablet`, `admin_compaction` |
| BE OOM/crash, FE deadlock or Full GC | `starrocks_node` | `memory_tuning` |
| FE/BE won't start | `starrocks_deployment` | `admin_security` |
| Missing replicas, stuck decommission, disk skew | `starrocks_balance` | `admin_storage_balancer`, `tablet` |
| Async MV refresh failing / no rewrite | `starrocks_materialized_view` | `materialized_views` |
| Hive/Iceberg/S3 catalog errors | `starrocks_data_lake` | `lakehouse_integration`, `files_ingestion` |
| Shared-data (S3, DataCache) cluster | `shared_data` | — |
| High QPS, latency spikes under load | `starrocks_high_concurrency` | `concurrency_optimizer` |
| Runaway query, resource groups, queue full | `starrocks_resource_isolation` | `admin_query_monitor` |
| Daily health check | `starrocks_admin_cluster_health` | `self_healing`, `data_quality_guardian` |
| Designing tables | `starrocks_data_modeling` | `ddl_table_types`, `partitioning`, `bucketing` |

For problems spanning several areas, read `starrocks_guides/` first.

## Troubleshooting skills (13)

| Folder | Use when | References |
| --- | --- | --- |
| `starrocks_query` | Queries slow, hanging or wrong; profile analysis, scan skew, MERGE time, runtime filters | 3 refs, case 014, `analyze_logs.py` |
| `starrocks_import` | Stream/Broker/Routine Load, INSERT, Flink connector slow or failing; publish timeout, RPC failed | 6 refs, cases 001, 002, 017, 018 |
| `starrocks_node` | BE OOM/crash, FE deadlock, Full GC, FE heap growth | 15 refs, cases 003, 007, 008, 021–031, `analyze_logs.py` |
| `starrocks_compaction` | Score > 100, "too many versions", high MERGE time (shared-nothing) | 2 refs, case 014 |
| `starrocks_cpu_saturation` | First stop for high CPU; attributes load then hands off | 1 ref, `analyze_logs.py` |
| `starrocks_tablet` | Data skew, version count, error replicas, over-sharding | 4 refs, cases 004, 019 |
| `starrocks_balance` | Missing replicas, clone failures, balance speed, stuck decommission, colocate | Decommission checklist |
| `starrocks_materialized_view` | Async MV refresh fails, times out, goes inactive, rewrite misses | 4 refs, case 012 |
| `starrocks_data_lake` | External catalog failures: HMS, Kerberos, S3 throttling/SSL, cache TTL | Cases 006, 016 |
| `shared_data` | Shared-data clusters: DataCache, S3 multipart/503, FE leader switch | 5 refs, cases 009–011, 013 |
| `starrocks_deployment` | FE/BE won't start: ports, dirs, priority_networks, clock drift, BDB, SSL | 4 refs, cases 005, 020 |
| `starrocks_high_concurrency` | High QPS, throughput plateaus, latency spikes | Case 015 |
| `starrocks_resource_isolation` | Resource groups, query queues, big-query breakers, SQL blacklist | 2 refs |

## Admin, design and optimization skills (32)

| Area | Folders (prefix `starrocks_` omitted) |
| --- | --- |
| Administration | `admin_cluster_health`, `admin_compaction`, `admin_query_monitor`, `admin_security`, `admin_storage_balancer`, `admin_backup_restore` |
| Data modeling | `data_modeling`, `ddl_table_types`, `partitioning`, `bucketing`, `schema_evolution`, `realtime_modeling`, `medallion_architecture` |
| Query performance | `query_optimizer`, `explain_plan`, `join_optimization`, `aggregation_optimizer`, `cbo`, `concurrency_optimizer`, `memory_tuning`, `materialized_views` |
| Ingestion | `stream_load`, `broker_load`, `routine_load_kafka`, `files_ingestion`, `cdc_pipeline`, `lakehouse_integration`, `realtime_analytics` |
| Automation | `ai_incident_rca`, `ai_query_autotuner`, `self_healing`, `data_quality_guardian` |

See each `SKILL.md` frontmatter `description` for full scope.

## Shared material

| Folder | Contents |
| --- | --- |
| `starrocks_guides/` | `cascade-cluster-degradation.md` (compaction backlog → slow imports → BE OOM → FE deadlock), `cascade-import-rpc-failed.md` (statistics collection starves BRPC → imports fail) |
| `starrocks_references/` | `01-common-commands.md`: log grep patterns and cluster status commands used by all troubleshooting skills |
| `starrocks_scripts/` | `install.sh` (install to Claude Code, Cursor, JetBrains), `skill_converter.py` (verify/convert; needs Python 3.6+ and PyYAML) |

`analyze_logs.py` (in `starrocks_query`, `starrocks_node`, `starrocks_cpu_saturation` under `scripts/`) ranks top N queries in an FE audit log:

```bash
python3 scripts/analyze_logs.py "2025-04-15 00:00:00" "2025-04-15 01:00:00" "MemCostBytes" 3 fe.audit.log
# fields: MemCostBytes | QueryFEAllocatedMemory | CpuCostNs | ScanBytes | ScanRows
```

## Install

```bash
./starrocks_scripts/install.sh --tool claude-code --target ~/.claude/skills/
./starrocks_scripts/install.sh --tool cursor --target .cursor/rules/
./starrocks_scripts/install.sh --tool all --target .
```

## Known issues

- **Overlapping skills:** `materialized_view`/`materialized_views`, `compaction`/`admin_compaction`, `balance`/`admin_storage_balancer`, `high_concurrency`/`concurrency_optimizer`, `query`/`query_optimizer`/`explain_plan`, `resource_isolation`/`admin_query_monitor`, `data_lake`/`lakehouse_integration`/`files_ingestion`, `node`/`memory_tuning`.
- **Broken cross-links:** skills link to the original layout (`../import/SKILL.md`, `guides/`, `references/01-common-commands.md`); folders are now `starrocks_*`.
- `starrocks_scripts/README.md` lists `analyze_logs.py`, but no copy exists there.
- `skill_converter.py` only knows the 13 troubleshooting categories.
- Some skills reference skills not in this repo (`trino_iceberg`, `apache_kafka`, `apache_flink`, `cdc_debezium`, `airflow_dags`, `pyspark_streaming`).
- Folder names don't match frontmatter `name` fields.
- The 32 admin skills have keyword-list descriptions without a "Use when…" trigger.
