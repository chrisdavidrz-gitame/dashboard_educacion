// 1) Clase al botón logout
(function(){
  try {
    const btn = window.parent.document.querySelector('.logout-wrap button');
    if (btn) {
      btn.classList.add('btn-logout');
      btn.setAttribute('data-role','logout');
    }
  } catch(e) {}
})();

// 2) Forzar color chips multiselect
(function(){
  function applyChips(){
    try{
      const parentDoc = window.parent.document;
      parentDoc.querySelectorAll('span[data-baseweb="tag"]').forEach(n=>{
        try{
          n.style.backgroundColor = '#3E5A7E';
          n.style.color = '#ffffff';
          n.style.borderColor = 'rgba(0,0,0,0.08)';
        } catch(e){}
      });

      parentDoc.querySelectorAll('span[data-baseweb="tag"] svg').forEach(svg=>{
        try{
          svg.style.color = '#000000';
          svg.style.fill = '#000000';
        } catch(e){}
      });
    } catch(e){}
  }

  applyChips();
  const parentDoc = window.parent.document;
  const mo = new MutationObserver(()=>{ applyChips(); });
  mo.observe(parentDoc.body, { childList: true, subtree: true });
  setInterval(applyChips, 1000);
})();

// 3) Agregar clase al botón Progresar
(function(){
  function tagProgresar(){
    try{
      const doc = window.parent.document;
      const btns = Array.from(doc.querySelectorAll('button'));
      const b = btns.find(x => (x.innerText || "").trim() === "Progresar");
      if(b){
        b.classList.add("btn-progresar-icon");
      }
    } catch(e){}
  }

  tagProgresar();
  const mo = new MutationObserver(tagProgresar);
  mo.observe(window.parent.document.body, {childList:true, subtree:true});
})();

(function () {
  function tagMenuButtons() {
    try {
      const doc = window.parent.document;
      const btns = Array.from(doc.querySelectorAll("button"));

      function addIfIncludes(keyword, classes) {
        const b = btns.find(x => ((x.innerText || "").toLowerCase()).includes(keyword));
        if (!b) return;
        classes.forEach(c => b.classList.add(c));
      }

      // OJO: usamos keywords simples (sin emojis ni saltos de linea)
      addIfIncludes("vouchers", ["btn-menu-icon", "btn-menu-vouchers"]);
      addIfIncludes("becas", ["btn-menu-icon", "btn-menu-becas"]);
      addIfIncludes("comedores", ["btn-menu-icon", "btn-menu-comedores"]);
      addIfIncludes("libros", ["btn-menu-icon", "btn-menu-libros"]);

    } catch (e) { }
  }

  tagMenuButtons();
  const mo = new MutationObserver(tagMenuButtons);
  mo.observe(window.parent.document.body, { childList: true, subtree: true });
})();


(function () {
  function tagMenuButtons() {
    try {
      const doc = window.parent.document;
      const btns = Array.from(doc.querySelectorAll("button"));

      function addIfIncludes(keyword, classes) {
        const b = btns.find(x => ((x.innerText || "").toLowerCase()).includes(keyword));
        if (!b) return;
        classes.forEach(c => b.classList.add(c));
      }

      // keywords simples (no dependen de emojis ni \n)
      addIfIncludes("vouchers", ["btn-menu-icon", "btn-menu-vouchers"]);
      addIfIncludes("becas", ["btn-menu-icon", "btn-menu-becas"]);
      addIfIncludes("comedores", ["btn-menu-icon", "btn-menu-comedores"]);
      addIfIncludes("libros", ["btn-menu-icon", "btn-menu-libros"]);
    } catch (e) {}
  }

  // Ejecutar varias veces por si Streamlit re-renderiza
  tagMenuButtons();
  const mo = new MutationObserver(tagMenuButtons);
  mo.observe(window.parent.document.body, { childList: true, subtree: true });
  setInterval(tagMenuButtons, 1000);
})();
