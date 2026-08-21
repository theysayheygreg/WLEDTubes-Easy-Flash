# Collaborator update — S3 Remote accepted build

- Tested source branch: `agent/s3-recovery-candidate`
- Exact HEAD: `10d7ac0d7e7f7407ba114195475111c74fe53629`
- Root fixes: stable node identity (F00); touch point-count release lifecycle; bounded 125 Hz polling cadence.
- Product/contract chain from Easy Flash pin: `45318507` → `54ed8ada` → `1bad186c` → `f64d1f09` → `4cd12103` → `10d7ac0d`; `fbeff278` adds bounded field diagnostics and is diagnostic-only.
- Contract: `usermods/Tubes/S3_REMOTE_BUILD_CONTRACT.md` at `54ed8ada`/later chain.
- Physical proof: app-only laptop flash and esptool verification; F00 stable over two reboots; human touch sequence PASS with matching releases, no hold repeats, invalid touches actionless; no panic/watchdog/brownout; display/radio/peers/local virtual-strip telemetry healthy.
- Caveats: PMU/IMU UNKNOWN/unavailable. Accepted app includes bounded diagnostics; do not silently strip them without a new build and physical re-test.
- No PR created. No push, deployment, promotion, or device action performed.
- Publication gate: exact HEAD is not currently reachable from Steve canonical or Greg fork refs observed (`main` remains `c6522ace...`). Transport/push the exact source first, then re-check provenance before Easy Flash packaging.
