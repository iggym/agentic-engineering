// Agentic Engineering — shared article behaviour (progressive enhancement).
// The page is fully readable without this script.
(function(){
  // reading progress bar
  var bar = document.querySelector('.progress');
  if(bar){
    var onScroll = function(){
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    };
    document.addEventListener('scroll', onScroll, {passive:true});
    onScroll();
  }

  // execution trace: step through stages, reveal root cause
  document.querySelectorAll('.trace').forEach(function(trace){
    var items = Array.prototype.slice.call(trace.querySelectorAll('li'));
    var stepBtn = trace.querySelector('[data-action="step"]');
    var revealBtn = trace.querySelector('[data-action="reveal"]');
    var note = trace.querySelector('.trace-note');
    var idx = -1;
    function show(i){
      items.forEach(function(li, j){ li.classList.toggle('current', j === i); });
      if(note && items[i]){
        note.textContent = 'stage ' + (i + 1) + ' of ' + items.length + ' — ' + items[i].querySelector('.st').textContent.trim();
      }
    }
    items.forEach(function(li, i){
      li.tabIndex = 0;
      li.addEventListener('click', function(){ idx = i; show(i); });
      li.addEventListener('keydown', function(e){
        if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); idx = i; show(i); }
      });
    });
    if(stepBtn){
      stepBtn.addEventListener('click', function(){ idx = (idx + 1) % items.length; show(idx); });
    }
    if(revealBtn){
      revealBtn.addEventListener('click', function(){
        var on = trace.classList.toggle('reveal');
        revealBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
        revealBtn.textContent = on ? 'Hide root cause' : 'Show root cause';
      });
    }
  });
})();
