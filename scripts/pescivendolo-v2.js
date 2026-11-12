/* Zombie Pescivendolo V2. Existing AI, retarget, combat and footfalls stay active.
 * Embedded demonstration clips are intentionally not played by the game. */
const PESCIVENDOLO_V2_ASSET={id:'ZOMBIE_PESCIVENDOLO_V2',label:'Zombie Pescivendolo V2',
 sha256:'fa2fb2711747bddafffef1d2d8f6ed34ebe5cfe578a00b590b4feb84ec77f899',vertices:31267,triangles:60752};
function pescivendoloV2Configure(model){
 let found=false;
 model.traverse(o=>{if(!o.isSkinnedMesh)return;
  if(o.geometry.attributes.position.count!==PESCIVENDOLO_V2_ASSET.vertices||o.skeleton.bones.length!==23||!o.material.map)
   throw Error('Zombie Pescivendolo V2: unexpected geometry, rig or atlas');
  found=true;
 });
 if(!found)throw Error('Zombie Pescivendolo V2: skinned mesh missing');
 model.userData.pescivendoloAssetId=PESCIVENDOLO_V2_ASSET.id;
}
window.__partenobiaPescivendoloV2={status:()=>({version:'V22Y TEST',asset:PESCIVENDOLO_V2_ASSET,
 instances:N19_ENEMIES.filter(v=>v.name==='Zombie Pescivendolo V2').map(v=>({room:v.kind,ready:!!v.ready,
 animationReady:!!v.animReady,assetId:v.model?.userData.pescivendoloAssetId||null,
 bones:Object.keys(v.bones).length,error:v.error||v.animError||null,dead:!!v.dead,hits:v.hits||0}))})};
