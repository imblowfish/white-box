let options = {
	debug:"info",
	modules: {
		// toolbar: "#toolbar"
	},
	theme:"snow"
}
			
let quill = new Quill("#editor", options);

function SaveHtml(){
	// alert(document.getElementsByClassName("ql-preview"));
	var htmlContent = document.getElementsByClassName("ql-editor")[0].innerHTML;
	alert(htmlContent);
	var bl = new Blob([htmlContent], {type: "text/html"});
	var a = document.createElement("a");
	a.href = URL.createObjectURL(bl);
	a.download = "your-download-name-here.html";
	a.hidden = true;
	document.body.appendChild(a);
	a.innerHTML = "something random - nobody will see this, it doesn't matter what you put here";
	a.click();
}
button = document.getElementById("button_save");
button.onclick = SaveHtml;