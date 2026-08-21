# S3 Remote source-provenance transport packet

Status: **PACKAGING BLOCKED — do not publish, promote, deploy, or mutate the current release.**

## Accepted source

- Repository: `https://github.com/theysayheygreg/WLEDtubes.git`
- Worktree: `/private/tmp/wledtubes-s3-recovery`
- Branch: `agent/s3-recovery-candidate`
- Exact tested HEAD: `10d7ac0d7e7f7407ba114195475111c74fe53629`
- Worktree status: clean
- Expected transport: push the exact branch/commit to an authorized remote, then open the explicitly authorized PR/transport path. No PR was created by this work.
- Observed remote state: Steve canonical `origin/main` and Greg fork `fork/main` both resolve to `c6522acef3e954b14aad30d6f687cdb99bd1624e`; neither exposes `10d7ac0d` or `agent/s3-recovery-candidate`.

## Commit chain from the current Easy Flash source pin

`45318507` -> `fbeff278` -> `54ed8ada` -> `1bad186c` -> `f64d1f09` -> `4cd12103` -> `10d7ac0d`

- `45318507` product-required S3 peer telemetry synchronization and contract/hitbox behavior.
- `fbeff278` diagnostic-only bounded holistic field diagnostics (125 Hz diagnostic polling path); retain in the physically accepted app receipt unless a separately built release-clean artifact is physically re-tested.
- `54ed8ada` product-required S3 remote build contract.
- `1bad186c` product-required stable S3 remote local identity (F00 acceptance fix).
- `f64d1f09` product-required touch press lifecycle fix.
- `4cd12103` product-required touch release polling fix.
- `10d7ac0d` product-required bounded 125 Hz touch polling cadence fix and associated tests.
- `1b15cf90` is Easy Flash/browser-only and is not part of the firmware source chain; preserve the already-pushed Easy Flash main separately.

## Exact accepted app bytes

- Source artifact: `build_output/firmware/waveshare_s3_tubes_remote.bin`
- Size: `1,210,192` bytes
- SHA-256: `16fdd640d67a48d499eca3146da22bdda0e95076ab6d0f38df14911d759212a2`
- The local artifact was verified to match this size and hash.
- It is an application image, not a merged image. A future candidate must assemble a new merged image from this exact app plus the reviewed S3 bootloader, partition table, and boot_app0; never reuse the prior merged image.
- S3 flash mode must remain `keep`; do not introduce `qio`/`qout`.

## Physical acceptance carried by this packet

- App-only laptop flash; esptool verification passed.
- Stable local ID F00 across two reboots on the identity fix.
- Latest touch build human-tested PASS: conductor, home, conductor, home, previous, next, previous, next, follow, master, home.
- Every accepted press had a matching release; holds produced no repeated actions; invalid touches were actionless.
- No panic, watchdog, or brownout. 480x480 display, radio, peers, and local virtual-strip telemetry healthy.
- PMU and IMU remain UNKNOWN/unavailable.

## Publication gate

Do not create or point a release manifest at `10d7ac0d` until the exact commit is reachable from the canonical/authorized source transport and independently checked out clean. Then decide explicitly whether to publish the instrumented accepted app or build and physically re-test a release-clean app with diagnostics removed. Do not silently strip diagnostics or claim a clean build was physically accepted.

Only after that gate: create a new immutable provisional release ID, preserve Dig2Go/Athom artifacts and metadata byte-for-byte, assemble/hash the new S3 merged image, update granular hardware evidence (`machine+touch: pass`, `PMU: unknown`, `IMU: unknown`), and run the full Easy Flash verification suite.
