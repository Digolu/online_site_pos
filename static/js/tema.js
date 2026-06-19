/* ============================================
   Sistema POS · Lógica de tema (claro/escuro)
   Guardar em: static/js/tema.js
   ============================================ */

// Aplica o tema guardado ANTES da página renderizar (evita "flash" do tema errado)
(function () {
  const temaGuardado = localStorage.getItem("tema") || "claro";
  document.documentElement.setAttribute("data-tema", temaGuardado);
})();

// Alterna entre claro/escuro e guarda a escolha
function alternarTema() {
  const atual = document.documentElement.getAttribute("data-tema");
  const novo = atual === "escuro" ? "claro" : "escuro";
  document.documentElement.setAttribute("data-tema", novo);
  localStorage.setItem("tema", novo);
  atualizarIconeTema(novo);
}

// Troca o ícone do botão (sol/lua) conforme o tema atual
function atualizarIconeTema(tema) {
  const icone = document.getElementById("tema-icone");
  const texto = document.getElementById("tema-texto");
  if (!icone || !texto) return;

  if (tema === "escuro") {
    icone.innerHTML = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>';
    texto.textContent = "Claro";
  } else {
    icone.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
    texto.textContent = "Escuro";
  }
}

// Ao carregar a página, sincroniza o ícone com o tema ativo
window.addEventListener("DOMContentLoaded", () => {
  const temaAtual = document.documentElement.getAttribute("data-tema") || "claro";
  atualizarIconeTema(temaAtual);
});