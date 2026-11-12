/* V22W: one footfall recipe, exactly the existing Pulcinella drag + stone mix.
 * No new sample or alternate timbre; only room gain/pan and actual travel vary.
 */
function sfxZombieStep(pan,vol){
 sfxDrag(pan,vol);
 sfxUndeadFootstep(pan,.65*vol);
}
function zombieTravelStep(v,travel,pan,vol){
 if(!v||v.dead||!Number.isFinite(travel)||travel<=0)return;
 v._v22wStepDistance=(v._v22wStepDistance||0)+travel;
 if(v._v22wStepDistance<.27)return;
 v._v22wStepDistance%=.27;
 sfxZombieStep(pan,vol);
}
const DIEGO_V2_ASSET={id:'ZOMBIE_DIEGO_V2',label:'Zombie Diego V2',
 sha256:'658a2cd501eeef95270727e34043d32741909a44cdb9be642c8a9f7f79ed2718',
 vertices:43886,triangles:83932};
function diegoV2Configure(model){
 let found=false;
 model.traverse(o=>{if(!o.isSkinnedMesh)return;
  if(o.geometry.attributes.position.count!==DIEGO_V2_ASSET.vertices||o.skeleton.bones.length!==23||!o.material.map)
   throw Error('Zombie Diego V2: unexpected model, rig or atlas');
  found=true;
 });
 if(!found)throw Error('Zombie Diego V2: skinned mesh missing');
 model.userData.diegoAssetId=DIEGO_V2_ASSET.id;
}
window.__partenobiaV22W={status:()=>({version:'V22W TEST',asset:DIEGO_V2_ASSET,
 diego:{ready:DIEGO.ready,animationReady:!!DIEGO.animReady,assetId:DIEGO.model?.userData.diegoAssetId,
 error:DIEGO.error||null,bones:Object.keys(DIEGO.bones).length,scale:DIEGO.root?.scale.x},
 footsteps:'Pulcinella: sfxDrag(pan,vol) + sfxUndeadFootstep(pan,.65*vol)',
 hero:window.__heroAssetVersion})};
