import json,hashlib,shutil,os
from pathlib import Path
root=Path('/private/tmp/easy-flash-s3-candidate'); old='provisional-pr70-45318507'; rid='functional-s3-checkpoint-10d7ac0d'; src=root/'dist/releases'/old; dst=root/'dist/releases'/rid
shutil.copytree(src,dst)
# replace S3 merged image using exact accepted app and prior reviewed non-app slices
oldm=(src/'firmware/waveshare-s3-tubes-remote-merged.bin').read_bytes(); app=Path('/private/tmp/wledtubes-s3-recovery/build_output/firmware/waveshare_s3_tubes_remote.bin').read_bytes()
merged=oldm[:65536]+app
(dst/'firmware/waveshare-s3-tubes-remote-merged.bin').write_bytes(merged)
def sha(b): return hashlib.sha256(b).hexdigest()
manifest=json.loads((dst/'manifest.json').read_text()); rec=json.loads((dst/'provenance/build-receipt.json').read_text())
for v,t in zip(manifest['variants'],rec['sourceReceipt']['targets']):
 v['artifacts'][0]['path']=v['artifacts'][0]['path'].replace(old,rid)
 v['provenance']['partitionPath']=v['provenance']['partitionPath'].replace(old,rid)
 if v['id']=='waveshare-s3-tubes-remote':
  s=v['source'];s.update(repository='https://github.com/theysayheygreg/WLEDtubes.git',commit='10d7ac0d7e7f7407ba114195475111c74fe53629',clean=True)
  v['bootIdentity']['source']=s['commit'];v['description']='Functional recovery/test checkpoint; product design and feature restoration in progress. PMU/IMU unknown.'
  a=v['artifacts'][0];a.update(sizeBytes=len(merged),sha256=sha(merged));a['components'][-1].update(sizeBytes=len(app),sha256=sha(app));v['provenance']['ota'].update(sizeBytes=len(app),sha256=sha(app))
  t['bootIdentity']['source']=s['commit'];t['artifacts']['usb'].update(lengthBytes=len(merged),sha256=sha(merged));t['artifacts']['usb']['components'][-1].update(lengthBytes=len(app),sha256=sha(app));t['artifacts']['ota'].update(lengthBytes=len(app),sha256=sha(app))
  # target source registry ref
  v['sourceRef']='greg-s3-10d7ac0d'
for v in manifest['variants'][:2]: v['sourceRef']='steve-f0ccd8b2'
# explicit registry, backwards-compatible source fields retained
manifest['sourceRegistry']={'steve-f0ccd8b2':{'repository':'https://github.com/SteveEisner/WLEDtubes.git','commit':'f0ccd8b28d44b2411f4ed9ba491e3a342e092566','clean':True},'greg-s3-10d7ac0d':{'repository':'https://github.com/theysayheygreg/WLEDtubes.git','commit':'10d7ac0d7e7f7407ba114195475111c74fe53629','clean':True}}
manifest['provisional']=True; manifest['promotion']='Functional S3 recovery/test checkpoint; product design and feature restoration in progress. PMU/IMU unknown.'
# receipt per-target source refs
rec['sourceReceipt']['targets'][2]['sourceRef']='greg-s3-10d7ac0d';rec['sourceReceipt']['targets'][0]['sourceRef']='steve-f0ccd8b2';rec['sourceReceipt']['targets'][1]['sourceRef']='steve-f0ccd8b2'
rec['sourceRegistry']=manifest['sourceRegistry']
# update all paths and digests
for x in [manifest,rec]:
 pass
(dst/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');
# receipt digest chain recompute after source receipt mutation
sr=rec['sourceReceipt']; rec['sourceReceiptDigestSha256']=sha(json.dumps(sr,sort_keys=True,separators=(',',':')).encode()); rec['receiptDigestSha256']=''
rec['receiptDigestSha256']=sha(json.dumps({k:v for k,v in rec.items() if k!='receiptDigestSha256'},sort_keys=True,separators=(',',':')).encode())
(dst/'provenance/build-receipt.json').write_text(json.dumps(rec,indent=2)+'\n')
# manifest hashes
m=json.loads((dst/'manifest.json').read_text()); rbytes=(dst/'provenance/build-receipt.json').read_bytes();m['provenance']['receiptDigestSha256']=rec['receiptDigestSha256'];m['provenance']['sourceReceiptDigestSha256']=rec['sourceReceiptDigestSha256'];m['provenance']['evidence']['receipt']['sha256']=sha(rbytes);m['provenance']['evidence']['receipt']['path']=m['provenance']['evidence']['receipt']['path'].replace(old,rid);m['provenance']['evidence']['contract']['path']=m['provenance']['evidence']['contract']['path'].replace(old,rid)
for v in m['variants']:
 v['artifacts'][0]['path']=v['artifacts'][0]['path'].replace(old,rid);v['provenance']['partitionPath']=v['provenance']['partitionPath'].replace(old,rid)
(dst/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
# current pointer
(root/'dist/current.json').write_text(json.dumps({'releaseId':rid,'manifest':f'releases/{rid}/manifest.json','generatedAt':'2026-08-21T00:00:00.000Z','provisional':True},indent=2)+'\n')
