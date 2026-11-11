/* Edoardo nuovo V01: replacement approved by the author on 2026-11-11.
 * Keep independent rigs, combat geometry and AI. Share only the immutable image.
 * The TEST clips bundled in the GLB are intentionally NOT played by the game:
 * the existing PARTENOBIA retargeting, attacks and collapse controllers remain active.
 */
const EDOARDO_NUOVO_ASSET={id:'EDOARDO_NUOVO_V01',label:'Edoardo nuovo',
 sha256:'1226bd1929754f19fd1e98fecffbec849261d7f914b7ef8c5af2f1c50f0b223e',
 vertices:28184,triangles:54704};
let edoardoNuovoSharedMap=null;
function edoardoNuovoConfigure(model){
 model.userData.edoardoAssetId=EDOARDO_NUOVO_ASSET.id;
 let found=false;
 model.traverse(o=>{
  if(!o.isSkinnedMesh)return;
  if(o.geometry.attributes.position.count!==EDOARDO_NUOVO_ASSET.vertices||
     o.skeleton.bones.length!==23||!o.material.map)
    throw Error('Edoardo nuovo: GLB, texture o rig inattesi');
  const map=o.material.map;
  if(!edoardoNuovoSharedMap)edoardoNuovoSharedMap=map;
  else if(map!==edoardoNuovoSharedMap){
   o.material.map=edoardoNuovoSharedMap;
   map.dispose();
   // GLTFLoader may decode to ImageBitmap. Release discarded duplicate pixels.
   if(map.image&&typeof map.image.close==='function')map.image.close();
  }
  found=true;
 });
 if(!found)throw Error('Edoardo nuovo: mesh con skin assente');
}
window.__partenobiaEdoardoNuovo={status:()=>{
 const records=[{room:'vicolo-storico',actor:EDOARDO},
  ...FONT_ENEMIES.filter(v=>v.name==='Edoardo').map(v=>({room:'fontanelle',actor:v})),
  ...N19_ENEMIES.filter(v=>v.name==='Edoardo').map(v=>({room:v.kind,actor:v}))];
 const maps=new Set();
 return {version:'V22U',asset:EDOARDO_NUOVO_ASSET,instances:records.map(({room,actor:v})=>{
  const model=v.H?.m;let vertices=0,bones=0,textureSize=null,skin=null;
  model?.traverse(o=>{if(o.isSkinnedMesh){vertices+=o.geometry.attributes.position.count;
   bones=o.skeleton.bones.length;skin=o.skeleton;const map=o.material.map;
   if(map){maps.add(map);textureSize=[map.image.width,map.image.height]}}});
  return {room,ready:!!v.ready,assetId:model?.userData.edoardoAssetId||null,
   vertices,bones,textureSize,dead:!!v.dead,hits:v.hits||0,
   animationReady:!!v.animReady,error:v.error||v.animError||null};
 }),get sharedTextures(){return maps.size}};
}};
