const {app, BrowserWindow} = require("electron");
let args = process.argv;

host = "127.0.0.1";
port = 8080;

function createWindow(){
	let id_name, file_path;
	if(args.length < 4){
		url = "";
	}else{
		where_to_look = args[2];
		if(where_to_look == "global"){
			id_name = args[3];
			host = host;
			port = port;
			url = `http://${host}:${port}/${id_name}.html`;
		}else if(where_to_look == "net"){
			url = args[3];
		}else
			file_path = args[3];
	}
	let win = new BrowserWindow({
		width: 800,
		height: 600
	});
	win.setMenu(null);
	if(where_to_look == "local")
		win.loadFile(file_path)
	else
		win.loadURL(url);
}

app.whenReady().then(createWindow);

app.on("window-all-closed", ()=>{
	app.quit();
});
