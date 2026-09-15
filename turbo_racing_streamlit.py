import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🏎️ Turbo Racing", page_icon="🏎️", layout="centered")

HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
*{box-sizing:border-box}
body{margin:0;background:#10131a;color:#fff;font-family:Arial,sans-serif;overflow:hidden}
.wrap{max-width:430px;margin:auto}
.top{display:flex;justify-content:space-between;gap:6px;margin:5px 0}
.box{background:#1c2230;border:1px solid #384158;border-radius:10px;padding:7px;text-align:center;flex:1}
.box b{display:block;font-size:18px}
canvas{display:block;width:100%;height:auto;background:#222;border-radius:16px;border:3px solid #59647b;touch-action:none}
.controls{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:9px}
button{height:54px;border:0;border-radius:13px;background:#273148;color:#fff;font-size:22px;font-weight:bold;box-shadow:0 3px 0 #151a26;touch-action:manipulation}
button:active{transform:translateY(2px);box-shadow:none}
.gas{background:#1e6b4a}.brake{background:#71363a}.nitro{background:#245d82}
.start{grid-column:1/4;background:#8b4fd3}
.bar{height:10px;background:#252b3a;border-radius:9px;overflow:hidden;margin-top:7px}
.fill{height:100%;width:100%;background:#36b9ff;transition:.08s}
#msg{text-align:center;font-weight:bold;min-height:24px;margin:7px}
small{opacity:.75}
</style>
</head>
<body>
<div class="wrap">
<div class="top">
 <div class="box">🏆<b id="score">0</b><small>Điểm</small></div>
 <div class="box">🏁<b id="lap">1/3</b><small>Vòng</small></div>
 <div class="box">⚡<b id="speed">0</b><small>km/h</small></div>
</div>
<canvas id="game" width="420" height="650"></canvas>
<div id="msg">Nhấn BẮT ĐẦU để đua!</div>
<div class="bar"><div id="nitrobar" class="fill"></div></div>
<div class="controls">
 <button onclick="left()">⬅️</button>
 <button class="gas" onclick="gas()">⛽ GAS</button>
 <button onclick="right()">➡️</button>
 <button class="brake" onclick="brake()">🛑 PHANH</button>
 <button class="nitro" onclick="nitro()">⚡ NITRO</button>
 <button onclick="togglePause()">⏸️</button>
 <button class="start" onclick="start()">🏁 BẮT ĐẦU / CHƠI LẠI</button>
</div>
</div>

<script>
const c=document.getElementById("game"),ctx=c.getContext("2d");
let running=false,paused=false,over=false;
let player={lane:1,x:0,y:550,w:48,h:82};
let enemies=[],score=0,lap=1,roadY=0,speed=0,nitroFuel=100;
let keys={left:false,right:false,gas:false,brake:false,nitro:false};
const lanes=[105,185,265];

function reset(){
 score=0;lap=1;speed=0;nitroFuel=100;roadY=0;enemies=[];
 player.x=lanes[1]; running=true;paused=false;over=false;
 document.getElementById("msg").textContent="🏎️ ĐUA!";
 for(let i=0;i<4;i++) spawn(-i*190-100);
}
function start(){reset()}
function togglePause(){if(running)paused=!paused}

function left(){player.x=Math.max(lanes[0],player.x-80)}
function right(){player.x=Math.min(lanes[2],player.x+80)}
function gas(){speed=Math.min(220,speed+22)}
function brake(){speed=Math.max(0,speed-35)}
function nitro(){
 if(nitroFuel>2){speed=Math.min(360,speed+100);nitroFuel-=12}
}
document.addEventListener("keydown",e=>{
 if(e.key==="ArrowLeft"||e.key==="a")left();
 if(e.key==="ArrowRight"||e.key==="d")right();
 if(e.key==="ArrowUp"||e.key==="w")gas();
 if(e.key==="ArrowDown"||e.key==="s")brake();
 if(e.key===" ")nitro();
});
function spawn(y=-100){
 let lane=Math.floor(Math.random()*3);
 enemies.push({x:lanes[lane],y:y,w:46,h:78,spd:45+Math.random()*70});
}
function rectHit(a,b){
 return Math.abs(a.x-b.x)<(a.w+b.w)*.42 && Math.abs(a.y-b.y)<(a.h+b.h)*.42;
}
function drawCar(x,y,w,h,main,glass){
 ctx.save();ctx.translate(x,y);
 ctx.fillStyle=main;round(-w/2,-h/2,w,h,10);ctx.fill();
 ctx.fillStyle=glass;round(-w*.30,-h*.32,w*.60,h*.27,6);ctx.fill();
 ctx.fillStyle="#111";ctx.fillRect(-w*.58,-h*.30,7,20);ctx.fillRect(w*.44,-h*.30,7,20);
 ctx.fillRect(-w*.58,h*.15,7,20);ctx.fillRect(w*.44,h*.15,7,20);
 ctx.fillStyle="#fff";ctx.fillRect(-w*.26,h*.31,w*.52,5);
 ctx.restore();
}
function round(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.closePath()}

function draw(){
 ctx.clearRect(0,0,c.width,c.height);
 // grass
 ctx.fillStyle="#267342";ctx.fillRect(0,0,c.width,c.height);
 // road
 ctx.fillStyle="#30343a";ctx.fillRect(55,0,310,c.height);
 // curbs
 for(let y=-80+(roadY%80);y<c.height;y+=80){
   ctx.fillStyle="#eee";ctx.fillRect(45,y,10,40);ctx.fillStyle="#d43c3c";ctx.fillRect(45,y+40,10,40);
   ctx.fillStyle="#eee";ctx.fillRect(365,y,10,40);ctx.fillStyle="#d43c3c";ctx.fillRect(365,y+40,10,40);
 }
 // lane markings
 ctx.fillStyle="#eee";
 for(let y=-80+(roadY%90);y<c.height;y+=90){
   ctx.fillRect(153,y,7,48);ctx.fillRect(260,y,7,48);
 }
 // start/finish pattern
 if(lap>=3){
   ctx.fillStyle="#fff";ctx.fillRect(55,70-roadY%650,310,16);
 }
 enemies.forEach(e=>drawCar(e.x,e.y,e.w,e.h,"#e44","#a9d8ff"));
 drawCar(player.x,player.y,player.w,player.h,"#23a7ff","#bdefff");
 // nitro flame
 if(keys.nitro&&nitroFuel>0){
   ctx.fillStyle="#ffd43b";ctx.beginPath();ctx.moveTo(player.x-12,595);ctx.lineTo(player.x,630);ctx.lineTo(player.x+12,595);ctx.fill();
 }
}

function update(){
 if(running&&!paused&&!over){
   let target=80;
   if(keys.gas)target=190;
   if(keys.brake)target=25;
   if(keys.nitro&&nitroFuel>0){target=330;nitroFuel-=0.8}
   else nitroFuel=Math.min(100,nitroFuel+0.12);
   speed += (target-speed)*0.055;
   roadY += speed*0.06;
   enemies.forEach(e=>e.y += (speed*0.045+e.spd*0.015));
   enemies=enemies.filter(e=>e.y<730);
   if(enemies.length<4)spawn(-80-Math.random()*180);
   for(const e of enemies)if(rectHit(player,e)){over=true;running=false;document.getElementById("msg").textContent="💥 CRASH! Nhấn chơi lại."}
   score += speed*0.002;
   if(Math.floor(score)>0 && Math.floor(score)%250===0)lap=Math.min(3,1+Math.floor(score/250));
   if(score>=750){over=true;running=false;document.getElementById("msg").textContent="🏆 BẠN ĐÃ VÔ ĐỊCH!";lap=3}
 }
 document.getElementById("score").textContent=Math.floor(score);
 document.getElementById("lap").textContent=lap+"/3";
 document.getElementById("speed").textContent=Math.floor(speed);
 document.getElementById("nitrobar").style.width=nitroFuel+"%";
 draw();requestAnimationFrame(update);
}
update();
</script>
</body>
</html>
"""

components.html(HTML, height=850, scrolling=False)
