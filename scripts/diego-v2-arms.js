/* V22Z: calibrate only Diego V2's expressive-arm rest, never its skin bind pose.
 * The mesh was authored in A-pose (~36 degrees); the shared controller expects
 * arms almost down. Correct the captured rest quaternion once before use.
 */
function diegoV2CalibrateArms(H){
 if(H.m.userData.diegoAssetId!=='ZOMBIE_DIEGO_V2')throw Error('Diego arm calibration: unexpected asset');
 const report={};
 for(const side of ['l','r']){
  const rest=H.armBind['upperarm_'+side],forearm=H.bn['lowerarm_'+side];
  if(!rest||!forearm)throw Error('Diego arm calibration: missing joint');
  const original=forearm.position.clone().applyQuaternion(rest.q).normalize();
  const target=new THREE.Vector3(side==='l'?.10:-.10,-1,.025).normalize();
  const delta=new THREE.Quaternion().setFromUnitVectors(original,target);
  rest.q.premultiply(delta).normalize();
  const corrected=forearm.position.clone().applyQuaternion(rest.q).normalize();
  report[side]={beforeDegrees:Math.atan2(Math.abs(original.x),-original.y)*180/Math.PI,
   afterDegrees:Math.atan2(Math.abs(corrected.x),-corrected.y)*180/Math.PI};
 }
 H.armCalibration=report;
}
