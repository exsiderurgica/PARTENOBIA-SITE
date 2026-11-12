/* V23A: hanging-forward arms in model space, compensating the hunched torso.
 * Swing bone directions only: no joint translation, skin-bind edits or two-bone IK.
 */
function diegoV2ForwardArms(H,dt,phase,speed){
 zombieExpressiveArms(H,dt,phase,speed);
 DIEGO.root.scale.setScalar(churchCharacterScaleAt(DIEGO.z));
 H.m.updateWorldMatrix(true,true);
 const state=H.armState;
 function aim(bone,child,direction){
  const desired=direction.clone().transformDirection(H.m.matrixWorld);
  const parentQ=bone.parent.getWorldQuaternion(new THREE.Quaternion()).invert();
  desired.applyQuaternion(parentQ).normalize();
  const current=child.position.clone().applyQuaternion(bone.quaternion).normalize();
  bone.quaternion.premultiply(new THREE.Quaternion().setFromUnitVectors(current,desired)).normalize();
  bone.updateWorldMatrix(false,true);
 }
 for(const side of ['l','r']){
  const reach=THREE.MathUtils.clamp(side==='l'?state.left:state.right,0,1);
  const sign=side==='l'?1:-1;
  const upper=(22+48*reach)*Math.PI/180,lower=(32+45*reach)*Math.PI/180;
  aim(H.bn['upperarm_'+side],H.bn['lowerarm_'+side],new THREE.Vector3(sign*.08,-Math.cos(upper),Math.sin(upper)));
  aim(H.bn['lowerarm_'+side],H.bn['hand_'+side],new THREE.Vector3(sign*.035,-Math.cos(lower),Math.sin(lower)));
 }
 H.m.updateWorldMatrix(true,true);
}
