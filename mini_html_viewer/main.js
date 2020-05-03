// let remote = require("electron").remote;
const log = require("electron-log");
const {app, BrowserWindow} = require("electron");
let args = process.argv;

host = "127.0.0.1";
port = 8080;

function createWindow(){
	let id_name, file_path;
	if(args.length < 4){
		url = "";
	}else{
		server = (args[2]).toLowerCase();
		if(server == "global"){
			id_name = id_name = args[3];
			host = host;
			port = port;
			url = `http://${host}:${port}/${id_name}.html`;
		}else
			file_path = args[3];
	}
	let win = new BrowserWindow({
		width: 800,
		height: 600,
		webPreferences:{
			nodeIntegration: true
		}
	});
	if(server == "global")
		win.loadURL(url);
	else
		win.loadFile(file_path)
}

app.whenReady().then(createWindow);

app.on("window-all-closed", ()=>{
	app.quit();
});
