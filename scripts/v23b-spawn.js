/* Place the cab's existing Edoardo once, at the left side of the initial view.
 * On portrait screens he enters from the left edge instead of appearing centrally.
 * Preserve position/health on revisits and never move the protagonist.
 */
function v23bCabLeftSpawn(v){
 if(v._v23bSpawnPlaced)return;
 let x=180;
 if(VW.portrait){
  const width=innerWidth/VW.s;
  const left=Math.max(0,Math.min(Math.max(0,IW-width),N19_CFG.cab.spawn[0]-width/2));
  x=Math.max(80,left-50);
 }
 const p=n19FromScreen('cab',x,880);
 v.x=p.x;v.z=p.z;v.spawn=[x,880];v._v23bSpawnPlaced=true;
 if(VW.portrait)V20.grace=Math.max(V20.grace,2.3);
}
