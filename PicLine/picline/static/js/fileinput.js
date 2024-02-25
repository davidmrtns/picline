let input = document.getElementById("foto");
let imagemArquivo = document.getElementById("imagem-arquivo");

input.addEventListener("change", () => {
    let inputImagem = document.querySelector("input[type=file]").files[0];

    imagemArquivo.classList.add("visivel");
    imagemArquivo.innerText = inputImagem.name;
});