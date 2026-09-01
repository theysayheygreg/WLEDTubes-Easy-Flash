#!/usr/bin/env node
import {createHash} from "node:crypto";
import {cp,readFile,rm,writeFile} from "node:fs/promises";
import {join,resolve} from "node:path";

const RELEASE="preview-p2p-local-605dbe99-v51-native",COMMIT="605dbe990b14a1fcc33e08bde9fabc5af0e1295d";
const args=process.argv.slice(2),index=args.indexOf("--output"),out=resolve(index<0?"build/v51-preview-site":args[index+1]),staged=resolve("easy-flash/releases",RELEASE),hash=bytes=>createHash("sha256").update(bytes).digest("hex");
const receipt=JSON.parse(await readFile(join(staged,"provenance/preview-receipt.json")));
if(receipt.source.commit!==COMMIT||receipt.source.nativeReleaseVersion!==51||receipt.source.releaseVersionOverride!==null||receipt.matrix.length!==4)throw Error("staged merged-main native-v51 matrix identity mismatch");
for(const artifact of receipt.artifacts){const bytes=await readFile(resolve("easy-flash",artifact.path));if(bytes.length!==artifact.sizeBytes||hash(bytes)!==artifact.sha256)throw Error(`${artifact.targetId} staged artifact mismatch`);}
await rm(out,{recursive:true,force:true});await cp("dist",out,{recursive:true});
await rm(join(out,"releases"),{recursive:true,force:true});
for(const file of ["index.html","styles.css","firmware-bench.css","app.mjs","fleet-update.mjs","hosted-release.mjs","local-flash.mjs","boot-verification.mjs","profiles.mjs","firmware-ui.mjs","device-identity.mjs","safety-contract.mjs","operation-receipts.mjs","diagnose.mjs","p2p-seed.mjs"])await cp(resolve("easy-flash",file),join(out,file));
await cp("easy-flash/maintainer",join(out,"maintainer"),{recursive:true,force:true});await cp("easy-flash/vendor",join(out,"vendor"),{recursive:true,force:true});await cp(staged,join(out,"releases",RELEASE),{recursive:true,force:true});await cp("_headers",join(out,"_headers"));
await writeFile(join(out,"current.json"),JSON.stringify({releaseId:RELEASE,manifest:`releases/${RELEASE}/manifest.json`,generatedAt:new Date().toISOString(),provisional:true,previewChannel:"local-s3-carrier-native-v51-matrix"},null,2)+"\n");
console.log(`built self-contained ${RELEASE} at ${out}`);
