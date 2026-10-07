/* Dominion Hard Money: mobile menu and the language picker (Google Translate). */
(function(){
  var h=document.querySelector('header'),mb=h&&h.querySelector('.menu-btn');
  if(mb){mb.addEventListener('click',function(){var o=h.classList.toggle('open');mb.setAttribute('aria-expanded',o?'true':'false');});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&h.classList.contains('open')){h.classList.remove('open');mb.setAttribute('aria-expanded','false');mb.focus();}});}
  var r=document.getElementById('hml');if(!r)return;
  var b=document.getElementById('hmlBtn'),mn=document.getElementById('hmlMenu'),fl=document.getElementById('hmlFlag'),cd=document.getElementById('hmlCode');
  function cur(){var m=document.cookie.match(/googtrans=\/[^/]+\/([a-zA-Z-]+)/);return (m&&m[1])||'en';}
  function paint(c){var hit=null;Array.prototype.forEach.call(mn.children,function(e){var on=e.dataset.l===c;e.classList.toggle('on',on);e.setAttribute('aria-selected',on?'true':'false');if(on)hit=e;});if(!hit)hit=mn.children[0];fl.innerHTML=hit.querySelector('.hml-f').innerHTML;cd.textContent=hit.dataset.s;}
  function set(c){if(c===cur())return;var host=location.hostname,v=(c==='en')?'/en/en':'/en/'+c;document.cookie='googtrans='+v+';path=/';document.cookie='googtrans='+v+';path=/;domain='+host;var p=host.split('.');if(p.length>1)document.cookie='googtrans='+v+';path=/;domain=.'+p.slice(-2).join('.');location.reload();}
  Array.prototype.forEach.call(mn.children,function(e){e.addEventListener('click',function(){set(e.dataset.l);});});
  b.addEventListener('click',function(ev){ev.stopPropagation();var o=r.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});
  document.addEventListener('click',function(ev){if(!r.contains(ev.target)){r.classList.remove('open');b.setAttribute('aria-expanded','false');}});
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape'){r.classList.remove('open');b.setAttribute('aria-expanded','false');}});
  paint(cur());
  if(cur()!=='en'){
    var d=document.createElement('div');d.id='google_translate_element';document.body.appendChild(d);
    window.googleTranslateElementInit=function(){new google.translate.TranslateElement({pageLanguage:'en',includedLanguages:'en,es,zh-CN,vi,ko,ru,pt',autoDisplay:false},'google_translate_element');};
    var s=document.createElement('script');s.src='https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';document.body.appendChild(s);
  }
})();
